# HPE_CTY2023
Contains the files representing my final implementation of the project work at HPE CTY.

# Project Description
Program that captures and records all file modifications to a given directory into a cassandra database which can be later used for querying. 
Constructs a json file with the metadata of all files in a given directory known as initial.json.
Changes are recorded at every set interval (1 min by default) and saved in the format HH_MM_changes.json.
The json files are loaded into cassandra which provides a simple UI to search for file and returns its latest metadata and modification record.

# Instructions to run
Modify the path in changes.py to your required directory, specify the path where the json files need to be stored and run it.
Run cassandra_queries.py after modifying the default path with the location where json files are being stored.
Run queries.py and input the required filename to view its metadata and modification record. 


