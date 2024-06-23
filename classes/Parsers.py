import json
import time

from db.db import Database
from utils.utils import api_get_question_info
from utils.extrapolate import predict_question_rating

class Parser:
    def __init__(self):
        self.db: Database = Database()

    def parse_question_bank(self):
        with open("data/user.txt", "r+") as f:
            user_data = json.load(f)

        all_questions = user_data["stat_status_pairs"]

        for question in all_questions:
            question_id = int(question["stat"]["frontend_question_id"])
            title_slug = question["stat"]["question__title_slug"]
            total_acs = question["stat"]["total_acs"]
            total_submitted = question["stat"]["total_submitted"]

            question = self.db.find_question_by_question_id(question_id)

            if question:
                print(f"question id {question_id} parsed already, skipping")

                time.sleep(0.1 * 1) # so that we don't hit cluster with too many req/s
                continue

            r = api_get_question_info(title_slug)
            if r.status_code != 200:
                print(f"bad status code {r.status_code}: {r.text}")

                with open("data/error_slugs.txt", 'a') as file:
                    file.write(f"{title_slug}\n")

                time.sleep(10 * 1) # 10 seconds between each call
                continue

            print(f"response successfully received for question id {question_id}")

            question = r.json()
            question["questionId"] = int(question["questionId"])
            question["questionFrontendId"] = int(question["questionFrontendId"])
            question["total_acs"] = total_acs
            question["total_submitted"] = total_submitted

            self.db.insert_question(question)

            time.sleep(10 * 1) # 10 seconds between each call

    def build_ratings(self):
        # this method will take some time to run, as we are predicting using
        # the model on many questions

        self.db.delete_ratings_db()

        # preload ratings into a dictionary first
        ratings = dict()

        with open("data/ratings.txt", encoding="utf8") as f:
            next(f) # skip header line

            for line in f:
                rating, question_id, _, _, _, _, _ = line.split("\t")

                ratings[int(question_id)] = float(rating)

        questions = self.db.return_all_raw_questions()

        ratings_data = [{
            "question_id": question["questionFrontendId"],
            "title": question["questionTitle"],
            "title_slug": question["titleSlug"],
            "predicted_rating": predict_question_rating(question),
            "zerotrac_rating": ratings.get(question["questionFrontendId"], -1)
        } for question in questions]

        self.db.insert_ratings_db(ratings_data)

        print(f"Successfully pushed questions ratings to database")