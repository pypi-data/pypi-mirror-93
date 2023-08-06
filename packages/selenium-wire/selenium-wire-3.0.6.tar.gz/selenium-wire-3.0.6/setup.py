#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    author="Will Keeling",
    author_email='will@zifferent.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Extends Selenium to give you the ability to inspect requests made by the browser.",
    install_requires=['selenium>=3.4.0'],
    license="MIT",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='selenium-wire',
    name='selenium-wire',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    setup_requires=[],
    test_suite='nose.collector',
    tests_require=['nose'],
    url='https://github.com/wkeeling/selenium-wire',
    version='3.0.6',
    zip_safe=False,
)
