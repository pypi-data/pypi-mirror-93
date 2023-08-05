"""
https://duckdb.org/docs/api/python
"""
import duckdb


class Database(object):
    IN_MEMORY = ':memory:'

    def __init__(self, path: str, read_only: bool = False):
        self.conn = duckdb.connect(database=path, read_only=read_only)


