# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 16:00
# @Author  : Haijun


import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="HjGoogleSearch",
    version='1.0.3',
    author='navy',
    auther_email='haijun0422@gmail.com',
    description='search google by image and key words',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    install_requires=["requests", "aiohttp", "iso8601", "dynaconf", "aiostream", "redis", "loguru"],
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
)
