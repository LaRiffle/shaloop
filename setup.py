from distutils.core import setup, Extension
import numpy
from Cython.Distutils import build_ext

setup(
    cmdclass={"build_ext": build_ext},
    ext_modules=[
        Extension(
            "sha_loop",
            sources=["src/_sha_loop.pyx", "src/sha_loop.c"],
            include_dirs=[numpy.get_include(), "/usr/include/openssl"],
            libraries=["ssl", "crypto"],
        )
    ],
)
