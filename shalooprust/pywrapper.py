# Calling the Rust library through Maturin
from .shalooprust import ffi, lib

rust_run_raw_hash = lib.run_raw_hash
rust_run_raw_parallel_hash = lib.run_raw_parallel_hash

# import os
# from .ffi import ffi

# lib = ffi.dlopen(os.path.join(os.path.dirname(__file__), "native.so"), 4098)
# del os


import numpy as np

# Utils to convert numpy arrays
def _as_usize(np_int):
    return ffi.cast("unsigned long", np_int)


def _as_u8_array(np_u8_array):
    # return ffi.cast("unsigned  char *", np_u8_array.ctypes.data)
    return ffi.cast("uint8_t *", np_u8_array.ctypes.data)


def sha256_loop_func_sequential(np_input_array, np_output_array):
    # Convert types
    rust_input_array = _as_u8_array(np_input_array)
    rust_output_array = _as_u8_array(np_output_array)
    rust_n_values = _as_usize(np_input_array.shape[0])

    # Call rust
    rust_run_raw_hash(
        rust_input_array, rust_output_array, rust_n_values,
    )
    return


# TODO: decide where to fix thread parameters.
def sha256_loop_func(np_input_array, np_output_array, np_n_threads=4):
    # Convert types
    rust_input_array = _as_u8_array(np_input_array)
    rust_output_array = _as_u8_array(np_output_array)
    rust_n_values = _as_usize(np_input_array.shape[0])
    rust_n_threads = _as_usize(np_n_threads)

    # Call rust
    rust_run_raw_parallel_hash(
        rust_input_array, rust_output_array, rust_n_values, rust_n_threads
    )
    return
