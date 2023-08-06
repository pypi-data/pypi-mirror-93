#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'networkx', 'tsplib95', 'numpy', 'matplotlib', 'pandas', 'acopy']

setup_requirements = []

test_requirements = []

setup(
    author="ganariya",
    author_email='ganariya2525@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="kiacopy can make k-independent traveling salesman problem",
    entry_points={
        'console_scripts': [
            'kiacopy=kiacopy.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='kiacopy',
    name='kiacopy',
    packages=find_packages(include=['kiacopy', 'kiacopy.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ganariya/kiacopy',
    version='0.3.7',
    zip_safe=False,
)
