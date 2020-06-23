import numpy as np
import matplotlib.pyplot as plt
import sha_loop
import math
import time


dt1 = np.dtype((np.uint64, [("uint8", np.uint8, 8)]))


def consume(buffer, nbits):
    new_buffer = buffer >> nbits
    extracted = buffer - (new_buffer << nbits)
    return new_buffer, extracted


def randbit(shape):
    assert len(shape) == 3
    byte_dim = shape[-2]
    shape_with_bytes = shape[:-2] + (math.ceil(byte_dim / 64), shape[-1])
    randvalues = np.random.randint(0, 2 ** 64, size=shape_with_bytes, dtype=np.uint64)
    randvalues[:, 0] = randvalues[:, 0] % 2 ** (byte_dim % 64)
    return randvalues


import cProfile


def test_shaloop():

    pr = cProfile.Profile()
    pr.enable()

    λ = 80
    n_values = 100_000
    x = randbit((2, λ, n_values))[0]
    # x = np.array([[                  16,                   13   ,                62],
    #  [16684085919135629008 , 3766798809093621433, 16281706966231673308]], dtype=np.uint64)
    # print(x)
    t = time.time()
    x = x.T
    x2 = x.view(dtype=dt1)
    x = x2["uint8"].reshape(*x.shape[:-1], -1)
    assert x.shape == (n_values, 2 * 8)

    # print(x)
    out = np.zeros((n_values, 32), dtype=np.uint8)
    out = sha_loop.sha256_loop_func(x, out)
    buffer = out.view(np.uint64).T

    buffer0, part0 = consume(buffer[0], λ - 64)
    part1 = buffer[1]
    part2 = buffer0 % 2
    buffer2, part3 = consume(buffer[2], λ - 64)
    part4 = buffer[3]
    part5 = buffer2 % 2

    valuebits = np.stack([part0, part1, part2, part3, part4, part5], axis=1)

    # print(valuebits.T)

    out = np.zeros((n_values, 32), dtype=np.uint8)
    out = sha_loop.sha256_loop_func(x, out)
    buffer = out.view(np.uint64).T

    buffer0, part0 = consume(buffer[0], λ - 64)
    part1 = buffer[1]
    part2 = buffer0 % 2
    buffer2, part3 = consume(buffer[2], λ - 64)
    part4 = buffer[3]
    part5 = buffer2 % 2

    valuebits = np.stack([part0, part1, part2, part3, part4, part5], axis=1)

    # print(valuebits.T)

    print(time.time() - t)

    # pr.print_stats()
