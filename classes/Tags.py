import numpy as np

class TagsStatistics:
    def __init__(self, user_completed_questions, rating_question_data):
        self.user_completed_questions = user_completed_questions
        self.rating_question_data = rating_question_data

        self.tags = {}
        self.output = {}

        self.tags["array"] = ArrayTag()
        self.tags["string"] = StringTag()
        self.tags["hash-table"] = HashTableTag()
        self.tags["matrix"] = MatrixTag()
        self.tags["stack"] = StackTag()
        self.tags["queue"] = QueueTag()
        self.tags["linked-list"] = LinkedListTag()

        self.tags["two-pointers"] = TwoPointersTag()
        self.tags["binary-search"] = BinarySearchTag()
        self.tags["sliding-window"] = SlidingWindowTag()
        self.tags["tree"] = TreeTag()
        self.tags["heap-priority-queue"] = HeapTag()
        self.tags["graph"] = GraphTag()
        self.tags["math"] = MathTag()

        self.tags["backtracking"] = BacktrackingTag()
        self.tags["dynamic-programming"] = DynamicProgrammingTag()
        self.tags["bit-manipulation"] = BitManipulationTag()
        self.tags["topological-sort"] = TopologicalSortTag()

        self.tags["overall"] = OverallTag()

    def build_tag_data(self):
        for question_id in self.user_completed_questions:
            if str(question_id) not in self.rating_question_data:
                continue

            question_object = self.rating_question_data[str(question_id)]

            question_rating = question_object["rating"]
            question_tags = question_object["tags"]

            for question_tag in question_tags:
                tag_slug = question_tag["slug"]

                # some tags are not supported such as bfs/dfs
                if tag_slug not in self.tags:
                    continue

                self.tags[tag_slug].add_rating(question_rating, question_id)
                self.tags["overall"].add_rating(question_rating, question_id)

        for tag_slug in self.tags:
            tag_class = self.tags[tag_slug]

            tag_class.calculate_rating()

            self.output[tag_slug] = tag_class.tag_rating

    def to_object(self):
        return self.output

class Tag:
    def __init__(self):
        self.slug = ""
        self.questions = []
        self.ratings = []
        self.tag_rating = 0
        self.tag_difficulty = ""

    def add_rating(self, rating, question_id):
        self.questions.append(question_id)
        self.ratings.append(rating)

    def calculate_rating(self):
        # The user must have done at least 2 problems with the given tag
        # for there to be a rating calculated
        if len(self.ratings) < 3:
            self.tag_rating = 0
            return

        # self.tag_rating = quantiles(self.ratings, n=100)[74] # 75th percentile
        np_ratings = np.array(self.ratings)
        self.tag_rating = np.percentile(np_ratings, 75) # 75th percentile

class ArrayTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "array"
        self.tag_difficulty = "Easy"

class StringTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "string"
        self.tag_difficulty = "Easy"

class HashTableTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "hash-table"
        self.tag_difficulty = "Easy"

class MatrixTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "matrix"
        self.tag_difficulty = "Easy"

class StackTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "stack"
        self.tag_difficulty = "Easy"

class QueueTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "queue"
        self.tag_difficulty = "Easy"

class LinkedListTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "linked-list"
        self.tag_difficulty = "Easy"

class TwoPointersTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "two-pointers"
        self.tag_difficulty = "Medium"

class BinarySearchTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "binary-search"
        self.tag_difficulty = "Medium"

class SlidingWindowTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "sliding-window"
        self.tag_difficulty = "Medium"

class TreeTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "tree"
        self.tag_difficulty = "Medium"

class HeapTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "heap-priority-queue"
        self.tag_difficulty = "Medium"

class GraphTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "graph"
        self.tag_difficulty = "Medium"

class MathTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "math"
        self.tag_difficulty = "Medium"

class BacktrackingTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "backtracking"
        self.tag_difficulty = "Hard"

class DynamicProgrammingTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "dynamic-programming"
        self.tag_difficulty = "Hard"

class BitManipulationTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "bit-manipulation"
        self.tag_difficulty = "Hard"

class TopologicalSortTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "topological-sort"
        self.tag_difficulty = "Hard"

class OverallTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "overall"