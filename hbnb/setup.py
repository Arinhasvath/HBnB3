#!/usr/bin/python3

"""
Setup configuration for HBnB package.
Handles package dependencies and installation settings.
"""

from setuptools import setup, find_packages

setup(
    name="hbnb",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-restx',
    ],
)
