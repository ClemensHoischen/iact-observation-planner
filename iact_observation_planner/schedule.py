""""
Schedule class that provides good output and plotting.
"""

from datetime import datetime, timedelta, date

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.dates import num2date, date2num


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
                culmination = max(time_alt, key=lambda item: item[1])
                print(
                    f" * {key}: from {start:%H:%M:%S} to {end:%H:%M:%S}  highest altitude at {culmination[0]:%H:%M:%S}: {culmination[1]:.1f}"
                )

    def plot_schedule(self, all_targets):
        # one ax per night
        # night range = sun_set <-> sun_rise +/- 1h
        # plot each target observable range in each night

        fig, axes = plt.subplots(nrows=self.n_nights, ncols=1, sharex=True)

        fig.set_tight_layout({"rect": [0, 0, 1, 0.95], "pad": 0, "h_pad": 0})
        # plt.setp(axes)
        # get global layout stuff
        #   min and max time for the plot as a number
        earliest_set = min(self.nights, key=lambda x: x.sun_set.time()).sun_set
        latest_rise = max(self.nights, key=lambda x: x.sun_rise.time()).sun_rise

        time_min = (
            timedelta(
                days=0,
                hours=earliest_set.hour,
                minutes=earliest_set.minute,
                seconds=earliest_set.second,
            )
            - timedelta(hours=1)
        )

        time_max = (
            timedelta(
                days=1,
                hours=latest_rise.hour,
                minutes=latest_rise.minute,
                seconds=latest_rise.second,
            )
            + timedelta(hours=1)
        )

        # prepare first night more carefully:
        ybins = np.linspace(-1, 1, len(all_targets) + 1)
        n_hours = round((time_max - time_min).total_seconds() / 60.0 / 60.0)

        hour_labels = [
            (time_min + timedelta(hours=i)).total_seconds() // 3600
            for i in range(n_hours)
        ]
        xticks_ar = [timedelta(hours=hour).total_seconds() for hour in hour_labels]

        hour_labels = [hour for hour in hour_labels if hour < 24] + [
            hour - 24 for hour in hour_labels if hour > 23
        ]
        xtick_labels = [f"{int(hour):02}:00" for hour in hour_labels]

        # plot all nights and targets
        i_night = 0
        for night in self.nights:
            ax = axes[i_night]
            plot_sun_moon_down(ax, night.sun_set, night.sun_rise, night.moon_set, night.moon_rise)
            date = night.date
            
            ybins = np.linspace(-1, 1, (len(night.schedule.keys())) + 1)
            for i, key in enumerate(night.schedule.keys()):
                target = night.schedule[key]
                start = get_timedelta_seconds(target["start"].time())
                end = get_timedelta_seconds(target["end"].time())
                ymin = ybins[i]
                ymax = ybins[i + 1]
                ax.fill_between([start, end], ymin, ymax, alpha=1, color=target["color"])

            ax.set_yticks(np.arange(1))
            ax.set_yticklabels([f"{date:%Y-%m-%d}"])
            i_night += 1

        [ax.set_xticks(xticks_ar) for ax in axes]
        [ax.set_xticklabels(xtick_labels) for ax in axes]

        #TODO: add legend with target names
        #TODO: add title
        #TODO: add axis titles
        #TODO: return fig object for storage according to options
        #TODO: add grid

        plt.show()
        return fig


def plot_sun_moon_down(ax, sun_set, sun_rise, moon_set, moon_rise):
    start_sun = get_timedelta_seconds(sun_set)
    end_sun = get_timedelta_seconds(sun_rise)
    start_moon = get_timedelta_seconds(moon_set)
    end_moon = get_timedelta_seconds(moon_rise)
    # mark area where the sun is down
    ax.fill_between([start_sun, end_sun], -1.25, 1.25, color="black", alpha=0.4, zorder=0)
    # TODO: also mark the area where the sun and moon is down
    moon_start = max([start_sun, start_moon])
    moon_end = min([end_sun, end_moon])
    #
    # ax.fill_between([moon_start, moon_end], -1.25, 1.25,
    #                 where=moon_start>=start_sun and moon_end <=end_sun,
    #                 color='black', alpha=0.6, zorder=1)


def get_timedelta_seconds(time):
    days = 0
    if time.hour < 12:
        days = 1

    time_d = timedelta(
        days=days, hours=time.hour, minutes=time.minute, seconds=time.second
    )

    return time_d.total_seconds()
