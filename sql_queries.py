# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = """
CREATE TABLE songplays
(
    songplay_id SERIAL UNIQUE,
    start_time TIME,
    user_id INTEGER,
    level TEXT,
    song_id TEXT,
    artist_id TEXT,
    session_id INTEGER,
    location TEXT,
    user_agent TEXT
)
"""

user_table_create = """
CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    level TEXT
)
"""

song_table_create = """
CREATE TABLE songs
(
    song_id TEXT PRIMARY KEY,
    title TEXT,
    artist_id TEXT,
    year INTEGER,
    duration FLOAT
)
"""

artist_table_create = """
CREATE TABLE artists
(
    artist_id TEXT PRIMARY KEY,
    name TEXT,
    location TEXT,
    latitude FLOAT,
    longitude FLOAT
)
"""

time_table_create = """
CREATE TABLE time
(
    start_time TIME PRIMARY KEY,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER
)
"""

# INSERT RECORDS

songplay_table_insert = """
INSERT INTO songplays
(
    start_time, user_id, level,
    song_id,
    artist_id,
    session_id, location, user_agent
)
VALUES
(
    %s, %s, %s,
    (
        SELECT song_id
        FROM songs
        WHERE LOWER(TRIM(title)) = LOWER(TRIM(%s))
    ),
    (
        SELECT artist_id
        FROM artists
        WHERE LOWER(TRIM(name)) = LOWER(TRIM(%s))
    ),
    %s, %s, %s
)
"""

user_table_insert = """
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id)
DO NOTHING
"""

song_table_insert = """
INSERT INTO songs  (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO NOTHING
"""

artist_table_insert = """
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO NOTHING
"""

time_table_insert = """
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time)
DO NOTHING
"""

# FIND SONGS

song_select = """
SELECT s.song_id, a.artist_id
FROM songs s
JOIN artist a
    ON a.artist_id = s.artist_id AND LOWER(TRIM(name)) = LOWER(TRIM(%s))
WHERE LOWER(TRIM(title)) = LOWER(TRIM(%s))
"""

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
