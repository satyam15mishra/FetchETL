import json
from google.colab import drive
import pandas as pd

# Mount Google Drive
drive.mount('/content/drive')

json_file_path = '/content/brands.json'

# Function to parse JSON file
def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            data.append(json.loads(line))
    return data

# Parse the JSON file
brands_data = parse_json_file(json_file_path)

df = pd.json_normalize(brands_data, max_level=2)

df = df.rename(columns={'_id.$oid': '_id'})

df = df.rename(columns={'cpg.$ref': 'cpg_ref'})

df.drop('cpg.$id.$oid', axis = 1, inplace = True)

table_name = 'Brands'

# Generate SQL INSERT statements
sql_statements = []
for index, row in df.iterrows():
    values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in row.values])
    sql_statement = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({values});"
    sql_statements.append(sql_statement)

# Write SQL statements to a SQL file
sql_file_path = 'brands.sql'
with open(sql_file_path, 'w') as f:
    for sql_statement in sql_statements:
        f.write(sql_statement + '\n')

print(f"DataFrame has been written to {sql_file_path}")