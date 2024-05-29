import json
from google.colab import drive
import pandas as pd

# Mount Google Drive
drive.mount('/content/drive')

json_file_path = '/content/users.json'

# Function to parse JSON file
def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            data.append(json.loads(line))
    return data

# Parse the JSON file
users_data = parse_json_file(json_file_path)

users_df = pd.json_normalize(users_data, max_level=1)

users_df = users_df.rename(columns={'_id.$oid': 'userid', 'createdDate.$date': 'createDate', 'lastLogin.$date': 'lastLogin'})

users_df['createDate'] = pd.to_datetime(users_df['createDate'], unit='ms')

users_df['lastLogin'] = pd.to_datetime(users_df['lastLogin'], unit='ms')

table_name = 'Users'

# Generate SQL INSERT statements
sql_statements = []
for index, row in users_df.iterrows():
    values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in row.values])
    sql_statement = f"INSERT INTO {table_name} ({', '.join(users_df.columns)}) VALUES ({values});"
    sql_statements.append(sql_statement)

# Write SQL statements to a SQL file
sql_file_path = 'users.sql'
with open(sql_file_path, 'w') as f:
    for sql_statement in sql_statements:
        f.write(sql_statement + '\n')

print(f"DataFrame has been written to {sql_file_path}")