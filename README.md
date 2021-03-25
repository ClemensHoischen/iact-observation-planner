
[![test-suite](https://github.com/ClemensHoischen/iact-observation-planner/actions/workflows/github-pytest.yml/badge.svg?branch=main)](https://github.com/ClemensHoischen/iact-observation-planner/actions/workflows/github-pytest.yml)

![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/ClemensHoischen/2c51ac403e7cee714b127c1b33a1d8d1/raw/iact_observation_planner__heads_main.json)


# DISCLAIMER
**This package is not yet available on PyPI and is still in development.**
**Get in touch if you would like to help.**


# iact observation planner

This is a tool to quickly evaluate different constraints for planning observations with iacts. different sites, darkness conditions are supported. multiple targets with individual target hours and altitude limits are supported.

## Installation

`pip install iact-observation-planner`

## Configuring

If you want to use more specific configurations than given by the default, you can make use of the `iop-init <path>` command that comes with this package.

It will copy the default configuration to `<path>`. Applying an environemnt variable to your shell before using the iact-observation-planner will force the tool to read this config.

## Usage
just try `iact-observation-planner --help` for the details of all options.

Example command to plan:
- PKS 2155 with altitude > 50 deg for 2 hours
- Crab Nebula with altitude > 30 deg for 5 hours
- starting 2021-03-15
- for 3 nights
- using the 'gray'darkness definition
- on the HESS site

`iact-observation-planner  --target "PKS 2155-304;50;2" "Crab Nebula;30;5" -d 2021-03-15 -r 3 -o gray -s HESS`



## Acknowledgements

Parts of this project are based on the the [hessobs](https://github.com/kosack/hessobs) project by @kosack.
