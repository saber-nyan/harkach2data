# -*- coding: utf-8 -*-
"""
Скрипт установки~
"""
from distutils.core import setup

from setuptools import find_packages

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='harkach2data',
    version='0.0.0.1',
    description='Утилиты сбора данных со 2ch.hk',
    long_description=readme,
    author='saber-nyan',
    author_email='saber-nyan@ya.ru',
    url='https://github.com/saber-nyan/harkach2data',
    license='WTFPL',
    install_requires=[
        'requests',
    ],
    packages=find_packages(),
    include_package_data=True
)
