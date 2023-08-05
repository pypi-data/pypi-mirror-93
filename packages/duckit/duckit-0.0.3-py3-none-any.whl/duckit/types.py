
# https://duckdb.org/docs/sql/data_types/overview
SUPPORTED_TYPES = {
    'BIGINT': {'INT8', 'LONG'},
    'BOOLEAN': {'BOOL', 'LOGICAL'},
    'BLOB': {'BYTEA', 'BINARY', 'VARBINARY'},
    'DATE': {},
    'DOUBLE': {'FLOAT8', 'NUMERIC', 'DECIMAL'},
    'HUGEINT': {},
    'INTEGER': {'INT4', 'INT', 'SIGNED'},
    'REAL': {'FLOAT4', 'FLOAT'},
    'SMALLINT': {'INT2', 'SHORT'},
    'TIMESTAMP': {'DATETIME'},
    'TINYINT': {'INT1'},
    'VARCHAR': {'CHAR', 'BPCHAR', 'TEXT', 'STRING'},
}

ALL_VALID_TYPES = set()
for e in SUPPORTED_TYPES.values():
    for e2 in e:
        ALL_VALID_TYPES.add(e2)

