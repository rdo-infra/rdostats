#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='rdostats',
    version='1',
    description='A tool for generating bugzilla statistics',
    author='Lars Kellogg-Stedman',
    author_email='lars@redhat.com',
    url='http://github.com/larsks/rdostats',
    install_requires=open('requirements.txt').readlines(),
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'rdostats=rdostats.main:main',
        ],
        'rdostats': [
            'generate=rdostats.commands.generate:Generate',
            'fetch=rdostats.commands.fetch:Fetch',
            'diff=rdostats.commands.diff:Diff',
        ],
    }
)
