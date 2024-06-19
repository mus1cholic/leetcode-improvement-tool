import json
import time

from db.db import Database
from utils.utils import api_get_question_info
from utils.extrapolate import predict_question_rating

class Parser:
    def __init__(self):
        self.db: Database = Database()

    def parse_singular_question(self, title_slug):
        # util function for just calling the api once on a single question, for maybe
        # when the api throws an error and gives bad response
        
        with open("data/user.txt", "r+") as f:
            user_data = json.load(f)

        r = api_get_question_info(title_slug)

        question = r.json()
        question["questionId"] = int(question["questionId"])
        question["questionId"] = int(question["questionFrontendId"])
        # TODO: fix these
        # question["total_acs"] = total_acs
        # question["total_submitted"] = total_submitted

        self.db.insert_question(question)

    def parse_question_bank(self):
        with open("data/user.txt", "r+") as f:
            user_data = json.load(f)

        self.db.delete_questions_db()

        all_questions = user_data["stat_status_pairs"]

        for question in all_questions:
            question_id = int(question["stat"]["frontend_question_id"])
            title_slug = question["stat"]["question__title_slug"]
            total_acs = question["stat"]["total_acs"]
            total_submitted = question["stat"]["total_submitted"]

            question = self.db.find_question(question_id)

            if question:
                print(f"question id {question_id} parsed already, skipping")
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
            question["questionId"] = int(question["questionFrontendId"])
            question["total_acs"] = total_acs
            question["total_submitted"] = total_submitted

            self.db.insert_question(question)

            time.sleep(10 * 1) # 10 seconds between each call