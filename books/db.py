from pymongo import MongoClient


# mui gio
client = MongoClient('mongodb://localhost:27017', tz_aware=True)

client = MongoClient("mongodb://localhost:27017")
db = client['mylibrary']
books_collection = db['books']
borrows_collection = db['borrows']

