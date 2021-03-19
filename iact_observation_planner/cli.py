"""Console script for iact_observation_planner."""
import argparse
import sys
import os
import json

from iact_observation_planner.observer_config import observer_config


def deploy_default_cfg(path):
    site_cfg = "site_config.json"
    destination = path + "/" + site_cfg

    if os.path.isfile(destination):
        print("Site Config already present. Delete it if you want to get a fresh one.")
        return -1

    default_config = observer_config()
    with open(destination, "w") as config_file:
        json.dump(default_config, config_file)

    print("GENERATED DEFAULT CONFIG -> {}".format(destination))
    print(json.dumps(default_config, indent=4), "\n")
    print("execute: export SITE_CONFIG={}".format(
        destination), "to use this configuration.")
    return 0


def main():
    """Console script for iact_observation_planner."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', dest='init_path',
                        help="initialize a default configuration that can be tuned to your needs.")
    args = parser.parse_args()

    target_base_path = args.init_path

    if not os.path.exists(target_base_path):
        print("{} is not a valid path.\n ... Aborting.".format(target_base_path))
        return -1

    return_site_cfg = deploy_default_cfg(target_base_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
