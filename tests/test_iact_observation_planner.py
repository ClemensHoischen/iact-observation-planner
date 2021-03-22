#!/usr/bin/env python

"""Tests for `iact_observation_planner` package."""
import os
import subprocess as sp


import pytest


from astropy.coordinates import EarthLocation

from iact_observation_planner import iact_observation_planner
from iact_observation_planner import observer_config
from iact_observation_planner import targets


def test_deploy_config(tmp_path):
    site_cfg = "site_config.json"
    command = "iop-init"

    call = sp.run([command, "--init", str(tmp_path)], stdout=sp.PIPE)

    dest_file = "{}".format(str(tmp_path) + "/" + site_cfg)
    assert "GENERATED DEFAULT CONFIG ->" and dest_file in call.stdout.decode("utf-8")
    assert os.path.isfile(dest_file)


@pytest.mark.parametrize("site",["HESS", "MAGIC"])
@pytest.mark.parametrize("dark",["dark", "gray", "bright"])
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

@pytest.mark.parametrize("targets", [["Crab Nebula;30;2", "Vela Pulsar;25;4"], ["PKS2155-304;55;10"]])
@pytest.mark.parametrize("darkness", [None, "dark", "gray", "bright"])
def test_main_script_options(targets, darkness):
    command = "iact-observation-planner"
    test_targets = " ".join(targets)
    dark = ""
    if darkness:
        dark = "-o {}".format(darkness)

    call = sp.run([command, test_targets, dark], stdout=sp.PIPE)
