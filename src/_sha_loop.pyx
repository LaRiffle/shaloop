""" Example of wrapping a C function that takes C double arrays as input using
    the Numpy declarations from Cython """

# cimport the Cython declarations for numpy
cimport numpy as np

# if you want to use the Numpy-C-API from Cython
# (not strictly necessary for this example, but good practice)
np.import_array()

# cdefine the signature of our c function
cdef extern from "sha_loop.h":
    void sha256_loop(unsigned char * buffer, int n_values, unsigned char * out)
    void sha512_loop(unsigned char * buffer, int n_values, unsigned char * out)


def sha256_loop_func(np.ndarray[unsigned char, ndim=2, mode="c"] in_array not None, np.ndarray[unsigned char, ndim=2, mode="c"] out not None):
    n_values = in_array.shape[0]
    n_char = in_array.shape[1]

    sha256_loop(
        <unsigned char*> in_array.data,
        n_values,
        <unsigned char*> out.data,
    )

    return out


def sha512_loop_func(np.ndarray[unsigned char, ndim=2, mode="c"] in_array not None, np.ndarray[unsigned char, ndim=2, mode="c"] out not None):
    n_values = in_array.shape[0]
    n_char = in_array.shape[1]

    sha512_loop(
        <unsigned char*> in_array.data,
        n_values,
        <unsigned char*> out.data,
    )

    return out

