import requests
import pandas as pd
import pyodbc
import sys

# Step 1: Fetch all data from the World Bank Data360 API (handle pagination)
base_url = "https://data360api.worldbank.org/data360/data"
all_rows = []
page = 0
page_size = 1000  # Increase page size to 1000 for faster data fetching

# Get total row count first
params_count = {
    "DATABASE_ID": "WB_WDI",
    "$format": "json",
    "$top": 1,
    "$skip": 0
}
try:
    response_count = requests.get(base_url, params=params_count)
    response_count.raise_for_status()
    data_count = response_count.json()
    total_rows = data_count.get("count", 0)
    total_pages = (total_rows + page_size - 1) // page_size if total_rows else None
    if total_pages:
        print(f"Total rows reported by API: {total_rows}")
        print(f"Total pages to fetch: {total_pages}")
    else:
        print("Could not determine total rows/pages from API.")
except Exception as e:
    print(f"Error fetching row count: {e}")
    total_pages = None

max_pages = 8  # Only fetch 8 pages for testing
while True:
    if page >= max_pages:
        print(f"Reached max_pages={max_pages}, stopping early for test.")
        break
    params = {
        "DATABASE_ID": "WB_WDI",
        "$format": "json",
        "$top": page_size,
        "$skip": page * page_size
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching page {page + 1}: {e}")
        break
    if "value" in data and data["value"]:
        all_rows.extend(data["value"])
        if total_pages:
            print(f"Fetched page {page + 1} of {total_pages}, total rows so far: {len(all_rows)}")
        else:
            print(f"Fetched page {page + 1}, total rows so far: {len(all_rows)}")
        if len(data["value"]) < page_size:
            break  # Last page
        page += 1
    else:
        break

df = pd.DataFrame(all_rows)
print(f"Total rows fetched: {len(df)}")
print(df.head())

# Step 2: Connect to SQL Server and insert data
# Use Windows Authentication (Trusted_Connection)
server = 'localhost\\SQLEXPRESS'
database = 'WorldBankDB_TEST'
table = 'EconomicData_TEST'

# Step 2a: Connect to master and create database if it doesn't exist
try:
    conn_str_master = f"DRIVER={{SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes;"
    conn_master = pyodbc.connect(conn_str_master, autocommit=True)
    cursor_master = conn_master.cursor()
    cursor_master.execute(f"IF DB_ID('{database}') IS NULL CREATE DATABASE {database}")
    print(f"Database '{database}' checked/created.")
    cursor_master.close()
    conn_master.close()
except Exception as e:
    print(f"Error creating/checking database: {e}")
    sys.exit(1)

# Step 2b: Connect to WorldBankDB
try:
    conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print(f"Connected to database '{database}'.")
except Exception as e:
    print(f"Error connecting to database '{database}': {e}")
    sys.exit(1)

# Step 2c: Create table if it doesn't exist (auto schema for all columns)
try:
    # Dynamically build CREATE TABLE statement from DataFrame columns
    sql_types = {
        'int64': 'BIGINT',
        'float64': 'FLOAT',
        'object': 'NVARCHAR(MAX)',
        'bool': 'BIT',
        'datetime64[ns]': 'DATETIME',
    }
    columns = []
    for col, dtype in df.dtypes.items():
        sql_type = sql_types.get(str(dtype), 'NVARCHAR(MAX)')
        # SQL Server column names cannot have spaces or special chars, so sanitize
        col_clean = col.replace(' ', '_').replace('-', '_').replace('.', '_')
        columns.append(f"[{col_clean}] {sql_type}")
    create_table_sql = f"""
        IF OBJECT_ID('{table}', 'U') IS NULL
        CREATE TABLE {table} (
            {',\n            '.join(columns)}
        )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print(f"Table '{table}' checked/created with all columns.")
except Exception as e:
    print(f"Error creating/checking table: {e}")
    conn.close()
    sys.exit(1)

# Step 2d: Insert data (all columns)
inserted = 0
col_names = [col.replace(' ', '_').replace('-', '_').replace('.', '_') for col in df.columns]
placeholders = ','.join(['?' for _ in col_names])
insert_sql = f"INSERT INTO {table} ({','.join(f'[{c}]' for c in col_names)}) VALUES ({placeholders})"
for row in df.itertuples(index=False, name=None):
    try:
        cursor.execute(insert_sql, *row)
        inserted += 1
        if inserted % 1000 == 0:
            print(f"Inserted {inserted} rows...")
    except Exception as e:
        print(f"Error inserting row: {e}")
        continue
conn.commit()
conn.close()
print(f"Data inserted into SQL Server. Total rows inserted: {inserted}")