"""Console script for iact_observation_planner."""
import argparse
import os
import sys
import json

from iact_observation_planner.observer_config import default_observer_config


def deploy_default_cfg(path):
    """Function that deploys the default config to specified path and prompts the instructions
    for the needed environment variable to make use of it."""
    site_cfg = "site_config.json"
    destination = path + "/" + site_cfg

    if os.path.isfile(destination):
        print("Site Config already present. Delete it if you want to get a fresh one.")
        return -1

    default_config = default_observer_config()
    with open(destination, "w") as config_file:
        json.dump(default_config, config_file)

    print("GENERATED DEFAULT CONFIG -> {}".format(destination))
    print(json.dumps(default_config, indent=4), "\n")
    print(
        "execute: export IOP_SITE_CONFIG={}".format(destination),
        "to use this configuration. NOT IMPLEMENTED YET",
    )
    return 0


def main():
    """Console script for iact_observation_planner that deploys a configuration
    to user sapce and instructs the user how to enforce it being used."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--init",
        dest="init_path",
        help="initialize a default configuration that can be tuned to your needs.",
    )
    args = parser.parse_args()

    target_base_path = args.init_path

    if not os.path.exists(target_base_path):
        print("{} is not a valid path.\n ... Aborting.".format(target_base_path))
        return -1

    return deploy_default_cfg(target_base_path)


if __name__ == "__main__":
    main()
