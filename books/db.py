from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client['mylibrary']
books_collection = db['books']
borrows_collection = db['borrows']