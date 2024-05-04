class Suggestion:
    def __init__(self):
        pass

    def suggest_problem(self):
        # suggests a problem based on some criteria
        # to be overriden by a subclass
        pass

class WeakSkillsetSuggestion:
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