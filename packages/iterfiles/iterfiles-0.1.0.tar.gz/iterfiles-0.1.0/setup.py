#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup(
    author="Alexander Lukanin",
    author_email='alexander.lukanin.13@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Find and process files in a Pythonic way, without boilerplate code.",
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['file', 'pattern', 'directory', 'tree', 'traverse', 'find', 'convert'],
    name='iterfiles',
    packages=find_packages(include=['iterfiles', 'iterfiles.*']),
    test_suite='tests',
    url='https://github.com/alexanderlukanin13/iterfiles',
    version='0.1.0',
    zip_safe=True,
)
