# -*- coding:utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Eric-Tools",
    version="1.1.0",
    author="Eric",
    author_email="799050481@qq.com",
    description="Python Daily Development Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eric-jxl/Tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7.16',
)
