"""observer_config.py

contains the default observer configuration that is written to user-space for configuration.
"""


def observer_config():
    cfg = {
        "Site": {
            "site_name": "H.E.S.S.",
            "site_lon": "16.3 deg",
            "site_lat": "-23.26 deg",
            "site_alt": "1800 m",
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
            "wobble offset": "0.7 deg",
        },
    }
    return cfg
