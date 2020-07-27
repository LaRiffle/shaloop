# Shaloop 🚣‍

Rust optimization to run SHA256 over Numpy arrays.

## Development

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

If you have the old C version of Shaloop installed, you can run a benchmark with:

```bash 
python test/benchmark.py
```

### Deploy 

Build for release:

```bash
docker run --rm -v $(pwd):/io konstin2/maturin build --release -b cffi --manylinux 2014
```

docker run --rm -v $(pwd):/io konstin2/maturin build --release -b cffi --manylinux 2014 -o dist

If raises an error about some file not found:

```
docker run --rm -v $(pwd):/io konstin2/maturin build --release -b cffi --manylinux 2014 --no-sdist
```

Set .pypirc

delete tar.gz (some issue)

python3 -m twine upload --repository testpypi target/wheels/*


- [ ] Numpy and CFFI dependencies.


- [ ] Optimized Rustc compilation parameters.
- [ ] Mac?