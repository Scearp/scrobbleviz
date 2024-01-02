from calendar import calendar
import plays

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys


def main():
    with open("config.txt") as dat:
        paths = [line.replace("\n", "") for line in dat.readlines()]

    all_plays = []
    for p in paths:
        if "lastfm" in p:
            all_plays.append(plays.load_lastfm_plays(p))
        elif "spotify" in p:
            all_plays.append(plays.load_spotify_plays(p))

    all_plays = pd.concat(all_plays)

    if len(sys.argv) > 1:
        all_plays = all_plays[all_plays['artist']
                              == sys.argv[1].replace('_', ' ')]

    start_year = 2019
    end_year = 2023

    calendar = []
    years = [y for y in range(start_year, start_year + 1)]
    months = [m for m in range(1, 13)]

    for y in range(start_year, end_year + 1):
        by_month = []
        df = all_plays[all_plays['date'].apply(lambda d: d.year == y)]
        for m in range(1, 13):
            mdf = df[df['date'].apply(lambda d: d.month == m)]
            if len(mdf) > 0:
                by_month.append(len(mdf))
            else:
                by_month.append(np.nan)
        calendar.append(by_month)

    calendar = np.array(calendar)

    fig, ax = plt.subplots()
    im = ax.imshow(calendar)

    for y in range(len(calendar)):
        for m in range(len(calendar[0])):
            if calendar[y, m] > 0:
                text = ax.text(m, y, round(calendar[y, m]),
                               ha='center', va='center', color='w')

    plt.show()


if __name__ == "__main__":
    main()
