#!/usr/bin/env python

"""Tests for `iact_observation_planner` package."""
import os
import subprocess as sp

from datetime import datetime, timedelta

import pytest

from astropy.coordinates import EarthLocation, SkyCoord

from iact_observation_planner import iact_observation_planner
from iact_observation_planner import observer_config
from iact_observation_planner import targets as iop_targets
from iact_observation_planner import nights


default_sites = ["HESS", "MAGIC"]
default_darkness = ["dark", "gray", "bright"]
default_dates = ["2021-01-01", None, datetime.utcnow()]
default_ranges = [1, 2, 10]


def test_deploy_config(tmp_path):
    site_cfg = "site_config.json"
    command = "iop-init"

    call = sp.run([command, "--init", str(tmp_path)], stdout=sp.PIPE)

    dest_file = "{}".format(str(tmp_path) + "/" + site_cfg)
    assert "GENERATED DEFAULT CONFIG ->" and dest_file in call.stdout.decode("utf-8")
    assert os.path.isfile(dest_file)


@pytest.mark.parametrize("site", default_sites)
@pytest.mark.parametrize("dark", default_darkness)
def test_cfg_data(site, dark):
    site_cfg = observer_config.default_observer_config()

    cfg = observer_config.ObserverConfiguration(site_cfg)
    site = cfg.get_site_from_name(site)
    darkness = cfg.get_darkness_from_name(dark)
    run_dur, wobble = cfg.get_observation_pars()
    assert cfg
    assert site
    assert darkness
    assert run_dur
    assert wobble


@pytest.mark.parametrize(
    "date,expected",
    [
        ("2021-01-01", datetime(2021, 1, 1)),
        (
            None,
            datetime(
                datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day
            ),
        ),
    ],
)
def test_option_parsing_date(date, expected):
    print(date)
    parsed_date_dict = iact_observation_planner.parse_date(date)
    print(parsed_date_dict)
    assert parsed_date_dict == {"date": expected}


@pytest.mark.parametrize("test_range,expected", [(1, timedelta(days=1))])
def test_option_parsing_range(test_range, expected):
    print(test_range)
    parsed_dict = iact_observation_planner.parse_range(test_range)
    print(parsed_dict)
    assert parsed_dict == {"range": expected}


@pytest.mark.parametrize("test_site", default_sites)
def test_option_parsing_site(test_site):
    site = iact_observation_planner.parse_site(test_site)
    assert isinstance(site["site"], EarthLocation)


@pytest.mark.parametrize("test_dark", default_darkness)
def test_option_parsing_darkness(test_dark):
    parsed_dict = iact_observation_planner.parse_darkness(test_dark)
    assert parsed_dict


@pytest.mark.parametrize("test_date", default_dates)
@pytest.mark.parametrize("test_range", default_ranges)
@pytest.mark.parametrize("test_dark", default_darkness)
@pytest.mark.parametrize("test_site", default_sites)
def test_parse_all_opts(test_site, test_dark, test_date, test_range):
    parsed_opts = iact_observation_planner.parse_options(
        test_site, test_dark, test_date, test_range
    )
    assert parsed_opts


@pytest.mark.parametrize(
    "targets",
    [
        ["PKS1510-089"],
        ["PKS2155-304;55;10"],
        ["Crab Nebula;30;2", "Vela Pulsar;25;4"],
        ["rd/123.3d,-23.5d/my_target;15;8"],
        ["rd/55.2351d,85.1d/my_other_target"],
    ],
)
def test_resolve_targets(targets):
    parsed_targets = iop_targets.resolve_target_list(targets)
    assert len(parsed_targets) == len(targets)
    for p_targ in parsed_targets:
        assert isinstance(p_targ.coords, SkyCoord)


@pytest.mark.parametrize("test_range", [timedelta(days=r) for r in default_ranges])
@pytest.mark.parametrize("date", [datetime(2021, 3, 24)])
def test_night(date, test_range):
    site = iact_observation_planner.parse_site("HESS")["site"]
    dark = iact_observation_planner.parse_darkness("dark")["darkness"]
    parsed_nights = nights.setup_nights(date, site, dark, test_range)
    for night in parsed_nights:
        assert isinstance(night, type(nights.Night(datetime.utcnow(), site, dark)))


@pytest.mark.parametrize("test_dark", default_darkness)
@pytest.mark.parametrize("test_site", default_sites)
@pytest.mark.parametrize("date", [datetime(2021, 3, 24)])
def test_sunrise_sunset(date, test_site, test_dark):
    site = iact_observation_planner.parse_site(test_site)["site"]
    dark = iact_observation_planner.parse_darkness(test_dark)["darkness"]

    sun_set, sun_rise = nights.find_sun_rise_and_set(date, site, dark)
    assert sun_set < sun_rise


@pytest.mark.parametrize("test_targets", [["PKS 2155-304"]])
@pytest.mark.parametrize("test_range", [timedelta(days=r) for r in default_ranges])
@pytest.mark.parametrize("date", [datetime(2021, 3, 24)])
@pytest.mark.parametrize("test_dark", default_darkness)
@pytest.mark.parametrize("test_site", default_sites)
def test_plan_target(test_targets, date, test_site, test_dark, test_range):
    targets = iop_targets.resolve_target_list(test_targets)
    dark = iact_observation_planner.parse_darkness(test_dark)["darkness"]
    site = iact_observation_planner.parse_site(test_site)["site"]
    parsed_nights = nights.setup_nights(date, site, dark, test_range)

    for night in parsed_nights:
        for target in targets:
            night.plan_target(target)


@pytest.mark.parametrize(
    "test_args",
    [
        [
            '--target "M87;30;5" "Crab Nebula;25;1"',
            "-d 2021-01-15",
            "-r 1",
            "-o dark",
            "-s HESS",
        ]
    ],
)
def test_example_call(test_args):
    command = ["iact-observation-planner"]
    for arg in test_args:
        command.append(arg)

    comm = " ".join(command)

    call = sp.run(comm, stdout=sp.PIPE, shell=True, universal_newlines=True)
    print(call.stdout)
    assert "Planning the following targets:" in call.stdout
