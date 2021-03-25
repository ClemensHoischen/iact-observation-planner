# target.py

from astropy import coordinates as coo


def resolve_target_coordinates(name):
    """takes a list of target name strings and returns reformatted strings
    and coordinates (names, coords)
    """
    position = None
    tag = name
    if name.startswith("rd/"):
        position_str = name[3:].replace(",", " ")
        if position_str.find("/") > 0:
            # try to extract a name tag if it is there
            position_str, tag = position_str.split("/")
        position = coo.SkyCoord(position_str, frame=coo.ICRS)
    elif name.startswith("lb/"):
        position_str = name[3:].replace(",", " ")
        if position_str.find("/") > 0:
            # try to extract a name tag if it is there
            position_str, tag = position_str.split("/")
        position = coo.SkyCoord(position_str, frame=coo.Galactic)
    else:
        position = coo.SkyCoord.from_name(name)

    return position


class Target:
    """target class that holds the central information on each target, such as:
    * name
    * coordinates
    * altitude limit in degrees
    * hours targeted in observations
    * start time(s) of observable windows
    * end time(s) of observable windows
    """

    def __init__(self, name, coord, alt, hours):
        self.name = name
        self.coords = coord
        self.alt_limit = alt
        self.hours = hours

        # set altitude and hours to default values
        if not self.alt_limit:
            self.alt_limit = 45
        if not self.hours:
            self.hours = 2

        self.observe_starts = []
        self.observe_ends = []

    def __repr__(self):
        placeholder = ""
        out = ""
        out += f"{self.name:15} : {self.coords.to_string(style='hmsdms')}"
        out += f" - (ra = {self.coords.ra.deg:2.2f} deg = {self.coords.dec.deg:2.2f} deg)\n"
        out += f"{placeholder:15}   Altitude > {self.alt_limit}\n"
        out += f"{placeholder:15}   Target observation time = {self.hours}"

        return out


def resolve_target_list(targets_list):
    """resolves the target argument list given by the main tools usage into workable targets
    with name, coordinates, ..."""
    targets = []

    # Fill all targets from the commandline arguments into a dict
    targets_dict = {}
    for target in targets_list:
        target_args = target.split(";")
        name = target_args[0]

        if len(target_args) > 1:
            alt_limit = target_args[1]
        else:
            alt_limit = None

        if len(target_args) > 2:
            hours = target_args[2]
        else:
            hours = None

        targets_dict[name] = {"name": name, "alt_limit": alt_limit, "hours": hours}

    # fill a list of Target objects from the dict and return it
    for name, target_dict in targets_dict.items():
        name = target_dict["name"]
        coords = resolve_target_coordinates(target_dict["name"])
        targets.append(
            Target(
                target_dict["name"],
                coords,
                target_dict["alt_limit"],
                target_dict["hours"],
            )
        )

    return targets
