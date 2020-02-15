import argparse
import git
import pymongo

parser = argparse.ArgumentParser(description='Sync mongodb database to match git repository.')
parser.add_argument('git_repository', type=str, help='a git repository to sync')
parser.add_argument('mongo_database', type=str, help='the mongodb database')
parser.add_argument('-m', '--mongo_host', type=str, help='mongodb hostname', default='localhost')
parser.add_argument('-p', '--mongo_port', type=int, help='mongodb port', default=27017)
args = parser.parse_args()

git_repo = args.git_repository
print('Cloning git repository:', git_repo)

mongo_host = args.mongo_host
mongo_port = args.mongo_port
mongo_db = args.mongo_database
print('Connecting to MongoDB database:', mongo_host, mongo_port, mongo_db)
client = pymongo.MongoClient(mongo_host, mongo_port)
database = client[mongo_db]
