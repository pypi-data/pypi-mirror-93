# -*- encoding: UTF-8 -*-

from setuptools import setup
import direx

setup(
    name="dirEx",
    version=direx.__version__,
    author="Floyda",
    author_email="floyda@163.com",
    license="MIT",
    description="An extension to the built-in function dir()",
    long_description=open("readme.md").read(),
    keywords="dir extend built-in",
    url="https://github.com/floydawong/dirEx.git",
    packages=["direx"],
)
