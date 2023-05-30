from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import os
import json

cluster = Cluster(['localhost'])
session = cluster.connect()

# Create table if it does not exist
session.execute("CREATE KEYSPACE IF NOT EXISTS files WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}")
session.execute("DROP TABLE IF EXISTS files.file_changes;")
session.execute("DROP TABLE IF EXISTS files.file_changes1;")
session.execute("DROP TABLE IF EXISTS files.initial;")


session.execute("""
    CREATE TABLE IF NOT EXISTS files.file_changes (
        timestamp text,
        inode_number text,
        file_name text,
        file_size int,
        path text,
        date_of_creation text,
        last_modified text,
        operation_type text,
        PRIMARY KEY (file_name, timestamp)
    )
""")


with open("C:/workspace/HPE/initial.json", 'r') as f:
        data = json.load(f)

# Insert each record into the database
timestamp = "0:0"
for inode, file_data in data.items():
    query = SimpleStatement("""
        INSERT INTO files.file_changes (
            timestamp, inode_number, file_name, file_size, path, date_of_creation,
            last_modified, operation_type
        ) VALUES (
            %(timestamp)s, %(inode)s, %(file_name)s, %(file_size)s, %(path)s, %(date_of_creation)s,
            %(last_modified)s, %(operation_type)s
        )
    """)
    session.execute(query, {
        'timestamp': timestamp,
        'inode': inode,
        'file_name': file_data['File name'],
        'file_size': file_data['File size'],
        'path': file_data['path'],
        'date_of_creation': file_data['Date of creation'],
        'last_modified': file_data['last modified'],
        'operation_type': file_data['operation type']
    })


# Read JSON data from a file
directory = 'C:/workspace/HPE/changes'
while True:
    for filename in os.listdir(directory):
        timestamp = filename.split('_')[0] + ':' + filename.split('_')[1]
        with open(os.path.join(directory, filename), 'r') as f:
            data = json.load(f)

    # Insert each record into the database
        for inode, file_data in data.items():
            query = SimpleStatement("""
                INSERT INTO files.file_changes (
                    timestamp, inode_number, file_name, file_size, path, date_of_creation,
                    last_modified, operation_type
                ) VALUES (
                    %(timestamp)s, %(inode)s, %(file_name)s, %(file_size)s, %(path)s, %(date_of_creation)s,
                    %(last_modified)s, %(operation_type)s
                )
            """)
            session.execute(query, {
                'timestamp': timestamp,
                'inode': inode,
                'file_name': file_data['File name'],
                'file_size': file_data['File size'],
                'path': file_data['path'],
                'date_of_creation': file_data['Date of creation'],
                'last_modified': file_data['last modified'],
                'operation_type': file_data['operation type']
            })
        os.remove(os.path.join(directory, filename))


# Prompt the user to enter a metadata parameter to search for

# Perform a query using the user-specified metadata parameter
