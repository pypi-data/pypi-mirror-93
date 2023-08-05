from .db import Database
from typing import Dict, Union, List, Optional
from .types import ALL_VALID_TYPES
import duckdb
from dataclasses import dataclass


class ColumnDetails(object):

    def __init__(self, name, type_, constraints: Optional[List[str]] = None):
        self.name = name
        assert type_ in ALL_VALID_TYPES, f'error: {type_} is not a valid type'
        self.type_ = type_
        if constraints is None:
            constraints = []

    @property
    def constraints_sql(self) -> str:
        return f'{self.name} {self.type_}'


class Table(object):

    @classmethod
    def is_valid_type(cls, type_):
        # https://duckdb.org/docs/sql/data_types/overview
        return type_ in ALL_VALID_TYPES

    @classmethod
    def table_exists(cls, db: Database, table_name):
        try:
            _ = db.conn.table(table_name)
            return True
        except Exception:
            return False

    @classmethod
    def normalize_columns_input(cls, fields) -> List[ColumnDetails]:
        new_fields: List[ColumnDetails] = []
        if isinstance(fields, dict):
            for k, v in fields.items():
                new_fields.append(ColumnDetails(k, v.upper()))
        else:
            assert isinstance(fields, list)
            assert isinstance(fields[0], ColumnDetails)
            new_fields = fields
        return new_fields

    @classmethod
    def create_table(cls, db: Database, table_name, fields: Union[List[ColumnDetails], Dict[str, str]]):
        assert len(fields) >= 1
        fields: List[ColumnDetails] = cls.normalize_columns_input(fields)
        sql = f'CREATE TABLE {table_name} ({", ".join([x.constraints_sql for x in fields])});'
        db.conn.execute(sql)

    @classmethod
    def get_or_create(cls, path_or_db, table_name, columns: Union[List[ColumnDetails], Dict[str, str]], read_only=False) -> 'Table':
        # columns is a dict of column_name => column_types
        # TODO check if table exists
        if isinstance(path_or_db, str):
            db = Database(path_or_db, read_only=read_only)
        else:
            assert isinstance(path_or_db, Database)
            db = path_or_db
        if cls.table_exists(db, table_name):
            # TODO - ensure all the columns exist
            table = Table(db, table_name)
            fields: List[ColumnDetails] = cls.normalize_columns_input(columns)
            for col in fields:
                if col.name not in table.cached_columns:
                    table.add_column(col)
        else:
            cls.create_table(db, table_name, columns)
            table = Table(db, table_name)
        return table

    # TODO - a way to add full text search
    def __init__(self, db: Database, table_name: str):
        self.conn = db.conn
        self.db = db
        self.table_name = table_name
        self.table = self.conn.table(self.table_name)
        self.cached_columns = self.columns

    @property
    def columns(self) -> List[str]:
        # returns dict of column_name => column_type
        cols = list(self.table.columns)
        self.cached_columns = cols
        return self.cached_columns

    def column_type(self, column):
        types = self.table.types
        for idx, c in self.table.columns:
            if c == column:
                return types[idx]
        raise Exception('error - should not get here')

    def add_column(self, column: ColumnDetails):
        # https://duckdb.org/docs/sql/statements/alter_table
        result = self.conn.execute(f'ALTER TABLE {self.table_name} ADD COLUMN {column.constraints_sql()} ;')
        _ = self.columns
        return result

    def has_column(self, column):
        return column in self.columns

    def insert(self, row: Union[dict, list]):
        return self.insert_many([row])

    def all(self):
        for row_list in self.conn.execute(f'SELECT * FROM {self.table_name};').fetchall():
            row = {}
            for idx, val in enumerate(row_list):
                if val is None:
                    continue
                row[self.cached_columns[idx]] = val
            yield row

    def insert_many(self, rows: [List[Union[dict, list]]]):
        final_rows = []
        for row in rows:
            if isinstance(row, list):
                assert len(row) == len(self.cached_columns)
                row_result = row
            else:
                row_result = []
                for k, v in row.items():
                    assert k in self.cached_columns
                for c in self.cached_columns:
                    if c in row:
                        row_result.append(row[c])
                    else:
                        row_result.append(None)
            final_rows.append(row_result)
        self.conn.executemany(f"INSERT INTO {self.table_name} VALUES ({','.join('?' for _ in self.cached_columns)})", final_rows)

