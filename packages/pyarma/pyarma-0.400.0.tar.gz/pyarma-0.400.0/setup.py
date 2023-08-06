# Workaround for pre-PEP 518 (setuptools <43) users
try:
    from skbuild import setup
except ImportError:
    from setuptools import setup
try:
    from psutil import cpu_count, virtual_memory, WINDOWS
    psutil_found = True
except ImportError:
    psutil_found = False
import os

# Versioning information
# Only bump for stable releases or API breaks
major = ("PYARMA_VERSION_MAJOR", "0")

# Bump for functionality additions that DO NOT break past APIs
minor = ("PYARMA_VERSION_MINOR", "400")

# Bump for bugfixes that DO NOT break past APIs
patch = ("PYARMA_VERSION_PATCH", "0")

# Must pass this as a C++ string
name = ('PYARMA_VERSION_NAME', '"scout"')

# Check for CPU and memory
# If 8 GB or less memory is available, check for cores and use the physical cores
if psutil_found:
    if virtual_memory().available <= 8589934592:
        os.environ["CMAKE_BUILD_PARALLEL_LEVEL"] = str(cpu_count(logical=False))

# Arguments to pass to CMake
cmake_major = "-D" + major[0] + "=" + major[1]
cmake_minor = "-D" + minor[0] + "=" + minor[1]
cmake_patch = "-D" + patch[0] + "=" + patch[1]
cmake_name = "-D" + name[0] + "=" + name[1]
cmake_args = [cmake_major, cmake_minor, cmake_patch, cmake_name]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyarma",
    version=major[1]+"."+minor[1]+"."+patch[1],
    author="Jason Rumengan",
    author_email="jason.rumengan@connect.qut.edu.au",
    description="Linear algebra library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pyarma.sourceforge.io",
    packages=["pyarma"],
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research", 
        "Intended Audience :: Developers", 
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.0',
    keywords='linear algebra scientific computing pyarma pyarmadillo armadillo arma c++ pybind11 library',
    cmake_args=cmake_args,
    cmake_install_dir="src/pyarma",
    install_requires=["setuptools", "wheel", "scikit-build", "cmake", "ninja", "psutil"],
    setup_requires=["cmake"]
)