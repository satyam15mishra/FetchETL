import json
from google.colab import drive
import pandas as pd

# Mount Google Drive
drive.mount('/content/drive')

json_file_path = '/content/receipts.json'

# Function to parse JSON file
def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            data.append(json.loads(line))
    return data

# Parse the JSON file
receipts_data = parse_json_file(json_file_path)

# Modify the record_path argument to access the nested data
df = pd.json_normalize(receipts_data, max_level=1)

df = df.rename(columns={"pointsEarned": "receiptPointsEarned"})

# Convert list column to dictionary column
def convert_to_dict(lst):
    if isinstance(lst, list) and len(lst) > 0 and isinstance(lst[0], dict):
        return lst[0]
    else:
        return {}  # Return an empty dictionary if the element is not a list or the list is empty or the first element is not a dictionary

df['rewardsReceiptItemListDict'] = df['rewardsReceiptItemList'].apply(convert_to_dict)

df.drop('rewardsReceiptItemList', axis = 1, inplace = True)

receiptDF = pd.concat([df.drop(['rewardsReceiptItemListDict'], axis=1), df['rewardsReceiptItemListDict'].apply(pd.Series)], axis=1)
receiptDF = receiptDF.rename(columns = {"_id.$oid": "receipt_id", "createDate.$date": "createDate", "dateScanned.$date": "dateScanned", "finishedDate.$date": "finishedDate", "modifyDate.$date": "modifyDate", "pointsAwardedDate.$date": "pointsAwardedDate", "purchaseDate.$date": "purchaseDate"})

receiptDF['createDate'] = pd.to_datetime(receiptDF['createDate'], unit='ms')
receiptDF['dateScanned'] = pd.to_datetime(receiptDF['dateScanned'], unit='ms')
receiptDF['finishedDate'] = pd.to_datetime(receiptDF['finishedDate'], unit='ms')
receiptDF['modifyDate'] = pd.to_datetime(receiptDF['modifyDate'], unit='ms')
receiptDF['pointsAwardedDate'] = pd.to_datetime(receiptDF['pointsAwardedDate'], unit='ms')
receiptDF['purchaseDate'] = pd.to_datetime(receiptDF['purchaseDate'], unit='ms')

#receiptDF = receiptDF.rename(columns={receiptDF.columns[2]: 'init_PointsEarned'})
#receiptDF.head(5)

table_name = 'Receipts'

# Generate SQL INSERT statements
sql_statements = []
for index, row in receiptDF.iterrows():
    values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in row.values])
    sql_statement = f"INSERT INTO {table_name} ({', '.join(receiptDF.columns)}) VALUES ({values});"
    sql_statements.append(sql_statement)

# Write SQL statements to a SQL file
sql_file_path = 'receipts.sql'
with open(sql_file_path, 'w') as f:
    for sql_statement in sql_statements:
        f.write(sql_statement + '\n')

print(f"DataFrame has been written to {sql_file_path}")