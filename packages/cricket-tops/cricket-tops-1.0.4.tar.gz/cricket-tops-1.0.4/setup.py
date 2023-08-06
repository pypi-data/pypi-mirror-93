# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 22:40:18 2021

@author: Arghya Tarafdar
"""

from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="cricket-tops",
    version="1.0.4",
    description="A Python package to view the top ODI, Tests, T20 ranked players (men and women) as well as Top Tests, ODI and T20 ranked teams.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Arghya Tarafdar",
    author_email="arghya.tarafdar86@yahoo.co.in",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["cricket_tops"],
    include_package_data=True,
    install_requires=["pandas"],
    
)
