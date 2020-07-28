use sha2::{Digest, Sha256, Sha512};
use std::convert::TryInto;
use std::slice;
use std::thread;

/// Fixed line lengths known at compilation time.
const INPUT_LEN: usize = 16;
const OUTPUT_LEN: usize = 32;
const OUTPUT_LEN_512: usize = 64;

/// Hash one line of the array.
fn raw_line(input_array_pointer: *const u8, output_array_pointer: *mut u8) {
    // Read from the raw pointers given by Numpy.
    assert!(!input_array_pointer.is_null());
    assert!(!output_array_pointer.is_null());

    // Read-only input.
    let input: &[u8] = unsafe { slice::from_raw_parts(input_array_pointer, INPUT_LEN) };

    // Mutable output, we need to know the length.
    let output: &mut [u8; OUTPUT_LEN] = unsafe {
        slice::from_raw_parts_mut(output_array_pointer, OUTPUT_LEN)
            .try_into() // Force into OUTPUT_LEN size
            .unwrap() // Panic if necessary
    };

    // Initialize a hasher, update, digest, write to array of known length.
    *output = Sha256::digest(input).into();

    // No need to free the Numpy-managed memory.
}

// // Problem: try_from does not work for arrays longer than 32.
// impl<'a, T, const N: usize> TryFrom<&'a mut [T]> for &'a mut [T; N]
// where
//     [T; N]: LengthAtMost32,
// {
//     type Error = TryFromSliceError;

//     fn try_from(slice: &mut [T]) -> Result<&mut [T; N], TryFromSliceError> {
//         if slice.len() == N {
//             let ptr = slice.as_mut_ptr() as *mut [T; N];
//             unsafe { Ok(&mut *ptr) }
//         } else {
//             Err(TryFromSliceError(()))
//         }
//     }
// }

fn raw_line_512(input_array_pointer: *const u8, output_array_pointer: *mut u8) {
    // Read from the raw pointers given by Numpy.
    assert!(!input_array_pointer.is_null());
    assert!(!output_array_pointer.is_null());

    // Read-only input.
    let input: &[u8] = unsafe { slice::from_raw_parts(input_array_pointer, INPUT_LEN) };

    // Initialize output, hasher, update, digest, write to array of known length.
    unsafe {
        // Handmade "try_into().unwrap()" with no error checking.
        let ptr = slice::from_raw_parts_mut(output_array_pointer, OUTPUT_LEN_512).as_mut_ptr()
            as *mut [u8; OUTPUT_LEN_512];

        // Dereferencing the raw pointer.
        let output: &mut [u8; OUTPUT_LEN_512] = &mut *ptr;

        // Handmade "into()".
        output.copy_from_slice(Sha512::digest(input).as_slice());
    }
    // No need to free the Numpy-managed memory.
}

/// Hash the 2D array line by line.
fn raw_sequential(input_array_pointer: *const u8, output_array_pointer: *mut u8, n_values: usize) {
    for i in 0..n_values {
        unsafe {
            raw_line(
                input_array_pointer.add(INPUT_LEN * i),
                output_array_pointer.add(OUTPUT_LEN * i),
            );
        }
    }
}

fn raw_sequential_512(
    input_array_pointer: *const u8,
    output_array_pointer: *mut u8,
    n_values: usize,
) {
    for i in 0..n_values {
        unsafe {
            raw_line_512(
                input_array_pointer.add(INPUT_LEN * i),
                output_array_pointer.add(OUTPUT_LEN_512 * i),
            );
        }
    }
}

/// Hash the 2D array in parallel.
fn raw_share_memory(
    input_array_pointer: *const u8,
    output_array_pointer: *mut u8,
    n_values: usize,
    n_threads: usize,
) {
    let mut handles = Vec::new();

    // If n_threads does not divide n_values, the last thread has more work to do.
    let normal_chunk_size = n_values / n_threads;
    let last_chunk_size = normal_chunk_size + n_values % n_threads;
    let mut chunk_size = normal_chunk_size;

    for t in 0..n_threads {
        // Trick: raw pointers (*mut u8) are not sendable, so we cast them to integers.
        let input_cast_pointer =
            unsafe { input_array_pointer.add(INPUT_LEN * normal_chunk_size * t) as usize };

        let output_cast_pointer =
            unsafe { output_array_pointer.add(OUTPUT_LEN * normal_chunk_size * t) as usize };

        // The last thread reads a bit farther.
        if t == n_threads - 1 {
            chunk_size = last_chunk_size;
        }
        // Spawn threads, uncast the raw pointers insides.
        let handle = thread::spawn(move || {
            // Raw sequential operates on ~ n_values / n_threads contiguous lines as a standalone array
            raw_sequential(
                input_cast_pointer as *const u8,
                output_cast_pointer as *mut u8,
                chunk_size,
            )
        });

        // Keep track of the spawned threads.
        handles.push(handle)
    }
    // Wait for all the threads to terminate.
    for handle in handles {
        handle.join().unwrap();
    }
}

fn raw_share_memory_512(
    input_array_pointer: *const u8,
    output_array_pointer: *mut u8,
    n_values: usize,
    n_threads: usize,
) {
    let mut handles = Vec::new();

    // If n_threads does not divide n_values, the last thread has more work to do.
    let normal_chunk_size = n_values / n_threads;
    let last_chunk_size = normal_chunk_size + n_values % n_threads;
    let mut chunk_size = normal_chunk_size;

    for t in 0..n_threads {
        // Trick: raw pointers (*mut u8) are not sendable, so we cast them to integers.
        let input_cast_pointer =
            unsafe { input_array_pointer.add(INPUT_LEN * normal_chunk_size * t) as usize };

        let output_cast_pointer =
            unsafe { output_array_pointer.add(OUTPUT_LEN_512 * normal_chunk_size * t) as usize };

        // The last thread reads a bit farther.
        if t == n_threads - 1 {
            chunk_size = last_chunk_size;
        }
        // Spawn threads, uncast the raw pointers insides.
        let handle = thread::spawn(move || {
            // Raw sequential operates on ~ n_values / n_threads contiguous lines as a standalone array
            raw_sequential_512(
                input_cast_pointer as *const u8,
                output_cast_pointer as *mut u8,
                chunk_size,
            )
        });

        // Keep track of the spawned threads.
        handles.push(handle)
    }
    // Wait for all the threads to terminate.
    for handle in handles {
        handle.join().unwrap();
    }
}

/// Entry points for Python foreign function call.
#[no_mangle]
pub unsafe extern "C" fn run_raw_hash(
    input_array_pointer: *const u8,
    output_array_pointer: *mut u8,
    n_values: usize,
) {
    raw_sequential(input_array_pointer, output_array_pointer, n_values);
}

#[no_mangle]
pub unsafe extern "C" fn run_raw_parallel_hash(
    input_array_pointer: *const u8,
    output_array_pointer: *mut u8,
    n_values: usize,
    n_threads: usize,
) {
    raw_share_memory(
        input_array_pointer,
        output_array_pointer,
        n_values,
        n_threads,
    );
}

#[no_mangle]
pub unsafe extern "C" fn run_raw_hash_512(
    input_array_pointer: *const u8,
    output_array_pointer: *mut u8,
    n_values: usize,
) {
    raw_sequential_512(input_array_pointer, output_array_pointer, n_values);
}

#[no_mangle]
pub unsafe extern "C" fn run_raw_parallel_hash_512(
    input_array_pointer: *const u8,
    output_array_pointer: *mut u8,
    n_values: usize,
    n_threads: usize,
) {
    raw_share_memory_512(
        input_array_pointer,
        output_array_pointer,
        n_values,
        n_threads,
    );
}
