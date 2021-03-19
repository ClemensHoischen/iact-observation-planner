#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Clemens Hoischen",
    author_email="ClemensHoischen@gmail.com",
    python_requires=">=3.5",
    description="observation planner tool for iacts",
    entry_points={
        "console_scripts": [
            "iact-observation-planner=iact_observation_planner.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="iact_observation_planner",
    name="iact_observation_planner",
    packages=find_packages(
        include=["iact_observation_planner", "iact_observation_planner.*"]
    ),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ClemensHoischen/iact_observation_planner",
    version="0.0.1",
    zip_safe=False,
)
