# coding=utf-8
#!/usr/bin/env python

from setuptools import setup, find_packages
import tdprofile
import os

def read(*names):
    values = dict()
    extensions = ['.md', '.txt']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(
    name='tdprofile',
    version=tdprofile.__version__,
    description='Teradata Profile / Account Management',
    long_description=long_description,
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Documentation",
    ],
    keywords='teradata account profile command console windows',
    author='Zhong Dai',
    author_email='zhongdai.au@gmail.com',
    maintainer='Zhong Dai',
    maintainer_email='zhongdai.au@gmail.com',
    url='https://github.com/zhongdai/tdprofile',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tdprofile = tdprofile.tdprofile:command_line_runner',
            'addtdprofile = tdprofile.tdprofile:command_line_add_profile'
        ]
    },
    install_requires=[
        'pyodbc'
    ],
)
