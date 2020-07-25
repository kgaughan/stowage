#!/usr/bin/env python3

from setuptools import setup


setup(
    name="stowage",
    version="1.0.0",
    description="A standalone GNU Stow alike",
    long_description=open("README.rst").read(),
    author="Keith Gaughan",
    author_email="keith+stowage@gaughan.ie",
    url="https://github.com/kgaughan/stowage",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
    ],
    scripts=["stowage"],
)
