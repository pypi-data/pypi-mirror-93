# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

import setuptools  # type: ignore
from setuptools import setup, find_namespace_packages

metadata: dict = {}
with open("_metadata.py") as fp:
    exec(fp.read(), metadata)

setup(
    name=metadata["__extension_name__"],
    version=metadata["__extension_version__"],
    author="Alexander Cowtan",
    author_email="alexander.cowtan@cambridgequantum.com",
    python_requires=">=3.6",
    url="https://github.com/CQCL/pytket",
    description="Extension for pytket, providing translation to and from the PyZX framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="CQC Software Licence",
    packages=find_namespace_packages(include=["pytket.*"]),
    include_package_data=True,
    install_requires=["pytket ~= 0.7", "pyzx ~= 0.6.3"],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: Other/Proprietary License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    zip_safe=False,
)
