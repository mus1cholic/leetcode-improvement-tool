import enum
import json
import random

from db.db import Database

class RecommendationEnum(enum.Enum):
    simple = 1
    moderate = 2
    difficult = 3

class Suggestion:
    def __init__(self):
        self.db: Database = Database()

    def suggest_problem(self,
                        discord_user_id: int,
                        difficulty: RecommendationEnum = RecommendationEnum.moderate):
        # TODO: customizable options

        user_result = self.db.find_user(discord_user_id)
        
        if user_result == None:
            # TODO: write some code to check whether user has been registered
            return

        user_rating = user_result["projected_rating"]
        user_completed_questions = set(user_result["completed_questions"])
        user_blacklisted_tags = user_result["settings"]["blacklisted_tags"]
        
        match difficulty:
            case RecommendationEnum.simple:
                rating_min = user_rating - 300
                rating_max = user_rating - 100
            case RecommendationEnum.moderate:
                rating_min = user_rating - 100
                rating_max = user_rating + 100
            case RecommendationEnum.difficult:
                rating_min = user_rating + 100
                rating_max = user_rating + 300
            case _:
                pass

        result = set(self.db.find_problems(rating_min, rating_max, user_blacklisted_tags))

        # we need to filter out questions that the user has already completed
        result = list(result.difference(result & user_completed_questions))

        if not result:
            response = "could not find a result for you! Maybe try including " + \
                       "more tags or expanding your search range..."
            
            return response

        random_question_id = random.choice(result)

        question = self.db.find_question(random_question_id)

        response = f"here's a problem for you: {question['link']}\n" + \
                   f"Rating: ||{int(question['rating'])}||"

        return response

class WeakSkillsetSuggestion(Suggestion):
    def __init__(self):
        super().__init__()

    def suggest_problem(self, tag_difficulty):
        pass

class RandomSuggestion:
    def __init__(self):
        super().__init__()

    def suggest_problem(self, difficulty):
        # do we calculate rating range here or somewhere else?
        # rating range based on difficulty
        # rating_range = (x, y)

        # potential_questions = []

        # put this as a class variable when you first build the suggestion class
        # for question in self.user_not_done:
            # if question's rating is within rating_range:
                # append to potential_questions

        # choose random from potential question, return
        pass

class User:
    def __init__(self):
        pass

class Question:
    def __init__(self, id, title, title_slug):
        self.id = id
        self.tags = False
        self.rating = False