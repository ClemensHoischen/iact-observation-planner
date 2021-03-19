#!/usr/bin/env python

"""Tests for `iact_observation_planner` package."""
import os
import subprocess as sp


import pytest


from iact_observation_planner import iact_observation_planner


def test_deploy_config(tmp_path):
    site_cfg = "site_config.json"
    command = "iact-observation-planner"

    call = sp.run([command, "--init", str(tmp_path)], stdout=sp.PIPE)
    print(call.stdout.decode("utf-8"))

    dest_file = "{}".format(str(tmp_path) + "/" + site_cfg)
    assert "GENERATED DEFAULT CONFIG ->" and dest_file in call.stdout.decode("utf-8")
    assert os.path.isfile(dest_file)
