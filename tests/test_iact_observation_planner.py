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


def test_deploy_config(tmp_path):
    site_cfg = "site_config.json"
    command = "iop-init"

    call = sp.run([command, "--init", str(tmp_path)], stdout=sp.PIPE)

    dest_file = "{}".format(str(tmp_path) + "/" + site_cfg)
    assert "GENERATED DEFAULT CONFIG ->" and dest_file in call.stdout.decode("utf-8")
    assert os.path.isfile(dest_file)


@pytest.mark.parametrize("site", ["HESS", "MAGIC"])
@pytest.mark.parametrize("dark", ["dark", "gray", "bright"])
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


@pytest.mark.parametrize("test_site", ["MAGIC", "HESS"])
def test_option_parsing_site(test_site):
    site = iact_observation_planner.parse_site(test_site)
    assert isinstance(site["site"], EarthLocation)


@pytest.mark.parametrize(
    "targets",
    [
        ["PKS1510-089"],
        ["PKS2155-304;55;10"],
        ["Crab Nebula;30;2", "Vela Pulsar;25;4"],
        ["rd/123.3d,-23.5d/my_target;15;8"],
        ["rd/55.2351d,85.1d/my_other_target"],
    ],)
def test_resolve_targets(targets):
    parsed_targets = iop_targets.resolve_target_list(targets)
    assert len(parsed_targets) == len(targets)
    for p_targ in parsed_targets:
        assert isinstance(p_targ.coords, SkyCoord)


"""
@pytest.mark.now
@pytest.mark.parametrize(
    "targets",
    [
        ["Crab Nebula;30;2", "Vela Pulsar;25;4"],
        ["PKS2155-304;55;10"],
        ["PKS1510-089"],
        ["rd/123.3d,-23.5d/my_target;15;8"],
        ["rd/55.2351d,85.1d/my_other_target"],
    ],
)
@pytest.mark.parametrize("darkness", [None, "dark", "gray", "bright"])
def test_main_script_options(targets, darkness):
    command = "iact-observation-planner"
    opts = "--target"
    for target in targets:
        opts += " {} ".format(target)

    if darkness:
        opts += " -o {}".format(darkness)

    call = sp.run([command, opts], stdout=sp.PIPE)
"""