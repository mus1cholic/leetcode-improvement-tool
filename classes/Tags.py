import numpy as np

from enum import Enum
from pymongo.collection import Collection

class TagsEnum(Enum):
    Array = ("array", "Array")
    String = ("string", "String")
    HashTable = ("hash-table", "Hash Table")
    Matrix = ("matrix", "Matrix")
    Stack = ("stack", "Stack")
    LinkedList = ("linked-list", "Linked List")

    TwoPointers = ("two-pointers", "Two Pointers")
    BinarySearch = ("binary-search", "Binary Search")
    SlidingWindow = ("sliding-window", "Sliding Window")
    Tree = ("tree", "Tree")
    HeapPriorityQueue = ("heap-priority-queue", "Heap (Priority Queue)")
    Graph = ("graph", "Graph")
    Math = ("math", "Math")

    Greedy = ("greedy", "Greedy")
    Backtracking = ("backtracking", "Backtracking")
    DynamicProgramming = ("dynamic-programming", "Dynamic Programming")
    BitManipulation = ("bit-manipulation", "Bit Manipulation")
    TopologicalSort = ("topological-sort", "Topological Sort")

    slug: str
    full_name: str

    def __new__(cls, slug, full_name):
        obj = object.__new__(cls)
        obj._value_ = slug
        obj.slug = slug
        obj.full_name = full_name

        return obj
    
    @classmethod
    def _initialize_slug_map(cls):
        cls._slug_map = {member.slug: member for member in cls}

    @classmethod
    def from_slug(cls, slug):
        if not hasattr(cls, '_slug_map'):
            cls._initialize_slug_map()
        try:
            return cls._slug_map[slug]
        except KeyError:
            raise ValueError(f"No matching TagsEnum member for slug: {slug}")

class TagsStatistics:
    def __init__(self, user_completed_questions: list,
                 rating_question_tag_data_collection: Collection):
        self.user_completed_questions = user_completed_questions
        self.rating_question_tag_data_collection = rating_question_tag_data_collection

        self.tags: dict[TagsEnum, Tag] = {}
        self.output: list[dict[str: any]] = []

        self.tags[TagsEnum.Array.slug] = ArrayTag()
        self.tags[TagsEnum.String.slug] = StringTag()
        self.tags[TagsEnum.HashTable.slug] = HashTableTag()
        self.tags[TagsEnum.Matrix.slug] = MatrixTag()
        self.tags[TagsEnum.Stack.slug] = StackTag()
        self.tags[TagsEnum.LinkedList.slug] = LinkedListTag()

        self.tags[TagsEnum.TwoPointers.slug] = TwoPointersTag()
        self.tags[TagsEnum.BinarySearch.slug] = BinarySearchTag()
        self.tags[TagsEnum.SlidingWindow.slug] = SlidingWindowTag()
        self.tags[TagsEnum.Tree.slug] = TreeTag()
        self.tags[TagsEnum.HeapPriorityQueue.slug] = HeapTag()
        self.tags[TagsEnum.Graph.slug] = GraphTag()
        self.tags[TagsEnum.Math.slug] = MathTag()

        self.tags[TagsEnum.Greedy.slug] = GreedyTag()
        self.tags[TagsEnum.Backtracking.slug] = BacktrackingTag()
        self.tags[TagsEnum.DynamicProgramming.slug] = DynamicProgrammingTag()
        self.tags[TagsEnum.BitManipulation.slug] = BitManipulationTag()
        self.tags[TagsEnum.TopologicalSort.slug] = TopologicalSortTag()

        self.overall = Overall()

    def build_tag_data(self):
        results = list(self.rating_question_tag_data_collection.find(
            {"question_id": {"$in": self.user_completed_questions}}))

        for result in results:
            question_id = result["question_id"]
            question_rating = result["zerotrac_rating"]
            question_tags = result["tags"]

            for tag_slug in question_tags:
                # some tags are not supported such as bfs/dfs
                if tag_slug not in self.tags:
                    continue

                self.tags[tag_slug].add_rating(question_rating, question_id)

            self.overall.add_rating(question_rating, question_id)

        for tag in self.tags:
            tag_class = self.tags[tag]

            tag_class.calculate_rating()

            self.output.append({
                "slug": tag_class.slug,
                "difficulty": tag_class.tag_difficulty,
                "rating": tag_class.tag_rating,
                "questions": tag_class.questions
            })

        self.overall.calculate_rating()

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

class GreedyTag(Tag):
    def __init__(self):
        super().__init__()

        self.slug = "greedy"
        self.tag_difficulty = "Hard"

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

class Overall(Tag):
    def __init__(self):
        super().__init__()