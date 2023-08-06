#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Mark
# Mail: 1782980833@qq.com
# Created Time:  2020-3-29 16:00:00
#############################################

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="MarkExcel",  # 这里是pip项目发布的名称
    version="1.0.4",  # 版本号，数值大的会优先被pip
    keywords=("MarkExcel", "mark"),
    description="工具类整理",
    long_description="http://markdoc.handsomemark.com/project-3/doc-21/",
    license="MIT Licence",
    url="https://gitee.com/medincmedinc/mark_excel",  # 项目相关文件地址，一般是github
    author="Mark",
    author_email="1782980833@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["openpyxl", "et-xmlfile", "jdcal","flask","xlrd","xlwt"]  # 这个项目需要的第三方库
)
