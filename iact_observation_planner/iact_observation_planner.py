"""Main module."""
import os

from datetime import datetime, timedelta
from astropy.time import Time

from iact_observation_planner import observer_config
from iact_observation_planner import targets


CFG_DATA = observer_config.default_observer_config()
if os.environ.get("IOP_SITE_CONFIG"):
    # Lookup the site configuration and parse it.
    print("NOT IMPLEMENTED")

CFG = observer_config.ObserverConfiguration(CFG_DATA)


def parse_options(site, darkness, date, plan_range):
    """parses the options for the planning including the targets"""

    # parse targets
    opts = {}
    opts.update(parse_date(date))
    opts.update(parse_range(plan_range))
    opts.update(parse_site(site))
    opts.update(parse_darkness(darkness))

    return opts


def parse_darkness(option):
    return {"darkness": CFG.get_darkness_from_name(option)}


def parse_site(option):
    return {"site": CFG.get_site_from_name(option)}


def parse_range(option):
    """ parse the range options """
    return {"range": timedelta(days=option)}


def parse_date(option):
    """ parse date and range """
    date_opt = option
    date = Time(datetime.utcnow()).datetime

    if date_opt is not None:
        date = Time(date_opt, scale="utc").datetime

    date = datetime(date.year, date.month, date.day)

    return {"date": date}


def plan_targets(targets, site, darkness, date, plan_range):
    """main function of the tool that performs the planning"""
    targets = targets.resolve_target_list(targets)
    print(site, type(site))
    options = parse_options(site, darkness, date, plan_range)

    # calculate sun rise/set times
    # calculate moon conditions
    # claculate target visibility
    # allocate targets
