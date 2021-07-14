import sqlite3
import ast

from flask import current_app, g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """

    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        print("closing db")
        db.close()


def store_cache(fragility_set, sample_size, xy_set):
    id = fragility_set.id
    cache_db = get_db()
    cur = cache_db.cursor()
    # INSERT statement
    cur.execute("INSERT INTO cache (dfr3_id, sample_size, data) VALUES (:dfr3_id, :sample_size, :data)", 
        {'dfr3_id':id, 'sample_size': sample_size, 'data':str(xy_set)})
    
    cache_db.commit()
    return True

def check_cache(fragility_set, sample_size):
    xy_set = None
    id = fragility_set.id
    cache_db = get_db()
    cur = cache_db.cursor()
    cur.execute("SELECT data FROM cache WHERE dfr3_id = :dfr3_id AND sample_size = :sample_size", 
        {'dfr3_id': id, 'sample_size': sample_size})
    result = cur.fetchone()
    if result is not None:
        print("found cache")
        xy_set = ast.literal_eval(result['data'])
    return xy_set