# -*- coding: utf-8 -*-
"""
@Project ：MyTools
@File    ：setup.py.py
@IDE     ：PyCharm
@Author  ：Cheng Xiaozhao
@Date    ：
@Desc    ：
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="worktools",
    version="0.0.2",
    author="Cheng Xiaozhao",
    author_email="867616144@qq.com",
    description="Some common tools for the convenience of work and study",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cxz13797090526/MyTools/tree/feature",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
