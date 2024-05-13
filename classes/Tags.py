import enum

import numpy as np

from pymongo.collection import Collection

class TagsEnum(enum.StrEnum):
    Array = "array"
    String = "string"
    HashTable = "hash-table"
    Matrix = "matrix"
    Stack = "stack"
    Queue = "queue"
    LinkedList = "linked-list"

    TwoPointers = "two-pointers"
    BinarySearch = "binary-search"
    SlidingWindow = "sliding-window"
    Tree = "tree"
    HeapPriorityQueue = "heap-priority-queue"
    Graph = "graph"
    Math = "math"

    Backtracking = "backtracking"
    DynamicProgramming = "dynamic-programming"
    BitManipulation = "bit-manipulation"
    TopologicalSort = "topological-sort"

    Overall = "overall"

class TagsStatistics:
    def __init__(self, user_completed_questions: list,
                 rating_question_tag_data_collection: Collection):
        self.user_completed_questions = user_completed_questions
        self.rating_question_tag_data_collection = rating_question_tag_data_collection

        self.tags: dict[TagsEnum, Tag] = {}
        self.output: list[dict[str: any]] = []

        self.tags[TagsEnum.Array] = ArrayTag()
        self.tags[TagsEnum.String] = StringTag()
        self.tags[TagsEnum.HashTable] = HashTableTag()
        self.tags[TagsEnum.Matrix] = MatrixTag()
        self.tags[TagsEnum.Stack] = StackTag()
        self.tags[TagsEnum.Queue] = QueueTag()
        self.tags[TagsEnum.LinkedList] = LinkedListTag()

        self.tags[TagsEnum.TwoPointers] = TwoPointersTag()
        self.tags[TagsEnum.BinarySearch] = BinarySearchTag()
        self.tags[TagsEnum.SlidingWindow] = SlidingWindowTag()
        self.tags[TagsEnum.Tree] = TreeTag()
        self.tags[TagsEnum.HeapPriorityQueue] = HeapTag()
        self.tags[TagsEnum.Graph] = GraphTag()
        self.tags[TagsEnum.Math] = MathTag()

        self.tags[TagsEnum.Backtracking] = BacktrackingTag()
        self.tags[TagsEnum.DynamicProgramming] = DynamicProgrammingTag()
        self.tags[TagsEnum.BitManipulation] = BitManipulationTag()
        self.tags[TagsEnum.TopologicalSort] = TopologicalSortTag()

        self.tags[TagsEnum.Overall] = OverallTag()

    def build_tag_data(self):
        results = list(self.rating_question_tag_data_collection.find(
            {"question_id": {"$in": self.user_completed_questions}}))

        for result in results:
            question_id = result["question_id"]
            question_rating = result["rating"]
            question_tags = result["tags"]

            for tag_slug in question_tags:
                # some tags are not supported such as bfs/dfs
                if tag_slug not in self.tags:
                    continue

                self.tags[tag_slug].add_rating(question_rating, question_id)
                self.tags[TagsEnum.Overall].add_rating(question_rating, question_id)

        for tag in self.tags:
            tag_class = self.tags[tag]

            tag_class.calculate_rating()

            self.output.append({
                "slug": tag_class.slug,
                "difficulty": tag_class.tag_difficulty,
                "rating": tag_class.tag_rating,
                "questions": tag_class.questions
            })

        # print(self.output)

class Tag:
    def __init__(self):
        self.slug = ""
        self.questions = []
        self.ratings = []
        self.tag_rating = 0.0
        self.tag_difficulty = ""

    def add_rating(self, rating, question_id):
        self.questions.append(question_id)
        self.ratings.append(rating)

    def calculate_rating(self):
        np_ratings = np.array(self.ratings)
        np_ratings = np_ratings[np_ratings != 0] # filter out 0s

        # The user must have done at least 2 problems with the given tag
        # that has rating data for there to be a rating calculated
        if len(np_ratings) < 3:
            self.tag_rating = 0.0
            return
        
        self.tag_rating = np.percentile(np_ratings, 80) # 80th percentile

class ArrayTag(Tag):
    slug = "array"

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