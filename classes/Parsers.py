import json
import time

import utils.utils as utils

"""
This class contains class methods specifically used to parse data from leetcode api
"""

class Parser:
    def __init__(self):
        pass

    @staticmethod
    def parse_singular_question(title_slug="hopper-company-queries-i"):
        # util function for just calling the api once on a single question, for maybe
        # when the api throws an error and gives bad response

        r = utils.api_get_question_info(title_slug)
        data = r.json()

        with open("data/temp.json", "w+") as f:
            json.dump(data, f, indent=4, separators=(',', ': '))

    @staticmethod
    def parse_question_bank():
        with open("data/user.txt", "r+") as f:
            user_data = json.load(f)

        with open("data/ratings.json", "r+") as f:
            ratings_data = json.load(f)

        with open("data/questions_data.json") as f:
            questions_data = json.load(f)

        all_questions = user_data["stat_status_pairs"]

        for question in all_questions:
            question_id = question["stat"]["frontend_question_id"]
            title_slug = question["stat"]["question__title_slug"]
            total_acs = question["stat"]["total_acs"]
            total_submitted = question["stat"]["total_submitted"]

            # TODO: temp solution
            question_parsed_already = False
            for parsed_question in questions_data:
                if str(question_id) == parsed_question["questionFrontendId"]:
                    question_parsed_already = True
                    break
            if question_parsed_already:
                print(f"question id {question_id} parsed already, skipping")
                continue

            r = utils.api_get_question_info(title_slug)
            if r.status_code != 200:
                print(f"bad status code {r.status_code}: {r.text}")
                print("Restarting current iteration of loop")

                i -= 1
                continue

            print(f"response successfully received for question id {question_id}")

            cur_question_json = r.json()
            cur_question_json["total_acs"] = total_acs
            cur_question_json["total_submitted"] = total_submitted
            cur_question_json["rating"] = ratings_data[str(question_id)]["rating"] if str(question_id) in ratings_data else 0
            questions_data.append(cur_question_json)

            with open("data/questions_data.json", "w+") as f:
                json.dump(questions_data, f, indent=4, separators=(',', ': '))

            time.sleep(60 * 1) # 1 min between each call