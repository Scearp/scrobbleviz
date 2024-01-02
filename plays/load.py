import pandas as pd
import numpy as np
import matplotlib.dates as pdt

from pyarrow import csv, json
from datetime import datetime

def load_lastfm_plays(file_name):
    options = csv.ReadOptions(column_names=["artist",
                                        "album",
                                        "track",
                                        "date"])
    table = csv.read_csv(file_name, read_options=options)
    df = table.to_pandas()

    #df.date = [datetime.strptime(d, "%d %b %Y %H:%M").date()
    #           for d in df.date]

    dates = []
    for d in df.date:
        try:
            dates.append(datetime.strptime(d, "%d %b %Y %H:%M").date())
        except:
            dates.append(0)

    df.date = dates
    
    df = df[df.date != 0]

    return df

def load_spotify_plays(file_name):
    df = pd.read_json(file_name)
    df = df[df['msPlayed'].apply(lambda t: t > 30000)]

    df.columns = ['date', 'artist', 'track', 'album']

    df['date'] = [datetime.strptime(d, "%Y-%m-%d %H:%M").date()
               for d in df.date]

    df['album'] = [np.nan] * len(df['album'])


    return df
