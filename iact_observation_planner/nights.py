"""nights.py"""
from datetime import timedelta


class Night:
    def __init__(self, date):
        self.date = date
        self.sun_rise, self.sun_set = find_sun_rise_and_set(self.date)

    def __repr__(self):
        return str(self.date)

    def find_dark_range(self, darkness):
        # do calculation
        pass


def find_sun_rise_and_set(date):
    sun_rise = None
    sun_set = None

    # do calculation

    return sun_rise, sun_set


def setup_nights(date, plan_range):
    nights = []

    n_nights = plan_range.days
    night_start = date

    for i in range(n_nights):
        night = night_start + timedelta(days=i)
        nights.append(Night(night))

    return nights
