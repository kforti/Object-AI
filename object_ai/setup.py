#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages


setup(
    author="Kevin Fortier",
    author_email='kevin.r.fortier@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="",
    entry_points={
        'console_scripts': [

        ],
    },
    include_package_data=True,
    keywords='object_ai',
    name='object_ai',
    packages=find_packages(include=['object_ai', 'object_ai.*']),
    test_suite='tests',
    zip_safe=False,
)