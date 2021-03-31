"""Main module."""
import os

from datetime import datetime, timedelta
from astropy.time import Time

from iact_observation_planner import observer_config
from iact_observation_planner import targets as iop_targets
from iact_observation_planner import nights as iop_nights
from iact_observation_planner.schedule import Schedule

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


def plan_targets(target, site, darkness, date, plan_range):
    """main function of the tool that performs the planning"""
    targets = iop_targets.resolve_target_list(target)
    options = parse_options(site, darkness, date, plan_range)
    summarize_options(options, targets)

    # Setup the nights to plan and calculate sun rise/set times
    planned_nights = iop_nights.setup_nights(
        options["date"], options["site"], options["darkness"], options["range"]
    )

    # calculate 1 night per thread TODO: Threadding
    for night in planned_nights:
        for target in targets:
            night.plan_target(target)

    sched = Schedule(planned_nights)
    # TODO: summarize available tarktime per target
    # TODO: allocate time according to options (zenith, time)    
    figure = sched.plot_schedule(targets)
    figure.savefig("obsplan.png")
    #save figure according to options
    

def summarize_options(options, targets):
    out = "Planning the following targets:\n"
    for target in targets:
        out += f"{target}\n"

    out += "Boundry Conditions:\n"
    out += f" * Site:       {options['site'].info.name}\n"
    out += f" * Darkness:   {options['darkness']}\n"
    out += f" * Start Date: {options['date']:%Y-%m-%d}\n"
    out += f" * N nights:   {options['range'].days}\n"

    print(out)
