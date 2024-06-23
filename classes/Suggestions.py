import enum

from db.db import Database

from classes.Tags import TagsEnum

class RecommendationEnum(enum.Enum):
    simple = 1
    moderate = 2
    difficult = 3

class Suggestion:
    def __init__(self):
        self.db: Database = Database()

        self.user_result = None

    def rating_filter(self, pipeline: list[dict], *,
                      min_rating: int,
                      max_rating: int):
        if min_rating is None or max_rating is None:
            min_rating, max_rating = 0, 10000

        rating_filter_pipeline = {
            "$match": {
                "zerotrac_rating": {
                    "$gte": min_rating,
                    "$lte": max_rating
                }
            }
        }

        pipeline.append(rating_filter_pipeline)

    def keyword_filter(self, pipeline: list[dict], *,
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

    def tags_filter(self, pipeline: list[dict], *,
                    tags_must_include: list[TagsEnum],
                    tags_ignore: list[TagsEnum]):
        match_criteria = {}
        
        tags_must_include = [tag for tag in tags_must_include]
        tags_ignore = [tag for tag in tags_ignore]

        if tags_must_include:
            match_criteria["tags"] = {"$all": tags_must_include}

        if tags_ignore:
            if tags_must_include:
                match_criteria["tags"]["$nin"] = tags_ignore
            else:
                match_criteria["tags"] = {"$nin": tags_ignore}

        tags_filter_pipeline = {"$match": match_criteria}

        pipeline.append(tags_filter_pipeline)

    def completed_questions_filter(self, pipeline: list[dict]):
        completed_questions = self.user_result["completed_questions"]

        if not completed_questions:
            return
        
        completed_questions_filter_pipeline = {
            "$match": {
                "question_id": {
                    "$nin": completed_questions
                }
            }
        }

        pipeline.append(completed_questions_filter_pipeline)

    def random_question_filter(self, pipeline: list[dict], *,
                               size: int = 1):
        # maybe can support giving multiple questions in the future

        random_question_pipeline = {'$sample': {'size': size}}

        pipeline.append(random_question_pipeline)

    def set_user(self, discord_user_id: int):
        self.user_result = self.db.find_user_by_discord_id(discord_user_id)
        
        return self.user_result

    def suggest_problem(self, *,
                        min_rating: int = 0,
                        max_rating: int = 10000,
                        search_term: str = "",
                        tags_must_include: list[TagsEnum] = [],
                        tags_ignore: list[TagsEnum] = []):
        pipeline = []

        self.rating_filter(pipeline,
                           min_rating=min_rating,
                           max_rating=max_rating)
        
        self.keyword_filter(pipeline,
                            search_term=search_term)
        
        self.tags_filter(pipeline,
                         tags_must_include=tags_must_include,
                         tags_ignore=tags_ignore)
        
        self.completed_questions_filter(pipeline)
        
        self.random_question_filter(pipeline)
        
        result_cursor = self.db.rating_question_tag_data_collection.aggregate(pipeline)

        try:
            question = next(result_cursor)
        except StopIteration:
            return "could not find a result for you! Maybe try including " + \
                   "more tags or expanding your search range..."
    
        response = f"Here's a problem for you: {question['link']}\n" + \
                   f"Rating: ||{int(question['zerotrac_rating'])}||. Tags: ||{', '.join(question["tags"])}||"

        return response
    
class SimpleSuggestion(Suggestion):
    def __init__(self):
        super().__init__()

    def suggest_problem(self,
                        discord_user_id: int,
                        *,
                        difficulty: RecommendationEnum):
        user_result = super().set_user(discord_user_id)

        if user_result == None:
            return "You must set up your profile first before using /recommend! See the " + \
                    "instructions in /setup"
        
        user_rating = user_result["projected_rating"]
        
        match difficulty:
            case RecommendationEnum.simple:
                min_rating, max_rating = user_rating - 300, user_rating - 100
            case RecommendationEnum.moderate:
                min_rating, max_rating = user_rating - 100, user_rating + 100
            case RecommendationEnum.difficult:
                min_rating, max_rating = user_rating + 100, user_rating + 300
            case _:
                min_rating, max_rating = user_rating - 100, user_rating + 100

        user_blacklisted_tags = user_result["settings"]["blacklisted_tags"]

        return super().suggest_problem(min_rating=min_rating,
                                       max_rating=max_rating,
                                       tags_ignore=user_blacklisted_tags)
    
class AdvancedSuggestion(Suggestion):
    def __init__(self):
        super().__init__()

    def suggest_problem(self,
                        discord_user_id: int,
                        *,
                        min_rating: int = 0,
                        max_rating: int = 10000,
                        search_term: str = "",
                        tags_must_include: list[TagsEnum] = [],
                        tags_ignore: list[TagsEnum] = []):
        user_result = super().set_user(discord_user_id)

        if user_result == None:
            return "You must set up your profile first before using /recommend! See the " + \
                    "instructions in /setup"
        
        return super().suggest_problem(min_rating=min_rating,
                                       max_rating=max_rating,
                                       search_term=search_term,
                                       tags_must_include=tags_must_include,
                                       tags_ignore=tags_ignore)

class WeakSkillsetSuggestion(Suggestion):
    def __init__(self):
        super().__init__()

    def suggest_problem(self, tag_difficulty):
        pass