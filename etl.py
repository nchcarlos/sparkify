import datetime as dt
import glob
import os
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
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

    # We need to rename the columns from the log file to match what is defined
    # in the database. It turns out we can just strip the artist_ prefix from
    # all the fields except artist_id.
    artist_col_map = {c: c.replace('artist_', '') for c in artist_cols[1:]}

    # assuming 1 line per file
    _, song_data = next(df[song_cols].iterrows())
    cur.execute(song_table_insert, tuple(song_data.values))

    _, artist_data = next(df[artist_cols].rename(columns=artist_col_map).iterrows())
    cur.execute(artist_table_insert, tuple(artist_data.values))

def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, orient='records', lines=True)

    # we have to divide the ts data to convert it properly
    df['ts_sec'] = df['ts'].apply(lambda x: x / 1000)

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts_sec'], unit='s')
    df['ts'] = t

    # filter by NextSong action
    songplay_data = df[df['page'] == 'NextSong']
    songplay_data['start_time'] = songplay_data['ts'].dt.time

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

    for _, row in songplay_data[songplay_cols].iterrows():
        # print(tuple(row.values))
        cur.execute(songplay_table_insert, tuple(row.values))

    # # insert time data records
    time_data = songplay_data[['ts', 'start_time']]
    time_data['hour'] = time_data['ts'].dt.hour
    time_data['day'] = time_data['ts'].dt.day
    time_data['week'] = time_data['ts'].dt.week
    time_data['month'] = time_data['ts'].dt.month
    time_data['year'] = time_data['ts'].dt.year
    time_data['weekday'] = time_data['ts'].dt.weekday

    # for i, row in time_df.iterrows():
    #     cur.execute(time_table_insert, list(row))

    # # load user table
    # user_data = df[df['userId'] != '']

    # # insert user records
    # for _, row in user_data[user_cols].iterrows():
    #     cur.execute(user_table_insert, tuple(row.values))

    # # insert songplay records
    # for index, row in df.iterrows():

    #     # get songid and artistid from song and artist tables
    #     results = cur.execute(song_select, (row.song, row.artist, row.length))
    #     songid, artistid = results if results else None, None

    #     # insert songplay record
    #     songplay_data =
    #     cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
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