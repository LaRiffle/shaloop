import shaloop
import numpy as np
import time


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


if __name__ == "__main__":

    # TODO: add some sweet asserts.
