
[![test-suite](https://github.com/ClemensHoischen/iact-observation-planner/actions/workflows/github-pytest.yml/badge.svg?branch=main)](https://github.com/ClemensHoischen/iact-observation-planner/actions/workflows/github-pytest.yml)


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
- PKS 2155-304 with altitude > 50 deg for 2 hours
- Crab Nebula with altitude > 30 deg for 5 hours
- starting _2021-03-15_
- for _1_ nights
- using the _gray_ darkness definition
- on the _HESS_ site

`iact-observation-planner  --target "PKS 2155-304;50;2" "Crab Nebula;30;5" -d 2021-01-15 -r 1 -o dark -s HESS`

The resulting output is:

```
Planning the following targets:
PKS 2155-304    : 21h58m52.0652s -30d13m32.1207s - (ra = 329.72 deg = -30.23 deg)
                  Altitude > 50.0 deg
                  Target observation time = 2
Crab Nebula     : 05h34m31.94s +22d00m52.2s - (ra = 83.63 deg = 22.01 deg)
                  Altitude > 30.0 deg
                  Target observation time = 5
Boundry Conditions:
 * Site:       HESS
 * Darkness:   {'max_sun_altitude': '-16 deg', 'max_moon_altitude': '-0.5 deg', 'max_moon_phase': False, 'min_moon_distance': False}
 * Start Date: 2021-01-15
 * N nights:   1

Evening Date: 2021-01-15
 * Sun Set:  2021-01-15 19:00:42.902484
 * Sun Rise: 2021-01-16 03:08:22.424208

Target Crab Nebula:
 * observable from  2021-01-15T19:00:42
 * observable until 2021-01-15T23:27:49
```

## Acknowledgements

Parts of this project are based on the the [hessobs](https://github.com/kosack/hessobs) project by @kosack.
