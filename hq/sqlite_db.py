import sqlite3

def get_readonly_connection(db_path):
    return sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
