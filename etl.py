import os
import glob
import json
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
    pass

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
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    # conn.set_session(autocommit=True)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    # process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()

if __name__ == "__main__":
    main()