from setuptools import dist
from setuptools import find_packages

dist.Distribution().fetch_build_eggs(["numpy>=1.19"])

import os
import re
import sys
import platform
import subprocess

from distutils.core import setup, Extension
from distutils.version import LooseVersion
import numpy


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_version():
    version_file = read("version.py")
    version_re = r"__version__ = \"(?P<version>.+)\""
    version = re.match(version_re, version_file).group("version")
    return version


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
    packages=find_packages(include=["shaloop", "shaloop.*"]),
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    setup_requires=required,
    zip_safe=False,
)
