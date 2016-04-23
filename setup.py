#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scan',
    version='0.03',
    description='Simple 3D scanner',
    long_description=''.join(open('README.md').readlines()),
    keywords='3dscanner',
    author='Jan Copak',
    author_email='jan.copak@soukroma.cz',
    license='MIT',
    url='https://github.com/octopusengine/simple3dscanner',
    packages=[p for p in find_packages() if p != 'test'],
    package_data={'scan': ['templates/*']},
    install_requires=['jinja2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'       
        ]
)
