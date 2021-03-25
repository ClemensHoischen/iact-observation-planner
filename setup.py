#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["astropy==4.2", "ephem==3.7.7.0", "pandas==1.2.3", "matplotlib"]

setup_requirements = [
    "astropy",
]

test_requirements = ["pytest>=3", "pytest-cov>=2.11"]

setup(
    author="Clemens Hoischen",
    author_email="ClemensHoischen@gmail.com",
    python_requires=">=3.5",
    description="observation planner tool for iacts",
    entry_points={
        "console_scripts": [
            "iop-init=iact_observation_planner.iop_init:main",
            "iact-observation-planner=iact_observation_planner.iop:main",
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
