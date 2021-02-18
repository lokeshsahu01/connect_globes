import pymongo
from bson import ObjectId
# Connected Database
connection = pymongo.MongoClient('localhost', 27017)

database = connection['seartzDB']


