import json
import time

from .Tags import Tag

import utils.utils as utils

"""
This class contains class methods specifically used to build .json files
"""

class Builder:
    def __init__(self):
        pass

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

    @staticmethod
    def build_question_rating_data():
        # now that we have question bank, we can simplify all of the questions
        # to build association between rating, question, and tags

        # input: ratings.json, questions_data.json
        # output: rating_question_tag.json

        start_time = time.perf_counter()

        with open("data/ratings.json", "r+") as f:
            ratings_data = json.load(f)

        with open("data/questions_data.json", "r+") as f:
            questions_data = json.load(f)

        questions_data = list(questions_data)
        write_data = {}

        for question in questions_data:
            question_id = question["questionFrontendId"] # JSON only use strings as keys
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
            if str(question_id) not in ratings_data:
                continue

            rating = ratings_data[str(question_id)]["rating"]

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

            write_data[question_id] = question_object_structure

        with open("data/rating_question_tag.json", "w+") as f:
            json.dump(write_data, f, indent=4, separators=(',', ': '))

        end_time = time.perf_counter()

        print(f"Successfully built questions_rating database, took {end_time - start_time}s")

    @staticmethod
    def build_user_data():
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

        with open("data/user.txt", "r+") as f:
            user_data = json.load(f)

        with open("data/user_data.json", "r+") as f:
            write_data = json.load(f)

        user_name = user_data["user_name"]

        # TODO: find a way to not call this in a Builder, we want
        # parsing calls to only be called in Parsers
        r = utils.api_get_question_info(user_name)
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

        user_tags_stats = Tags.TagsStatistics(completed_questions, rating_question_data)
        user_tags_stats.build_tag_data()
        user_tags = user_tags_stats.to_object()

        user_data_structure = {
            "user_name": user_name,
            "contest_rating": contest_rating,
            "completed_questions": completed_questions,
            "tags": user_tags
        }

        write_data[user_name] = user_data_structure

        with open("data/user_data.json", "w+") as f:
            json.dump(write_data, f, indent=4, separators=(',', ': '))

        end_time = time.perf_counter()

        print(f"Successfully built user database, took {end_time - start_time}s")
