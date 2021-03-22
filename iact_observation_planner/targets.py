# target.py

from astropy import coordinates as coo


def _resolve_target_coordinates(target_names):
    """takes a list of target name strings and returns reformatted strings
    and coordinates (names, coords)
    """
    names = []
    coords = []

    for name in target_names:
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

        names.append(tag)
        coords.append(position)

    return names, coords


class Target:
    def __init__(self, name, coord):
        self.name = name
        self.coords = coord
        self.observe_starts = []
        self.observe_ends = []

    def __repr__(self):
        out = ""
        out += "{0:15s} : {coord}".format(
            self.name, coord=self.coords.to_string(style="hmsdms")
        )
        out += " - (ra = {} deg = {} deg)\n".format(
            self.coords.ra.deg, self.coords.dec.deg
        )
        return out


def resolve_target_list(names_list):
    targets = []
    names, coords = _resolve_target_coordinates(names_list)
    for nn, cc in zip(names, coords):
        targets.append(Target(nn, cc))

    return targets
