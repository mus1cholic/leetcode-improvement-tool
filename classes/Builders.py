import json
import time

from .Users import User

from db.db import Database

"""
This class contains class methods specifically used to modify and check .json files
"""

class Builder:
    def __init__(self):
        self.db: Database = Database()

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
                    'question_id': {'$toInt': '$questionFrontendId'}
                }
            },
            {
                '$lookup': {
                    'from': 'ratings_data',
                    'localField': 'question_id',
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
                '$addFields': {
                    "tags": {
                        "$map": {
                            "input": "$topicTags",
                            "as": "tag",
                            "in": "$$tag.slug"
                        }
                    }
                }
            },
            {
                '$unset': ['questionFrontendId', 'joined_docs', '_id', 'topicTags']
            },
            {
                '$project': {
                    "question_id": "$question_id",
                    "title": "$questionTitle",
                    "title_slug": "$titleSlug",
                    "link": "$link",
                    "rating": "$rating",
                    "difficulty": "$difficulty",
                    "premium": "$isPaidOnly",
                    "tags": "$tags"
                }
            },
            {
                '$out': 'rating_question_tag_data' # this replaces the entire collection
            }
        ]

        self.db.questions_data_collection.aggregate(pipeline)

        end_time = time.perf_counter()

        print(f"Successfully pushed to questions_rating database, took {end_time - start_time}s")

    def build_user_data(self, user_discord_id: int, user_discord_username: str, user_data_txt: str):
        user = User(user_discord_id, user_discord_username, user_data_txt, self.db.rating_question_tag_data_collection)
        user.build_user()

        user_data_structure = user.output_user_data_structure()

        self.db.user_data_collection.insert_one(user_data_structure)

        print(f"Successfully built user database for user {user_discord_username}")

    def check_user_exist(self, user_id: int):
        result = self.db.user_data_collection.find_one({"discord_id": user_id})

        return result != None