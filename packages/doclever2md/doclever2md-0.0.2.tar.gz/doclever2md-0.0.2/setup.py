#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: skyleft
# Description: doclever导出的json转藏经阁风格markdown

from setuptools import setup, find_packages

setup(
    name='doclever2md',
    version='0.0.2',
    keywords='doclever,markdown',
    description='a tool which can convert doclever json to cangjingge style markdown',
    license='MIT License',
    url='https://andy-cheung.me',
    author='skyleft',
    author_email='skyleft123@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Jinja2>=2.11.2'
    ],
    entry_points={
        'console_scripts': [
            'doclever2md = doclever2md.main:main',
        ],
    },
)
