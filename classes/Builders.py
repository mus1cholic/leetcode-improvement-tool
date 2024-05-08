import json
import time

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .Tags import TagsStatistics
from data import secret as secret

import utils.utils as utils
import utils.constants as constants

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
        # to build association between rating, question, and tags. since we are
        # essentially doing a complicated join, we can utilize mongoDB's aggregation
        # functions to complete this step instead of doing it locally

        start_time = time.perf_counter()

        pipeline = [
            {
                '$unset': ['questionId','question', 'exampleTestcases', 'hints',
                           'solution', 'companyTagStats', 'likes', 'dislikes',
                           'similarQuestions', 'total_acs', 'total_submitted']
            },
            {
                '$addFields': {
                    'questionFrontendId_int': {'$toInt': '$questionFrontendId'}
                }
            },
            {
                '$lookup': {
                    'from': 'ratings_data',
                    'localField': 'questionFrontendId_int',
                    'foreignField': 'question_id',
                    'as': 'joined_docs'
                }
            },
            {
                '$addFields': {
                    'joined_docs': {
                        '$cond': {
                            # TODO: There are questions in questions_data.json that aren't
                            # in ratings.txt. For now, we skip those because we haven't
                            # developed a way to accurately calculate rating for those.
                            # Eventually we will do this through best-fit line of accepted
                            # submission percentage
                            'if': {'$eq': ['$joined_docs', []]},  # Check if joined_docs is empty
                            'then': [{'rating': 0}],  # If empty, set rating to 0 in a new object in the array
                            'else': '$joined_docs'  # Otherwise, keep it as is
                        }
                    }
                }
            },
            {
                '$unwind': {
                    'path': '$joined_docs',
                    'preserveNullAndEmptyArrays': True  # Preserve documents even if joined_docs is empty
                }
            },
            {
                '$replaceRoot': {
                    'newRoot': {
                        '$mergeObjects': ['$joined_docs', '$$ROOT']  # Merge fields of col1 and joined_docs
                    }
                }
            },
            {
                '$unset': ['questionFrontendId_int', 'joined_docs', '_id']
            },
            {
                '$project': {
                    "question_id": "$questionFrontendId",
                    "title": "$questionTitle",
                    "title_slug": "$titleSlug",
                    "link": "$link",
                    "rating": "$rating",
                    "difficulty": "$difficulty",
                    "premium": "$isPaidOnly",
                    "tags": "$topicTags"
                }
            },
            {
                '$out': 'rating_question_tag_data' # this replaces the entire collection
            }
        ]

        self.questions_data_collection.aggregate(pipeline)

        end_time = time.perf_counter()

        print(f"Successfully pushed to questions_rating database, took {end_time - start_time}s")

    def build_user_data(self, user_discord_id: int, user_discord_username: str, user_data_txt: str):
        """
        {
            "discord_id": long,
            "discord_username": str, !!
            "lc_user_name": str,
            "contest_rating": float,
            "questions_rating": float, !!
            "projected_rating": float, !!
            "completed_questions": [question_ids],
            "tags": { !!
                "tag_slug": {
                    "tag_rating": float,
                    "completed_questions": [question_ids]
                }
            }
        }
        """
        # if contest_rating is 0, projected rating is 70th percentile of questions_rating
        # if contest_rating < questions_rating, projected rating = 0.75*questions_rating + 0.25*contest_rating
        # if contest_rating >= questions_rating, projected rating = 0.75*contest_rating + 0.25*questions_rating

        user_data = json.loads(user_data_txt)

        lc_username = user_data["user_name"]

        # sanity check
        if lc_username == "":
            # TODO: put some error message here back
            pass

        user_contest_data_request = utils.api_get_user_contest_info(lc_username)
        user_contest_data = user_contest_data_request.json()
        user_contest_rating = user_contest_data.get("contestRating", constants.CONTEST_RATING_DEFAULT)

        user_questions_stats = user_data["stat_status_pairs"]

        completed_questions = []

        for question in user_questions_stats:
            question_id = question["stat"]["frontend_question_id"]
            completed_status = question["status"]
            # total_acs = question["stat"]["total_acs"]
            # total_submitted = question["stat"]["total_submitted"]

            if completed_status != "ac":
                continue

            completed_questions.append(question_id)

        completed_questions.sort()

        # Calculate individual tag rating

        user_tags_stats = TagsStatistics(completed_questions, rating_question_data)
        user_tags_stats.build_tag_data()
        user_tags = user_tags_stats.to_object()

        user_data_structure = {
            "discord_id": user_discord_id,
            "discord_username": user_discord_username,
            "lc_user_name": lc_username,
            "contest_rating": user_contest_rating,
            "questions_rating": float, # TODO
            "projected_rating": float, # TODO
            "completed_questions": [completed_questions],
            # "tags": { !!
            #     "tag_slug": {
            #         "tag_rating": float,
            #         "completed_questions": [question_ids]
            #     }
            # }
        }

        print(user_data_structure)

        return

        self.user_data_collection.insert_one(user_data_structure)

        print(f"Successfully built user database")

    def check_user_exist(self, user_id: int):
        result = self.user_data_collection.find_one({"discord_id": user_id})

        return result != None