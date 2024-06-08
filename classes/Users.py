import json

from utils.constants import CONTEST_RATING_DEFAULT
import utils.utils as utils

from classes.Tags import Tag, TagsStatistics, TagsEnum

from pymongo.collection import Collection

class User():
    def __init__(self, user_discord_id: int, user_discord_username: str,
                 user_data_txt: str,
                 rating_question_tag_data_collection: Collection):
        self.discord_id: int = user_discord_id
        self.discord_username: str = user_discord_username
        self.lc_username: str
        self.lc_avatar: str
        self.contest_rating: float
        self.questions_rating: float
        self.projected_rating: float
        self.completed_questions: list[int]
        self.user_tags_stats: TagsStatistics

        self.data_txt: str = user_data_txt
        self.rating_question_tag_data_collection: Collection = rating_question_tag_data_collection

    def build_user(self):
        self.parse_txt()

        self.get_leetcode_data()
        self.build_tags()

        self.build_ratings()

        self.build_settings()

    def parse_txt(self):
        user_data = json.loads(self.data_txt)

        self.lc_username = user_data["user_name"]

        if self.lc_username == "":
            # TODO: put some error message here back
            pass

        user_questions_stats = user_data["stat_status_pairs"]

        self.completed_questions = sorted([question['stat']['frontend_question_id']
                                           for question in user_questions_stats
                                           if question['status'] == 'ac'])
        
    def get_leetcode_data(self):
        # get profile avatar
        user_data_request = utils.api_get_user_info(self.lc_username)
        user_data = user_data_request.json()

        self.avatar = user_data["avatar"]

        # get rating
        user_contest_data_request = utils.api_get_user_contest_info(self.lc_username)
        user_contest_data = user_contest_data_request.json()

        self.contest_rating = user_contest_data.get("contestRating", CONTEST_RATING_DEFAULT)

    def build_tags(self):
        self.user_tags_stats = TagsStatistics(self.completed_questions, self.rating_question_tag_data_collection)
        self.user_tags_stats.build_tag_data()

    def build_ratings(self):        
        self.questions_rating = self.user_tags_stats.tags[TagsEnum.Overall].tag_rating
        
        # if contest_rating is 0, projected rating is questions_rating - 75
        # if contest_rating < questions_rating, projected rating = 0.75*questions_rating + 0.25*contest_rating
        # if contest_rating >= questions_rating, projected rating = 0.75*contest_rating + 0.25*questions_rating

        if self.contest_rating == 0.0:
            if self.questions_rating == 0.0:
                # if you have no questions done, your default projected rating is 1350
                self.projected_rating = 1350 
            else:
                self.projected_rating = self.questions_rating - 100
        elif self.contest_rating < self.questions_rating:
            self.projected_rating = 0.75 * self.questions_rating + 0.25 * self.contest_rating
        elif self.contest_rating >= self.questions_rating:
            self.projected_rating = 0.75 * self.contest_rating + 0.25 * self.questions_rating

    def build_settings(self):
        settings = {
            "blacklisted_tags": [],
            "show_premium": True, # Not Yet Implemented
            "show_questions_done_before": False, # Not Yet Implemented
            # "full_ratings": True, # Not Yet Implemented
        }

        self.settings = settings

    def output_user_data_structure(self):
        user_data_structure = {
            "discord_id": self.discord_id,
            "discord_username": self.discord_username,
            "lc_user_name": self.lc_username,
            "avatar": self.avatar,
            "contest_rating": self.contest_rating,
            "questions_rating": self.questions_rating,
            "projected_rating": self.projected_rating,
            "completed_questions": self.completed_questions,
            "tags": self.user_tags_stats.output,
            "settings": self.settings
        }

        return user_data_structure
    
    @staticmethod
    def read_from_database(user_discord_id: int):
        pass