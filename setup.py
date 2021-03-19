#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Clemens Hoischen",
    author_email='ClemensHoischen@gmail.com',
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
    description="observation planner tool for iacts",
    entry_points={
        'console_scripts': [
            'iact_observation_planner=iact_observation_planner.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='iact_observation_planner',
    name='iact_observation_planner',
    packages=find_packages(include=['iact_observation_planner', 'iact_observation_planner.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ClemensHoischen/iact_observation_planner',
    version='0.0.1',
    zip_safe=False,
)
