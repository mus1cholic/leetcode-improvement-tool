from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from data import secret as secret

class Database(object):
    client = None

    db = None

    user_data_collection = None
    ratings_data_collection = None
    questions_data_collection = None
    rating_question_tag_data_collection = None

    def __init__(self):
        if Database.client == None:
            Database.client = MongoClient(secret.MONGO_DB_URI, server_api=ServerApi('1'))

            try:
                Database.client.admin.command('ping')
                print("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                print(e)

        Database.db = Database.client["leetcode_improvement_tool"]

        Database.user_data_collection = Database.db["user_data"]
        Database.ratings_data_collection = Database.db["ratings_data"]
        Database.questions_data_collection = Database.db["questions_data"]
        Database.rating_question_tag_data_collection = Database.db["rating_question_tag_data"]

    @classmethod
    def find_user(cls, discord_user_id: int):
        query = {
            "discord_id": discord_user_id
        }

        result = cls.user_data_collection.find_one(query)

        return result
    
    @classmethod
    def find_question(cls, question_id: int):
        query = {
            "question_id": question_id
        }

        result = cls.rating_question_tag_data_collection.find_one(query)

        return result
    
    @classmethod
    def find_problems(cls, rating_min: float, rating_max: float):
        query = {
            "rating": {
                "$gte": rating_min,
                "$lte": rating_max
            }
        }

        result = cls.rating_question_tag_data_collection.distinct("question_id", query)

        return result