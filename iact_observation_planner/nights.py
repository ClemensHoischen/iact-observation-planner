"""nights.py"""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from matplotlib.dates import num2date, date2num

import astropy.units as u
from astropy.time import Time
from astropy.units import Quantity
from astropy.coordinates import Angle, SkyCoord, AltAz

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
        self.moon_set, self.moon_rise = find_monn_rise_and_set(
            self.date, self.site, self.darkness
        )
        self.schedule = {}

    def __repr__(self):
        out = f"Evening Date: {self.date:%Y-%m-%d}\n"
        out += f" * Sun Set:  {self.sun_set}\n"
        out += f" * Sun Rise: {self.sun_rise}\n"
        return out

    def plan_target(self, target):
        """plan a target into a single night

        Args:
            target (target): target to plan
        """
        test_range = [timedelta(seconds=0), self.sun_rise - self.sun_set]
        sun_set_date = Time(self.sun_set, scale="utc")

        time_range = (
            np.linspace(test_range[0].seconds / 3600, test_range[1].seconds / 3600, 200)
            * u.hour
        ) + sun_set_date

        test_dates = np.array([date2num(time.datetime) for time in time_range])

        # calculate the moon and target positions during the night in alt az coordinates
        moon_pos = self.calculate_moon_positions(time_range)
        target_alt_az = self.calculate_target(time_range, target)

        # calculate the target/moon separation
        moon_alt_az = AltAz(
            alt=Angle(moon_pos["altitudes"], unit=u.deg),
            az=Angle(moon_pos["azimuths"], unit=u.deg),
            location=self.site,
            obstime=time_range,
        )
        targt_moon_separation = target_alt_az.separation(moon_alt_az)

        # get the appropriate darkness criteria and apply to the moon
        max_moon_alt = Quantity(self.darkness["max_moon_altitude"])
        max_moon_phase = False
        if self.darkness["max_moon_phase"]:
            max_moon_phase = Quantity(self.darkness["max_moon_phase"])
        min_moon_distance = False
        if self.darkness["min_moon_distance"]:
            min_moon_distance = Quantity(self.darkness["min_moon_distance"])

        # prepare the selection masks
        target_alt_ok = target_alt_az.alt > target.alt_limit
        moon_alt_ok = moon_alt_az.alt < max_moon_alt

        moon_dist_ok = [True for _ in target_alt_az]
        if min_moon_distance is not False:
            moon_dist_ok = targt_moon_separation > min_moon_distance

        moon_phase_ok = [True for _ in target_alt_az]
        if max_moon_phase is not False:
            moon_phase_ok = moon_pos["phases"] < max_moon_phase

        # apply masks
        filter_mask = target_alt_ok & moon_alt_ok & moon_dist_ok & moon_phase_ok
        valid_target_times = test_dates[filter_mask]
        valid_dates = [num2date(d) for d in valid_target_times]

        if len(valid_dates):
            target_start = min(valid_dates)
            target_end = max(valid_dates)

            self.schedule.update(
                {
                    target.name: {
                        "start": target_start,
                        "end": target_end,
                        "altitudes": target_alt_az.alt[filter_mask],
                        "times": valid_dates,
                        "color": target.color,
                    }
                }
            )

    def calculate_target(self, time_range, target):
        position = SkyCoord(
            target.coords.ra, target.coords.dec, unit=target.coords.ra.unit
        )

        altaz_frame = AltAz(obstime=time_range, location=self.site)
        return position.transform_to(altaz_frame)

    def calculate_moon_positions(self, test_dates):
        moon_altitudes = np.zeros_like(test_dates)
        moon_azimuths = np.zeros_like(test_dates)
        moon_phases = np.zeros_like(test_dates)

        moon = ephem.Moon()
        obs = ephem.Observer()
        obs.lon = str(self.site.lon / u.deg)
        obs.lat = str(self.site.lat / u.deg)
        obs.elev = self.site.height / u.m
        for ii, tt in enumerate(test_dates):
            obs.date = ephem.Date(tt.datetime)
            moon.compute(obs)
            moon_altitudes[ii] = moon.alt * 180.0 / np.pi
            moon_azimuths[ii] = moon.az * 180.0 / np.pi
            moon_phases[ii] = moon.phase

        moon_conditions = {
            "altitudes": moon_altitudes,
            "azimuths": moon_azimuths,
            "phases": moon_phases,
        }
        return moon_conditions


def setup_nights(date, site, darkness, plan_range):
    """Setup an array of night objects that can be used to plan targets.

    Args:
        date (datetime): night-date
        site (EarthLocation): site definition
        darkness (dict): darkness definition
        plan_range (timedelta): number of nights

    Returns:
        nights (array): array of nights
    """
    nights = []

    n_nights = plan_range.days
    night_start = date

    for i in range(n_nights):
        night = night_start + timedelta(days=i)
        nights.append(Night(night, site, darkness))

    return nights


def find_sun_rise_and_set(date, site, darkness):
    """calculates the rise and set time for the sun

    Args:
        date (datetime): night-date
        site (EarthLocation): site definition
        darkness (dict): darkness definition

    Returns:
        sun_set, sun_rise (datetime, datetime): set and rise time of the sun
    """
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

def find_monn_rise_and_set(date, site, darkness):
    moon_rise = None
    moon_set = None

    moon_horizon = Angle(darkness["max_moon_altitude"]).to_string(unit=u.degree, sep=":")
    moon = ephem.Moon()
    obs = ephem.Observer()
    obs.lon = str(site.lon / u.deg)
    obs.lat = str(site.lat / u.deg)
    obs.elev = site.height / u.m
    obs.date = date
    obs.horizon = moon_horizon
    moon.compute(obs)

    moon_set = obs.next_setting(moon, use_center=True, start=date).datetime()
    moon_rise = obs.next_rising(moon, use_center=True, start=moon_set).datetime()

    return moon_set, moon_rise