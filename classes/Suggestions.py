import enum
import json
import random

from db.db import Database

from classes.Tags import TagsEnum

class RecommendationEnum(enum.Enum):
    simple = 1
    moderate = 2
    difficult = 3

class Suggestion:
    def __init__(self):
        self.db: Database = Database()

    @classmethod
    def rating_filter(cls, pipeline: list[dict], *,
                      min_rating: int,
                      max_rating: int,
                      difficulty: RecommendationEnum,
                      user_rating: float):
        if min_rating is None or max_rating is None:
            match difficulty:
                case RecommendationEnum.simple:
                    min_rating, max_rating = user_rating - 300, user_rating - 100
                case RecommendationEnum.moderate:
                    min_rating, max_rating = user_rating - 100, user_rating + 100
                case RecommendationEnum.difficult:
                    min_rating, max_rating = user_rating + 100, user_rating + 300

        rating_filter_pipeline = {
            "$match": {
                "rating": {
                    "$gte": min_rating,
                    "$lte": max_rating
                }
            }
        }

        pipeline.append(rating_filter_pipeline)

    @classmethod
    def keyword_filter(cls, pipeline: list[dict], *,
                       search_term: str):
        if not search_term:
            return

        keyword_filter_pipeline = {
            "$match": {
                "$or": [
                    {
                        "tags": {
                            "$elemMatch": {
                                "$regex": search_term.replace(" ", "-"),
                                "$options": "i"
                            }
                        }
                    },
                    {
                        "title": {
                            "$regex": search_term,
                            "$options": "i"
                        }
                    }
                ]
            }
        }

        pipeline.append(keyword_filter_pipeline)

    @classmethod
    def tags_filter(cls, pipeline: list[dict], *,
                    tags_must_include: list[TagsEnum],
                    tags_ignore: list[TagsEnum]):
        match_criteria = {}

        if tags_must_include:
            match_criteria["tags"] = {"$all": tags_must_include}

        if tags_ignore:
            if tags_must_include:
                match_criteria["tags"]["$nin"] = tags_ignore
            else:
                match_criteria["tags"] = {"$nin": tags_ignore}

        tags_filter_pipeline = {"$match": match_criteria}

        pipeline.append(tags_filter_pipeline)

    def suggest_problem(self,
                        discord_user_id: int,
                        *,
                        min_rating: int = 0,
                        max_rating: int = 10000,
                        search_term: str = "",
                        tags_must_include: list[TagsEnum] = [],
                        tags_ignore: list[TagsEnum] = [],
                        difficulty: RecommendationEnum = RecommendationEnum.moderate):
        user_result = self.db.find_user(discord_user_id)
        
        if user_result == None:
            # TODO: write some code to check whether user has been registered
            return

        user_rating = user_result["projected_rating"]
        user_completed_questions = set(user_result["completed_questions"])
        user_blacklisted_tags = user_result["settings"]["blacklisted_tags"]

        pipeline = []

        self.rating_filter(pipeline,
                           min_rating=min_rating,
                           max_rating=max_rating,
                           difficulty=difficulty,
                           user_rating=user_rating)
        
        self.keyword_filter(pipeline,
                            search_term=search_term)
        
        self.tags_filter(pipeline,
                         tags_must_include=tags_must_include,
                         tags_ignore=tags_ignore)
        
        result = self.db.rating_question_tag_data_collection.aggregate(pipeline)

        print(result)

        for document in result:
            print(document)

        return "test"

        # result = set(self.db.find_problems(rating_min, rating_max, user_blacklisted_tags))

        # we need to filter out questions that the user has already completed
        result = list(result.difference(result & user_completed_questions))

        if not result:
            response = "could not find a result for you! Maybe try including " + \
                       "more tags or expanding your search range..."
            
            return response

        random_question_id = random.choice(result)

        question = self.db.find_question(random_question_id)

        response = f"Here's a problem for you: {question['link']}\n" + \
                   f"Rating: ||{int(question['rating'])}||"

        return response

class WeakSkillsetSuggestion(Suggestion):
    def __init__(self):
        super().__init__()

    def suggest_problem(self, tag_difficulty):
        pass