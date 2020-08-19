import pytest

import psycopg2

@pytest.fixture
def db_conn():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    return cur, conn

def test_cols_exist(db_conn):
    cur, conn = db_conn

    table_col_query = """select table_name, column_name
    from information_schema.columns
    where table_schema = 'public'
    order by table_name"""

    expect_cols = {
        'songplays': [
            'songplay_id',
            'start_time',
            'user_id',
            'level',
            'song_id',
            'artist_id',
            'session_id',
            'location',
            'user_agent'
        ],
        'users': [
            'user_id',
            'first_name',
            'last_name',
            'gender',
            'level',
        ],
        'songs': [
            'song_id',
            'title',
            'artist_id',
            'year',
            'duration'
        ],
        'artists': [
            'artist_id',
            'name',
            'location',
            'latitude',
            'longitude'
        ],
        'time': [
            'start_time',
            'hour',
            'day',
            'week',
            'month',
            'year',
            'weekday'
        ]
    }

    cur.execute(table_col_query)
    got_cols = {}
    for t, c in cur:
        if t in got_cols.keys():
            got_cols[t].append(c)
        else:
            got_cols[t] = [c]
    cur.close()
    conn.close()

    for table in expect_cols:
        for col in expect_cols[table]:
            assert col in got_cols[table]

def test_tables_exist(db_conn):
    cur, conn = db_conn
    table_name_query = """select table_name
    from information_schema.tables
    where table_schema = 'public'"""

    expect_tables = [
        'songplays',
        'users',
        'songs',
        'artists',
        'time'
    ]

    cur.execute(table_name_query)
    got_tables = [t for t, in cur]
    cur.close()
    conn.close()

    for table in expect_tables:
        assert table in got_tables
