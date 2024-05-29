import json

import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import linregress
from db.db import Database
from classes.Tags import TagsEnum

def build_regression_fit():
    db = Database()

    questions_data = list(db.return_all_questions())

    # x is acceptance rate, y is rating
    x_hard, y_hard = [], []
    x_medium, y_medium = [], []
    x_easy, y_easy = [], []
    x_total, y_total = [], []

    for question in questions_data:
        if question["rating"] != 0 and question["total_acs"] >= 10000:
        # if question["rating"] != 0:
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