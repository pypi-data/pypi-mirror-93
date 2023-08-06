from setuptools import setup
from setuptools import find_packages

with open("LICENSE", "r") as f:
    license = f.readline()

setup(
    name="sRemo",
    version="1.0.0",
    author="zunda(@zunda_pixel)",
    author_email="zunda.pixel@gmail.com",
    description="Python client for sRemo(sCloud) API",
    url="https://github.com/zunda-pixel/sRemo",
    license="MIT",
    packages=find_packages(exclude="sRemo")
)
