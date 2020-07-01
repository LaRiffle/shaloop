from setuptools import dist

dist.Distribution().fetch_build_eggs(["Cython>=0.29", "numpy>=1.19"])

import os
import re
import sys
import platform
import subprocess

from distutils.core import setup, Extension
from distutils.version import LooseVersion
import numpy
from Cython.Distutils import build_ext


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_version():
    version_file = read("version.py")
    version_re = r"__version__ = \"(?P<version>.+)\""
    version = re.match(version_re, version_file).group("version")
    return version


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r"version\s*([\d.]+)", out.decode()).group(1))
            if cmake_version < "3.1.0":
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += [f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}"]
            if sys.maxsize > 2 ** 32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=self.build_temp)


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="shaloop",
    version=find_version(),
    author="Théo Ryffel",
    author_email="theo@arkhn.com",
    description="Faster crypto loops on numpy arrays",
    license="Apache-2.0",
    keywords="function secret sharing sha256 sha512 numpy array",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/LaRiffle/shaloop",
    # packages=setuptools.find_packages(include=["src", "src.*"]),
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    setup_requires=required,
    cmdclass={"build_ext": build_ext},
    ext_modules=[
        Extension(
            "sha_loop",
            sources=["src/_sha_loop.pyx", "src/sha_loop.c"],
            include_dirs=[numpy.get_include(), "/usr/include/openssl"],
            libraries=["ssl", "crypto"],
        )
    ],
    zip_safe=False,
)
