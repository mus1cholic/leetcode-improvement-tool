import requests
import json
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

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

"""
Features:

Rating by the following categories:

Fundamental:
Arrays
Strings
Hash Tables
Matrix
Stack
Queue
Linked List

Intermediate:
Two pointers
Binary Search
Sliding window
Trees
Heaps
Graphs
Greedy
Intervals
Math

Advanced:
Backtracking
Dynamic Programming
Bit Manipulation
Topological Sort


your_overall_rating = finding the rating of ratings[(3 * len(problems)) // 4]

- Throws a "random" suggested problem through your_overall_rating + x

- Suggests a "weak" random problem by going through your weakest categories and finding a problem there
"""

def main():
    pass

def parse_question_ratings():
    """
    {
        "question_id": {
            "question_id": int,
            "title": str,
            "title_slug": str,
            "rating": float
        }
    }
    """

    start_time = time.perf_counter()

    ratings_data = {}

    with open("data/ratings.txt", encoding="utf8") as f:
        next(f) # skip header line

        for line in f:
            rating, question_id, title, _, title_slug, _, _ = line.split("\t")

            ratings_structure = {
                "question_id": int(question_id),
                "title": title,
                "title_slug": title_slug,
                "rating": float(rating)
            }

            ratings_data[question_id] = ratings_structure

    ratings_data = dict(sorted(ratings_data.items()))

    with open("data/ratings.json", "w+") as f:
        json.dump(ratings_data, f, indent=4, separators=(',', ': '))

    end_time = time.perf_counter()

    print(f"Successfully parsed questions ratings from ratings.txt, took {end_time - start_time}s")

def parse_singular_question(title_slug="hopper-company-queries-i"):
    # util function for just calling the api once on a single question, for maybe
    # when the api throws an error and gives bad response
    api_base_link = "http://localhost:3000"

    r = requests.get(f"{api_base_link}/select?titleSlug={title_slug}")

    data = r.json()

    with open("data/temp.json", "w+") as f:
        json.dump(data, f, indent=4, separators=(',', ': '))

def parse_question_bank():
    with open("data/user.txt", "r+") as f:
        user_data = json.load(f)

    with open("data/ratings.json", "r+") as f:
        ratings_data = json.load(f)

    api_base_link = "http://localhost:3000"

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

        r = requests.get(f"{api_base_link}/select?titleSlug={title_slug}")
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

def build_question_rating_data():
    # now that we have question bank, we can simplify all of the questions
    # to build association between rating, question, and tags

    start_time = time.perf_counter()

    with open("data/ratings.json", "r+") as f:
        ratings_data = json.load(f)

    with open("data/questions_data.json", "r+") as f:
        questions_data = json.load(f)

    questions_data = list(questions_data)
    write_data = {}

    for question in questions_data:
        question_id = question["questionFrontendId"] # JSON only use strings as keys
        title = question["questionTitle"]
        title_slug = question["titleSlug"]
        link = question["link"]
        difficulty = question["difficulty"]
        premium = question["isPaidOnly"]
        tags = question["topicTags"] # TODO, make this a Tags object

        # TODO: There are questions in questions_data.json that aren't
        # in ratings.txt. For now, we skip those because we haven't
        # developed a way to accurately calculate rating for those.
        # Eventually we will do this through best-fit line of accepted
        # submission percentage
        if str(question_id) not in ratings_data:
            continue

        rating = ratings_data[str(question_id)]["rating"]

        question_object_structure = {
            "question_id": question_id,
            "title": title,
            "title_slug": title_slug,
            "link": link,
            "rating": rating,
            "difficulty": difficulty,
            "premium": premium,
            "tags": tags,
        }

        write_data[question_id] = question_object_structure

    with open("data/rating_question_tag.json", "w+") as f:
        json.dump(write_data, f, indent=4, separators=(',', ': '))

    end_time = time.perf_counter()

    print(f"Successfully built questions_rating database, took {end_time - start_time}s")

def build_user_data():
    # using user.txt, builds user database
    # json file strcture:
    """
    {
        "user_name": {
            "user_name": str,
            "contest_rating": float,
            "completed_questions": [question_id],
            "tags": {
                "tag_slug": {
                    "tag_slug": str,
                    "tag_rating": float
                }
            }
        }
    }
    """
    
    start_time = time.perf_counter()

    with open("data/rating_question_tag.json", "r+") as f:
        rating_question_data = json.load(f)

    with open("data/user.txt", "r+") as f:
        user_data = json.load(f)

    with open("data/user_data.json", "r+") as f:
        write_data = json.load(f)

    user_name = user_data["user_name"]

    api_base_link = "http://localhost:3000"

    r = requests.get(f"{api_base_link}/{user_name}/contest")
    user_contest_data = r.json()

    contest_rating = user_contest_data["contestRating"] if "contestRating" in user_contest_data else 0
    all_questions = user_data["stat_status_pairs"]

    completed_questions = []

    for question in all_questions:
        question_id = question["stat"]["frontend_question_id"]
        completed_status = question["status"]
        total_acs = question["stat"]["total_acs"]
        total_submitted = question["stat"]["total_submitted"]

        if completed_status != "ac":
            continue

        completed_questions.append(question_id)

    completed_questions.sort()

    # Calculate individual tag rating

    user_tags_stats = TagsStatistics(completed_questions, rating_question_data)
    user_tags_stats.build_tag_data()
    user_tags = user_tags_stats.to_object()

    print(user_tags_stats.tags["binary-search"].questions)

    user_data_structure = {
        "user_name": user_name,
        "contest_rating": contest_rating,
        "completed_questions": completed_questions,
        "tags": user_tags
    }

    write_data[user_name] = user_data_structure

    with open("data/user_data.json", "w+") as f:
        json.dump(write_data, f, indent=4, separators=(',', ': '))

    end_time = time.perf_counter()

    print(f"Successfully built user database, took {end_time - start_time}s")

def build_regression_fit():
    with open("data/questions_data.json", "r+") as f:
        questions_data = json.load(f)

    # x is acceptance rate, y is rating
    x_hard, y_hard = [], []
    x_medium, y_medium = [], []
    x_easy, y_easy = [], []
    x_total, y_total = [], []

    for question in questions_data:
        if question["rating"] != 0:
            if question["difficulty"] == "Easy":
                x_easy.append(100 * question["total_acs"] / question["total_submitted"])
                y_easy.append(question["rating"])
            elif question["difficulty"] == "Medium":
                x_medium.append(100 * question["total_acs"] / question["total_submitted"])
                y_medium.append(question["rating"])
            else:
                x_hard.append(100 * question["total_acs"] / question["total_submitted"])
                y_hard.append(question["rating"])

            x_total.append(100 * question["total_acs"] / question["total_submitted"])
            y_total.append(question["rating"])

    _, axes = plt.subplots(2, 2, figsize=(9, 9))
    xseq = np.linspace(0, 100, num=100)

    # Easy plot
    axes[0][0].scatter(x_easy, y_easy, s=30, alpha=0.7, c="green", edgecolors="k")

    slope_easy, intercept_easy, r_value_easy, _, _ = linregress(x_easy, y_easy)
    axes[0][0].plot(xseq, slope_easy * xseq + intercept_easy, color="k", lw=1.5)
    axes[0][0].text(70, 1550, f"R^2: {round(r_value_easy ** 2, 3)}")

    # Medium plot
    axes[0][1].scatter(x_medium, y_medium, s=30, alpha=0.7, c="yellow", edgecolors="k")

    slope_medium, intercept_medium, r_value_medium, _, _ = linregress(x_medium, y_medium)
    axes[0][1].plot(xseq, slope_medium * xseq + intercept_medium, color="k", lw=1.5)
    axes[0][1].text(70, 2300, f"R^2: {round(r_value_medium ** 2, 3)}")

    # Hard plot
    axes[1][0].scatter(x_hard, y_hard, s=30, alpha=0.7, c="red", edgecolors="k")

    slope_hard, intercept_hard, r_value_hard, _, _ = linregress(x_hard, y_hard)
    axes[1][0].plot(xseq, slope_hard * xseq + intercept_hard, color="k", lw=1.5)
    axes[1][0].text(70, 3000, f"R^2: {round(r_value_hard ** 2, 3)}")

    # Total plot
    axes[1][1].scatter(x_easy, y_easy, s=30, alpha=0.7, c="green", edgecolors="k")
    axes[1][1].scatter(x_medium, y_medium, s=30, alpha=0.7, c="yellow", edgecolors="k")
    axes[1][1].scatter(x_hard, y_hard, s=30, alpha=0.7, c="red", edgecolors="k")

    slope_total, intercept_total, r_value_total, _, _ = linregress(x_total, y_total)
    axes[1][1].plot(xseq, slope_total * xseq + intercept_total, color="k", lw=1.5)
    axes[1][1].text(70, 3000, f"R^2: {round(r_value_total ** 2, 3)}")
    # R^2 was 0.502

    # axes.set_xlabel("Acceptance Rate (%)")
    # axes.set_ylabel("Rating")

    plt.show()

# main()
# parse_question_ratings()
# parse_question_bank()
# build_question_rating_data()
build_user_data()
# build_regression_fit()

# parse_singular_question()





class Suggestion:
    def __init__(self):
        pass

    def suggest_problem(self):
        # suggests a problem based on some criteria
        # to be overriden by a subclass
        pass

class WeakSkillsetSuggestion:
    def __init__(self):
        pass

    def suggest_problem(self, tag_difficulty):
        pass

class RandomSuggestion:
    def __init__(self):
        pass

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