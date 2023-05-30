from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import os
import json

cluster = Cluster(['localhost'])
session = cluster.connect()

print("Get the metadata and modifications of a file")
file = input('Enter filename whose details you want to track: ')
query = SimpleStatement("""
SELECT * FROM files.file_changes WHERE {metadata_param}=%({metadata_param})s ORDER BY timestamp DESC
""".format(metadata_param='file_name'))
result = session.execute(query, {'file_name': file}).all()
print('metadata: ')
print('file name:', result[0][0])
print('date of creation:', result[0][2])
print('file size:', result[0][3])
print('inode number:', result[0][4])
print('last modified:', result[0][5])
print('file path:', result[0][7])
print("")
print("Modification record: ")
for row in result:
    print(row[1], row[6], end=", ")
print("")