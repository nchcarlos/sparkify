import datetime as dt
import glob
import os
import psycopg2
import pandas as pd
from sql_queries import (artist_table_insert, songplay_table_insert,
        song_select, song_table_insert, time_table_insert, user_table_insert)

def process_song_file(cur, filepath):
    """
    Parse a song data file and insert the data into the songs and artists
    databases.

    arguments:
    cur -- a cursor to perform the database operations
    filepath -- the path to the song data log file
    """
    df = pd.read_json(filepath, orient='records', lines=True)

    song_cols = [
        'song_id',
        'title',
        'artist_id',
        'year',
        'duration'
    ]

    artist_cols = [
        'artist_id',
        'artist_name',
        'artist_location',
        'artist_latitude',
        'artist_longitude'
    ]

    # assuming 1 line per file
    _, song_data = next(df[song_cols].iterrows())
    cur.execute(song_table_insert, tuple(song_data.values))

    _, artist_data = next(df[artist_cols].iterrows())
    cur.execute(artist_table_insert, tuple(artist_data.values))

def process_log_file(cur, filepath):
    """
    Parse a log data log file and insert the data into the songplays, users, and
    time databases.

    arguments:
    cur -- a cursor to perform the database operations
    filepath -- the path to the log data log file
    """
    # open log file
    df = pd.read_json(filepath, orient='records', lines=True)

    # we have to handle missing values for userId
    df['userId'] = df['userId'].apply(lambda x: None if isinstance(x, str) else x)

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    df['start_time'] = t.dt.time
    df['hour'] = t.dt.hour
    df['day'] = t.dt.day
    df['week'] = t.dt.isocalendar().week
    df['month'] = t.dt.month
    df['year'] = t.dt.year
    df['weekday'] = t.dt.weekday

    # filter by NextSong action
    songplay_data = df[df['page'] == 'NextSong']

    songplay_cols = [
        'start_time',
        'userId',
        'level',
        'song',
        'artist',
        'sessionId',
        'location',
        'userAgent'
    ]

    time_cols = [
        'start_time',
        'hour',
        'day',
        'week',
        'month',
        'year',
        'weekday'
    ]

    user_cols = [
        'userId',
        'firstName',
        'lastName',
        'gender',
        'level'
    ]

    # insert songplay records
    # sub-queries are used in the songplay_table_insert SQL to get the song_id
    # and the artist_id so we don't have to execute extra select statements to
    # get the data
    for _, row in songplay_data[songplay_cols].iterrows():
        cur.execute(songplay_table_insert, tuple(row.values))

    # insert time data records
    for _, row in df[time_cols].iterrows():
        cur.execute(time_table_insert, tuple(row))

    # load user table
    user_data = df[df['userId'].notnull()]

    # insert user records
    for _, row in user_data[user_cols].iterrows():
        cur.execute(user_table_insert, tuple(row.values))

def process_data(cur, conn, filepath, func):
    """
    Process data files in the data directory. Given the filepath, this function
    traverses the directory and extracts the paths to each JSON file. Each filepath
    is passed as an argument to the provided function that will extract the
    appropriate data.

    arguments:
    cur -- a cursor to perform the database operations
    conn -- a connection to the database
    filepath -- the path to the data directory
    func -- a function that will process the data file
    """
    # get all files matching extension from directory
    all_files = []
    for root, _, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

def main():
    conn = psycopg2.connect(
            "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()

if __name__ == "__main__":
    main()
