"""
Main script of the iact-observation-planner tool.
To be called via the commandline with `iact-observation-planner`
"""

import argparse
import sys

from datetime import datetime, timedelta

from iact_observation_planner import targets


def main():
    """Console script for iact_observation_planner."""
    parser = argparse.ArgumentParser(
        """Plan observations for specified targets with many options.\n
The target names can either be a source name resolvable by Simbad, or if prefixed
by rd/ or lb/,  a set of RA/Dec or Galactic coordinates in the format
expected by astropy SkyCoords, separated by a comma. E.g. rd/14h23m27s,-29d
or rd/280.0d,-45.6d You can add a tag name too: rd/14h23m,-29d/MySource
"""
    )
    parser.add_argument(
        "--target",
        metavar="target",
        type=str,
        nargs="+",
        help="""Targets to plan observations for.
Expected Format: e.g. <target_name>;<altitude_limit>;<hours>.\n
Example: "Crab Nebula;30;5" to plan observations on the crab nebula with
30 deg altitude limit for 5 hours.""",
    )
    parser.add_argument(
        "-d",
        "--date",
        dest="date",
        default=datetime.today(),
        help="date for the planning of observations",
    )
    parser.add_argument(
        "-r",
        "--range",
        dest="range",
        default=1,
        type=int,
        help="range of days to consider for the planning",
    )
    parser.add_argument(
        "-o",
        "--darkness",
        dest="darkness",
        help="darknes configuration to be used in the planning",
        default="dark",
    )
    parser.add_argument(
        "-s",
        "--site",
        dest="site",
        help="select a site for the planned observations"
        + "(needs to be present in the configuration)",
        default="HESS",
    )

    args = parser.parse_args()

    if not args.target:
        parser.print_help()
        return 0

    parsed_targets = targets.resolve_target_list(args.target)

    print("Will evaluate the possible observation for targets:")
    for target in parsed_targets:
        print(target)
    print("planning with:")
    print("  * site: {}".format(args.site))
    print("  * date: {}".format(args.date))
    print("  * range: {}".format(timedelta(days=args.range)))

    return 0


if __name__ == "__main__":
    main()
