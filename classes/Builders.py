import time

from classes.Users import User
from db.db import Database

"""
This class contains class methods specifically used to modify and check .json files
"""

class Builder:
    def __init__(self):
        self.db: Database = Database()

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
                           'similarQuestions']
            },
            {
                '$addFields': {
                    'question_id': '$questionFrontendId'
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
                    "predicted_rating": "$predicted_rating",
                    "zerotrac_rating": "$zerotrac_rating",
                    "difficulty": "$difficulty",
                    "total_acs": "$total_acs",
                    "total_submitted": "$total_submitted",
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

        self.db.insert_user(user_data_structure)