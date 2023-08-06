#coding:utf-8

from os import path
from codecs import open
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pynacos-sdk",
    version="0.4.0",
    author="olivetree",
    license="MIT",
    packages=["nacos"],
    author_email="olivetree123@163.com",
    url="https://github.com/olivetree123/pynacos-sdk",
    description="Nacos sdk for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "winney>=0.5.0",
    ],
)
