import json
import os
import tempfile
from argparse import ArgumentParser

from git import Repo
from pymongo import MongoClient

# Parse arguments
parser = ArgumentParser(description='Sync mongodb database to match git repository.')
parser.add_argument('git_repository', type=str, help='a git repository to sync')
parser.add_argument('mongo_database', type=str, help='the mongodb database')
parser.add_argument('-m', '--mongo_host', type=str, help='mongodb hostname', default='localhost')
parser.add_argument('-p', '--mongo_port', type=int, help='mongodb port', default=27017)
args = parser.parse_args()

# Clone repository
temp_dir = tempfile.mkdtemp()
git_repo = args.git_repository
print('Cloning git repository:', git_repo)
Repo.clone_from(git_repo, temp_dir)

# Populate file dictionary
print('Searching for files to sync')
files = {}
for dir_name, dir_names, file_names in os.walk(temp_dir):
    for subdir_name in dir_names:
        if subdir_name.startswith('.'):
            dir_names.remove(subdir_name)

    for file_name in file_names:
        if not file_name.startswith('.'):
            if dir_name in files:
                files[dir_name].append(file_name)
            else:
                files[dir_name] = [file_name]

# Read json files as dictionaries
print('Loading files to sync')
documents = {}
for dir_name in files:
    document_type = dir_name.split('\\')[-1]
    documents_of_type = []

    for file in files[dir_name]:
        json_file_path = os.path.join(dir_name, file)

        with open(json_file_path, 'r') as j:
            json_content = json.loads(j.read())
            documents_of_type.append(json_content)

    print('Loaded', len(documents_of_type), 'documents of type', document_type)
    documents[document_type] = documents_of_type

# Connect to MongoDB
mongo_host = args.mongo_host
mongo_port = args.mongo_port
mongo_db = args.mongo_database
print('Connecting to MongoDB database:', mongo_host, mongo_port, mongo_db)
client = MongoClient(mongo_host, mongo_port)
database = client[mongo_db]

# Write documents to database
print('Inserting documents into database')
for document_type in documents:
    print('Populating collection', document_type)
    database[document_type].drop()
    database[document_type].insert_many(documents[document_type])
print('Completed insert')
