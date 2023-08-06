from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="libsm3",
    version="0.0.4",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
    ],
    rust_extensions=[RustExtension("libsm3")],
    include_package_data=True,
    zip_safe=False,
)
