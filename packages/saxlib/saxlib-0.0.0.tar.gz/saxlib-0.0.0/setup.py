# imports
import sys
import warnings
import setuptools
import subprocess

import saxlib

setuptools.setup(
    name=saxlib.__name__,
    version=saxlib.__version__,
    description=saxlib.__doc__,
    long_description=open("README.md").read(),
    author=saxlib.__author__,
    author_email="floris.laporte@gmail.com",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "saxlib.wg_straight": ["weights/*.json"],
        "saxlib.dc_straight": ["weights/*.json"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License"
    ],
)
