# Project: Data Modeling with Postgres

## Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

```bash
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```
And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

```json
{
    "num_songs": 1,
    "artist_id": "ARJIE2Y1187B994AB7",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "",
    "artist_name": "Line Renaud",
    "song_id": "SOUPIRU12A6D4FA1E1",
    "title": "Der Kleine Dompfaff",
    "duration": 152.92036,
    "year": 0
}
```

## Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

```bash
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```

And below is an example of what the data in a log file, 2018-11-12-events.json, looks like.

```json
{
    "artist": "Olivia Ruiz",
    "auth": "Logged In",
    "firstName": "Jahiem",
    "gender": "M",
    "itemInSession": 3,
    "lastName": "Miles",
    "length": 254.74567,
    "level": "free",
    "location": "San Antonio-New Braunfels, TX",
    "method": "PUT",
    "page": "NextSong",
    "registration": 1540817347796.0,
    "sessionId": 42,
    "song": "Cabaret Blanco",
    "status": 200,
    "ts": 1541300540796,
    "userAgent": "\"Mozilla\/5.0 (Windows NT 5.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
    "userId": "43"
}
```

## Schema for Song Play Analysis

Using the song and log datasets, a star schema has been developed that was optimized for song data analysis queries.
The ```create_tables.py``` script creates the ```sparkifydb``` database and the following tables.

### Fact Table
1. **songplays** - records in log data associated with song plays i.e. records with page `NextSong`
   - *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

### Dimension Tables
1. **users** - users in the app
   - *user_id, first_name, last_name, gender, level*

1. **songs** - songs in music database
    - *song_id, title, artist_id, year, duration*

1. **artists** - artists in music database
    - *artist_id, name, location, latitude, longitude*

1. **time** - timestamps of records in songplays broken down into specific units
    - *start_time, hour, day, week, month, year, weekday*

To run the ```create_tables.py``` script, open a terminal window and run the following command:
```bash
python create_tables.py
```

## ETL Pipeline

The ```etl.py``` script implements an ETL pipeline to extract data from the log files and inserts the data into the appropriate tables.
To run the ```etl.py``` script, open a terminal window and run the following command:
```bash
python etl.py
```

The ```sql_queries.py``` script contains all of the required SQL queries and statements to create the tables and to insert data. The ```create_tables.py``` and ```etl.py``` scripts import the SQL, so the ```sql_queries.py``` script does not need to run directly.
