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


# For benchmarking
# def test_c(n_values):
#     np.random.seed(n_values)
#     i = np.random.randint(255, size=(n_values, 16)).astype("uint8")
#     o = np.zeros((n_values, 32), dtype=np.uint8)

#     # print(f"Input array:\n {i}")
#     # print(f"Initial output array:\n {o}")

#     t = time.time()
#     o = sha_loop.sha256_loop_func(i, o)
#     print(f"Sequential C time {time.time() - t}")

#     # print(f"Output array after computation:\n {o}")
#     return o


if __name__ == "__main__":

    # assert (test_raw_rust(8) == test_raw_parallel_rust(8, 1)).all()

    for n_values in [1, 10, 1_000, 100_000, 1_000_000, 10_000_000, 100_000_000]:
        print(f"n_values {n_values}")
        test_raw_rust(n_values)
        test_raw_parallel_rust(n_values, 4)
        test_raw_parallel_rust(n_values, 8)
        # assert (test_c(n_values) == test_raw_parallel_rust(n_values, 6)).all()
        print()

