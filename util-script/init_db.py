import sqlite3

if __name__ == "__main__":
    db = sqlite3.connect(
            "cache.sqlite3", detect_types=sqlite3.PARSE_DECLTYPES
        )
    db.row_factory = sqlite3.Row

    with open("schema.sql") as f:
        db.executescript(f.read())
