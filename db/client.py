from pymongo import MongoClient

db_client = MongoClient("mongodb://localhost:27017/")
db = db_client["to-do-proyect"]