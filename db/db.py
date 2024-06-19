import enum

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from data import secret as secret

# TODO: create enum class of fields
class DatabaseEnum(enum.StrEnum):
    pass

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
    def find_user_by_discord_id(cls, discord_user_id: int):
        query = {
            "discord_id": discord_user_id
        }

        result = cls.user_data_collection.find_one(query)

        return result
    
    @classmethod
    def find_user_by_leetcode_username(cls, lc_username: str):
        query = {# TODO: change this to username
            "lc_user_name": lc_username
        }

        result = cls.user_data_collection.find_one(query)

        return result
    
    @classmethod
    def update_user_field(cls, _id: int, field_name: str, field_val):
        query = {
            '_id': _id
        }
        pipeline = {
            '$set': {
                field_name: field_val
            }
        }

        result = cls.user_data_collection.update_one(query, pipeline)

        return result
    
    @classmethod
    def find_question_by_question_id(cls, question_id: int):
        query = {
            "questionFrontendId": question_id
        }

        result = cls.questions_data_collection.find_one(query)

        return result

    @classmethod
    def insert_user(cls, user_data_structure: dict):
        cls.user_data_collection.insert_one(user_data_structure)

    @classmethod
    def delete_user_by_discord_id(cls, discord_id: int):
        # must guarantee that the document exists first
        query = {
            "discord_id": discord_id
        }

        cls.user_data_collection.delete_one(query)
    
    @classmethod
    def return_all_questions(cls):
        # should only be using this once per session
        result = cls.rating_question_tag_data_collection.find()

        return result
    
    @classmethod
    def return_all_raw_questions(cls):
        # should only be using this once per session
        result = cls.questions_data_collection.find()

        return result
    
    @classmethod
    def insert_question(cls, data):
        cls.questions_data_collection.insert_one(data)
    
    @classmethod
    def insert_ratings_db(cls, data):
        # insert the entire ratings db
        cls.ratings_data_collection.insert_many(data)
    
    @classmethod
    def delete_ratings_db(cls):
        # deletes the entire ratings db, beware when using this
        cls.ratings_data_collection.delete_many({})

    @classmethod
    def delete_questions_db(cls):
        # deletes the entire questions db, beware when using this
        cls.questions_data_collection.delete_many({})