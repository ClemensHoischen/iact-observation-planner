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
    def __init__(self, name, coord, alt=45, hours=2):
        self.name = name
        self.coords = coord
        self.alt_limit = alt
        self.hours = hours
        self.observe_starts = []
        self.observe_ends = []

    def __repr__(self):
        out = ""
        out += "{0:15s} : {coord}".format(
            self.name, coord=self.coords.to_string(style="hmsdms")
        )
        out += " - (ra = {:2.2f} deg = {:2.2f} deg)".format(
            self.coords.ra.deg, self.coords.dec.deg
        )
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
            Target(target_dict["name"], coords, target_dict["alt_limit"], target_dict["hours"])
        )

    return targets
