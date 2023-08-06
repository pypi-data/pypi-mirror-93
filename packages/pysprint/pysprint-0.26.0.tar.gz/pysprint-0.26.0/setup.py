import os
import sys
import versioneer


if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")


from setuptools import setup, find_packages
from setuptools.command.sdist import sdist as SdistCommand


with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    from setuptools_rust import RustExtension, Binding
except ImportError:
    import subprocess

    errno = subprocess.call([sys.executable, "-m", "pip", "install", "setuptools-rust"])
    if errno:
        print("Please install setuptools-rust package")
        raise SystemExit(errno)
    else:
        from setuptools_rust import RustExtension, Binding

setup(
    name="pysprint",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Péter Leéh",
    author_email="leeh123peter@gmail.com",
    description="Spectrally refined interferometry for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ptrskay3/PySprint",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Rust",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=["numpy>=1.16.6", "scipy", "matplotlib", "pandas", "Jinja2", "scikit-learn"],
    setup_requires=["setuptools-rust>=0.10.1", "wheel"],
    extras_require={"optional": ["numba", "lmfit", "pytest", "dask"]},
    rust_extensions=[
        RustExtension("pysprint.numerics", "Cargo.toml", debug=False, binding=Binding.PyO3),
        ],
    entry_points={
        'console_scripts': [
            'pysprint = pysprint.templates.build:main',
        ],
    },
    zip_safe=False,
)
