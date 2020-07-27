import shalooprust as shaloop
import numpy as np
import time

# C version for benchmarking purposes
import sha_loop


def test_raw_rust(n_values):
    np.random.seed(n_values)
    i = np.random.randint(255, size=(n_values, 16)).astype("uint8")
    o = np.zeros((n_values, 32), dtype=np.uint8)

    # print(f"Input array:\n {i}")
    # print(f"Initial output array:\n {o}")

    t = time.time()
    shaloop.sha256_loop_func_sequential(i, o)
    print(f"Raw Rust time {time.time() - t}")

    # print(f"Output array after computation:\n {o}")
    return o


def test_raw_parallel_rust(n_values, n_threads):
    np.random.seed(n_values)
    i = np.random.randint(255, size=(n_values, 16)).astype("uint8")
    o = np.zeros((n_values, 32), dtype=np.uint8)

    # print(f"Input array:\n {i}")
    # print(f"Initial output array:\n {o}")

    t = time.time()
    shaloop.sha256_loop_func(i, o, n_threads)
    print(f"Raw parallel Rust with {n_threads} threads: time {time.time() - t}.")

    # print(f"Output array after computation:\n {o}")
    return o


def test_c(n_values):
    np.random.seed(n_values)
    i = np.random.randint(255, size=(n_values, 16)).astype("uint8")
    o = np.zeros((n_values, 32), dtype=np.uint8)

    # print(f"Input array:\n {i}")
    # print(f"Initial output array:\n {o}")

    t = time.time()
    o = sha_loop.sha256_loop_func(i, o)
    print(f"Sequential C time {time.time() - t}")

    # print(f"Output array after computation:\n {o}")
    return o


def save_c(n_values):
    o = test_c(n_values)
    np.savetxt(f"groundtruth-{n_values}.csv", o, delimiter=",", fmt="%03u")


if __name__ == "__main__":

    for n_values in [1, 10, 1_000, 100_000, 1_000_000, 10_000_000, 100_000_000]:
        print(f"Comparing speed for {n_values} values.")
        test_raw_rust(n_values)
        test_raw_parallel_rust(n_values, 4)
        test_raw_parallel_rust(n_values, 8)
        test_c(n_values)
        print()
