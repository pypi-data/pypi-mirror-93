"""Setup for the isolator."""

from setuptools import setup

version = "0.1.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="isolator",
    version=version,
    url="https://github.com/neuneck/isolator",
    license="mit",
    description="Isolate a python class into a separate process",
    long_description=long_description,
    packages=["isolator"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6',
)
