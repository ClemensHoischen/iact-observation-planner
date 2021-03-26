""""
Schedule class that provides good output and plotting.
"""

import matplotlib.pyplot as plt


class Schedule:
    def __init__(self, nights):
        self.nights = nights
        self.dates = [night.date for night in self.nights]
        self.sched_start = min([night.sun_set] for night in self.nights)
        self.sched_end = max([night.sun_rise] for night in self.nights)
        self.n_nights = len(self.nights)
        self.layout_schedule()

    def layout_schedule(self):
        for night in self.nights:
            print(f"Evening Date: {night.date:%Y-%m-%d}")
            targets_schedule = night.schedule
            for key in targets_schedule.keys():
                target = targets_schedule[key]
                start = target["start"]
                end = target["end"]
                time_alt = zip(target["times"], target["altitudes"])
                culmination = max(time_alt, key=lambda item:item[1])[0]
                print(f" * {key}: from {start:%H:%M:%S} to {end:%H:%M:%S}  culmination at {culmination:%H:%M:%S}")




    