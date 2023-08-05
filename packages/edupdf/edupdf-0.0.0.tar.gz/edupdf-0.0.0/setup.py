import setuptools
from pathlib import Path

setuptools.setup(
    name="edupdf",
    verison=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "test"]),
)