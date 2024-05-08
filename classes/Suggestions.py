import enum
import json
import random

class RecommendationEnum(enum.Enum):
    simple = 1
    moderate = 2
    difficult = 3

class Suggestion:
    def __init__(self):
        pass

        # with open("data/rating_question_tag.json", "r+") as f:
        #     self.questions_data = json.load(f)

        # # print(self.questions_data)

        # self.question_ids = [(self.questions_data[x]["rating"],
        #                       int(x),
        #                       self.questions_data[x]["link"])
        #                       for x in self.questions_data.keys()]
        
        # self.question_ids.sort(key=lambda x: x[0])

    def suggest_problem(self, rating_range, filter_func):
        range_min, range_max = rating_range

        # binary search
        left = 0
        right = len(self.question_ids) + 1

        def find_leftmost(k):
            return self.question_ids[k][0] >= range_min

        # find leftmost index that is in given range
        while left < right:
            mid = left + (right - left) // 2

            if find_leftmost(mid):
                right = mid
            else:
                left = mid + 1

        leftmost_index = left

        left = leftmost_index
        right = len(self.question_ids) + 1

        def find_rightmost(k):
            return self.question_ids[k][0] >= range_max
        
        # find leftmost index that is bigger than range_max
        while left < right:
            mid = left + (right - left) // 2

            if find_rightmost(mid):
                right = mid
            else:
                left = mid + 1

        rightmost_index = left - 1

        random_question_index = random.randint(leftmost_index, rightmost_index)

        return self.question_ids[random_question_index][2]


    def rating_range_filter(self, range):
        # suggests a problem based on some criteria
        # to be overriden by a subclass
        pass


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