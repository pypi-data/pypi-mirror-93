#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages
import os

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

name = "electrochem"

here = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(here, name, "_version.py")) as f:
    exec(f.read(), {}, version_ns)

setup(
    author="Vincent Wu",
    author_email='vincentwu@ucsb.edu',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Reads raw electrochemical cycling data and generates useful plots and tables for battery scientists.",
    entry_points={
        'console_scripts': [
            'electrochem=electrochem.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='electrochem',
    name='electrochem',
    packages=find_packages(include=['electrochem', 'electrochem.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/vince-wu/electrochem',
    version= version_ns["__version__"],
    zip_safe=False,
)
