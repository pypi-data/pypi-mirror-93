#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="Text2JSON",
    version="0.1.9",
    author="Yucheng Zeng",
    author_email="yucheng-zeng@outlook.com",
    description="Text2JSON",
    long_description=open("README.md").read(),
    license="MIT",
    url="https://github.com/1173710105/Text2JSON",
    packages=find_packages(),
    install_requires=[
        "numpy",
        'transformers==2.5.1',
        'chinese2digits'
    ],
    python_requires='>=3',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
)
