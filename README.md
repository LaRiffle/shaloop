# Shaloop 🚣‍

Rust optimization to run SHA256 over Numpy arrays.

## Installation

```bash
pip install shalooprust
```

## Development instructions

### Build, install and test locally

Activate a new virtual env, install Maturin and a Rust toolchain. Run:

```bash
maturin develop --release -b cffi
```

The Python package is now installed. Note: clean your PYTHONPATH to remove the package if necessary.

### Test and benchmark

```bash
python test/test_shaloop.py
```

```bash
python test/test_shaloop_512.py
```

If you have the old C version of Shaloop installed, you can run a benchmark with:

```bash 
python test/benchmark.py
```

### Build and publish 

```bash
docker run --rm -v $(pwd):/io konstin2/maturin publish -b cffi --manylinux 2010 -u __token__ -p pypi-your-token
```
