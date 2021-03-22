"""observer_config.py

contains the default observer configuration that is written to user-space for configuration.
"""

import json

import astropy.units as u
from astropy.units import Quantity
from astropy.coordinates import EarthLocation


class ObserverConfiguration:
    def __init__(self, cfg_data):
        self.cfg_data = cfg_data
        self.sites = cfg_data["Sites"]
        self.darkness = cfg_data["Darkness"]
        self.obs_pars = cfg_data["ObservationParameters"]

    def __repr__(self):
        return json.dumps(self.cfg_data, indent=2)

    def get_site_from_name(self, name):
        # Getter for the specific site from the cfg
        print("GET SITE")
        site = self.sites[name]
        return EarthLocation(
            lon=float(site["lon"]),
            lat=float(site["lat"]),
            height=float(site["height"]),
        )

    def get_darkness_from_name(self, name):
        # Getter for specific darkness criteria from the config
        return self.darkness[name]

    def get_observation_pars(self):
        # Getter for observation parameters
        return (self.obs_pars["run_duration"], self.obs_pars["wobble_offset"])


def default_observer_config():
    cfg = {
        "Sites": {
            "HESS": {
                "lon": 16.3,
                "lat": -23.26,
                "height": 1800,
            },
            "MAGIC": {
                "lon": 18.890,
                "lat": 28.7619,
                "height": 2200,
            }
        },
        "Darkness": {
            "dark": {
                "max_sun_altitude": "-16 deg",
                "max_moon_altitude": "-0.5 deg",
                "max_moon_phase": False,
                "min_moon_distance": False,
            },
            "gray": {
                "max_sun_altitude": "-16 deg",
                "max_moon_altitude": "45 deg",
                "max_moon_phase": "0.5",
                "min_moon_distance": "60 deg",
            },
            "bright": {
                "max_sun_altitude": "-16 deg",
                "max_moon_altitude": "70 deg",
                "max_moon_phase": "0.7",
                "min_moon_distance": "45 deg",
            },
        },
        "ObservationParameters": {
            "run_duration": "28 min",
            "wobble_offset": "0.7 deg",
        },
    }
    return cfg
