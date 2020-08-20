# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE songplays
(
    songplay_id SERIAL UNIQUE,
    start_time TIMESTAMP,
    user_id TEXT,
    level TEXT,
    song_id TEXT,
    artist_id TEXT,
    session_id INTEGER,
    location TEXT,
    user_agent TEXT
)""")

user_table_create = ("""CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    level TEXT
)""")

song_table_create = ("""CREATE TABLE songs
(
    song_id TEXT PRIMARY KEY,
    title TEXT,
    artist_id TEXT,
    year INTEGER,
    duration FLOAT
)""")

artist_table_create = ("""CREATE TABLE artists
(
    artist_id TEXT PRIMARY KEY,
    name TEXT,
    location TEXT,
    latitude FLOAT,
    longitude FLOAT
)""")

time_table_create = ("""CREATE TABLE time
(
    start_time TIMESTAMP,
    hour INTEGER,
    day TEXT,
    week INTEGER,
    month TEXT,
    year INTEGER,
    weekday INTEGER
)""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = '''INSERT INTO songs
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO NOTHING'''

artist_table_insert = '''INSERT INTO artists
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO NOTHING'''

time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create
]

drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop
]
