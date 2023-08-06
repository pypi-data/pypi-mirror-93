#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: zxj
# Created Time:  2021-1-29
#############################################


from setuptools import setup, find_packages

setup(
    name = "lh_clean_tool",
    version = "0.1.0",
    description = "clean universial code tool",
    long_description = "for data clean,add clean universial code",
    license = "MIT Licence",
    url = "https://github.com/jiaozhusos/LhClean.git",
    author = "zxj",
    author_email = "zhaoxuejiaotyut@126.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)