import json
import time

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .Tags import TagsStatistics
from data import secret as secret

import utils.utils as utils

"""
This class contains class methods specifically used to modify and check .json files
"""

class Builder:
    def __init__(self):
        client = MongoClient(secret.MONGO_DB_URI, server_api=ServerApi('1'))

        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        db = client["leetcode_improvement_tool"]

        self.user_data_collection = db["user_data"]
        self.ratings_data_collection = db["ratings_data"]
        self.questions_data_collection = db["questions_data"]
        self.rating_question_tag_data_collection = db["rating_question_tag_data"]

    @staticmethod
    def build_question_ratings():
        # input: ratings.txt
        # output: ratings.json

        """
        {
            "question_id": {
                "question_id": int,
                "title": str,
                "title_slug": str,
                "rating": float
            }
        }
        """

        start_time = time.perf_counter()

        ratings_data = {}

        with open("data/ratings.txt", encoding="utf8") as f:
            next(f) # skip header line

            for line in f:
                rating, question_id, title, _, title_slug, _, _ = line.split("\t")

                ratings_structure = {
                    "question_id": int(question_id),
                    "title": title,
                    "title_slug": title_slug,
                    "rating": float(rating)
                }

                ratings_data[question_id] = ratings_structure

        ratings_data = dict(sorted(ratings_data.items()))

        with open("data/ratings.json", "w+") as f:
            json.dump(ratings_data, f, indent=4, separators=(',', ': '))

        end_time = time.perf_counter()

        print(f"Successfully parsed questions ratings from ratings.txt, took {end_time - start_time}s")

    def build_question_rating_data(self):
        # now that we have question bank, we can simplify all of the questions
        # to build association between rating, question, and tags

        # input: ratings.json, questions_data.json
        # output: rating_question_tag.json

        # remember that these are lists
        ratings_data = self.ratings_data_collection.find()
        questions_data = self.questions_data_collection.find()

        rating_question_tag_data = []

        for question in questions_data:
            # print(question)

            question_id = question["questionFrontendId"]
            title = question["questionTitle"]
            title_slug = question["titleSlug"]
            link = question["link"]
            difficulty = question["difficulty"]
            premium = question["isPaidOnly"]
            tags = question["topicTags"] # TODO, make this a Tags object

            # TODO: There are questions in questions_data.json that aren't
            # in ratings.txt. For now, we skip those because we haven't
            # developed a way to accurately calculate rating for those.
            # Eventually we will do this through best-fit line of accepted
            # submission percentage
            # TODO: this is incredibly slow, because we are calling the db's find_one
            # method for each question. Find a way to d othis faster
            rating = self.ratings_data_collection.find_one({'question_id': int(question_id)})

            if rating == None:
                continue

            question_object_structure = {
                "question_id": question_id,
                "title": title,
                "title_slug": title_slug,
                "link": link,
                "rating": rating,
                "difficulty": difficulty,
                "premium": premium,
                "tags": tags,
            }

            rating_question_tag_data.append(question_object_structure)

        self.rating_question_tag_data_collection.insert_many(rating_question_tag_data)

        print(f"Successfully pushed to questions_rating database")

    @staticmethod
    def build_user_data(user_discord_id: str, user_data_txt: str):
        # using user.txt, builds user database

        # input: user.txt, rating_question_tag.json, user_data.json
        # output: user_data.json

        """
        {
            "user_name": {
                "user_name": str,
                "contest_rating": float,
                "completed_questions": [question_id],
                "tags": {
                    "tag_slug": {
                        "tag_slug": str,
                        "tag_rating": float
                    }
                }
            }
        }
        """
        
        start_time = time.perf_counter()

        with open("data/rating_question_tag.json", "r+") as f:
            rating_question_data = json.load(f)

        # with open("data/user.txt", "r+") as f:
        #     user_data = json.load(f)

        user_data = json.loads(user_data_txt)

        with open("data/user_data.json", "r+") as f:
            write_data = json.load(f)

        lc_username = user_data["user_name"]

        # TODO: find a way to not call this in a Builder, we want
        # parsing calls to only be called in Parsers
        r = utils.api_get_user_contest_info(lc_username)
        user_contest_data = r.json()

        contest_rating = user_contest_data["contestRating"] if "contestRating" in user_contest_data else 0
        all_questions = user_data["stat_status_pairs"]

        completed_questions = []

        for question in all_questions:
            question_id = question["stat"]["frontend_question_id"]
            completed_status = question["status"]
            total_acs = question["stat"]["total_acs"]
            total_submitted = question["stat"]["total_submitted"]

            if completed_status != "ac":
                continue

            completed_questions.append(question_id)

        completed_questions.sort()

        # Calculate individual tag rating

        user_tags_stats = TagsStatistics(completed_questions, rating_question_data)
        user_tags_stats.build_tag_data()
        user_tags = user_tags_stats.to_object()

        user_data_structure = {
            "user_name": lc_username,
            "contest_rating": contest_rating,
            "completed_questions": completed_questions,
            "tags": user_tags
        }

        write_data[user_discord_id] = user_data_structure

        with open("data/user_data.json", "w+") as f:
            json.dump(write_data, f, indent=4, separators=(',', ': '))

        end_time = time.perf_counter()

        print(f"Successfully built user database, took {end_time - start_time}s")

    @staticmethod
    def clean_up_data():
        # first thing is to make sure rating_question_tag is sorted by key
        with open("data/rating_question_tag.json", "r+") as f:
            rating_question_data = json.load(f)

        write_data = dict(sorted(rating_question_data.items(), key=lambda x: int(x[0])))

        with open("data/rating_question_tag.json", "w+") as f:
            json.dump(write_data, f, indent=4, separators=(',', ': '))

    @staticmethod
    def check_user_exist(user_id: str):
        with open("data/user.txt", "r+") as f:
            user_data = json.load(f)

        return user_id in user_data
    
    @staticmethod
    def temp_push_data():
        client = MongoClient(secret.MONGO_DB_URI, server_api=ServerApi('1'))

        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        # DB name
        db = client["leetcode_improvement_tool"]

        # collection (table) name
        questions_data_collection = db["user_data"]

        # document (SQL record)
        with open("data/user_data.json", "r+") as f:
            user_data = json.load(f)

        # ratings_arr = []

        # for rating in ratings_data:
        #     rating_object = ratings_data[rating]

        #     ratings_arr.append(rating_object)

        # ratings_arr.sort(key=lambda x: x["question_id"])

        x = questions_data_collection.insert_many(user_data)

        print(x.inserted_ids)