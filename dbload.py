import csv
import db
import os

demo_data_path = './demo_data/'

query = ""
with open(demo_data_path + "load_tables.sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

tsv_files = []
for filename in os.listdir(demo_data_path):
    if filename.endswith('.tsv'):
        tsv_files.append(filename)

for tsv_file in tsv_files:
    table_name = tsv_file[:-4]
    with open(demo_data_path + table_name + ".tsv", 'r', newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        with open(demo_data_path + table_name + ".sql", 'w') as sqlfile:
            for row in reader:
                values = ', '.join(f"'{value}'" for value in row.values())
                if "''" in values:
                    values = values.replace("''", "'0'")
                if "'s Day" in values:
                    values = values.replace("'s Day", "''s Day")
                sqlfile.write(f"INSERT INTO {table_name} ({', '.join(row.keys())}) VALUES ({values});\n")


query = ""
with open(demo_data_path + "date" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

query = ""
with open(demo_data_path + "city" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

query = ""
with open(demo_data_path + "store" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

query = ""
with open(demo_data_path + "product" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

query = ""
with open(demo_data_path + "category" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

query = ""
with open(demo_data_path + "incategory" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

query = ""
with open(demo_data_path + "holiday" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

query = ""
with open(demo_data_path + "transaction" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

query = ""
with open(demo_data_path + "discount" + ".sql", 'r') as sqlfile:
    query = sqlfile.read()
db.insert(query)

print("Demo data loading complete.")

