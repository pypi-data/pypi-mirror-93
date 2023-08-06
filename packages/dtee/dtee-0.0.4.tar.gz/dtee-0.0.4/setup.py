#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 16:49
# @Author: SHAW
# @QQ:838705177
# -----------------------

# from distutils.core import setup
import os

from setuptools import find_packages,setup

basedir = os.path.dirname(__file__)

with open(os.path.join(basedir,"README.rst"), "r",encoding="utf-8") as f:
  long_description = f.read()

setup(name='dtee',
      version='0.0.4',
      description='Tornado tcp stream parser',
      long_description=long_description,
      author='lee_shaw',
      author_email='838705177@qq.com',
      install_requires=['tornado>=6.0.0'],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      keywords='dtee tornado',
      )