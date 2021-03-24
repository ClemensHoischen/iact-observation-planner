"""nights.py"""
from datetime import timedelta

import astropy.units as u
from astropy.units import Quantity
from astropy.coordinates import Angle

from astropy.time import Time
import ephem


class Night:
    def __init__(self, date, site, darkness):
        self.date = date
        self.site = site
        self.darkness = darkness
        self.sun_set, self.sun_rise = find_sun_rise_and_set(
            self.date, self.site, self.darkness
        )

    def __repr__(self):
        out = str(self.date) + "\n"
        out += " * Sun Set:  {}\n".format(self.sun_set)
        out += " * Sun Rise: {}\n".format(self.sun_rise)
        return out


def setup_nights(date, site, darkness, plan_range):
    nights = []

    n_nights = plan_range.days
    night_start = date

    for i in range(n_nights):
        night = night_start + timedelta(days=i)
        nights.append(Night(night, site, darkness))

    return nights


def find_sun_rise_and_set(date, site, darkness):
    sun_rise = None
    sun_set = None

    sun_horizon = Angle(darkness["max_sun_altitude"]).to_string(unit=u.degree, sep=":")

    sun = ephem.Sun()
    obs = ephem.Observer()
    obs.lon = str(site.lon / u.deg)
    obs.lat = str(site.lat / u.deg)
    obs.elev = site.height / u.m
    obs.date = date
    obs.horizon = sun_horizon
    sun.compute(obs)

    sun_set = obs.next_setting(sun, use_center=True, start=date).datetime()
    sun_rise = obs.next_rising(sun, use_center=True, start=sun_set).datetime()

    return sun_set, sun_rise
