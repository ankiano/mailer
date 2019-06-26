#!/usr/bin/env python3.6
# coding=utf-8

from pip._internal.req import parse_requirements
from pip._internal.download import PipSession

from setuptools import setup, find_packages

parsed_requirements = parse_requirements(
    'requirements.txt',
    session=PipSession()
)

requirements = [str(ir.req) for ir in parsed_requirements]

setup(
    name='mailer',
    version='0.0.2',
    description='CLI tool for sending emails',
    long_description='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='mailer',
    entry_points={'console_scripts': ['mailer=mailer:cli']},
)
