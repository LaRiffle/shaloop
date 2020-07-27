import shalooprust as shaloop
import numpy as np
import os
import time


def test_raw_rust(n_values):
    np.random.seed(n_values)
    i = np.random.randint(255, size=(n_values, 16)).astype("uint8")
    o = np.zeros((n_values, 32), dtype=np.uint8)
    t = time.time()
    shaloop.sha256_loop_func_sequential(i, o)
    print(f"Sequential Rust time: {time.time() - t} s.")
    return o


def test_raw_parallel_rust(n_values, n_threads):
    np.random.seed(n_values)
    i = np.random.randint(255, size=(n_values, 16)).astype("uint8")
    o = np.zeros((n_values, 32), dtype=np.uint8)
    t = time.time()
    shaloop.sha256_loop_func(i, o, n_threads)
    print(f"Parallel Rust time with {n_threads} threads: {time.time() - t} s.")
    return o


if __name__ == "__main__":

    for n_values in [1, 10, 1_0003, 100_999]:
        print(f"Testing {n_values} values, comparing to C-generated ground truth.")
        ground_truth = np.loadtxt(
            os.path.join(os.path.dirname(__file__), f"groundtruth-{n_values}.csv"),
            delimiter=",",
        )
        assert (test_raw_parallel_rust(n_values, 8) == ground_truth).all()
        assert (test_raw_rust(n_values) == ground_truth).all()
    print("Success.")
