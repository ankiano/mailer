#!/usr/bin/env python3.10
# coding=utf-8

from setuptools import setup, find_packages
from pathlib import Path
from pkg_resources import parse_requirements

with Path('requirements.txt').open() as requirements_txt:
    requirements = [
        str(requirement) for requirement in parse_requirements(requirements_txt)
    ]

setup(
    name='mailer',
    version='1.0.4',
    description='CLI tool for sending emails',
    long_description='',
    py_modules=['mailer'],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='mailer',
    entry_points={'console_scripts': ['mailer=mailer:cli']},
)
