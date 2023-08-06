from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="gaction-lib",  # package name
    version="0.1a2",  # version
    description="[TODO]: Fill your description here",
    author="gawainx",
    author_email="liangyixp@live.cn",
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
    ],
    scripts=[],
    packages=setuptools.find_packages(),
)
