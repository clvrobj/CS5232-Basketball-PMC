"""
Evaluate the correctness of predictions of our model by comparing them with the actual game results.
"""
import os
import math
import csv
from tabulate import tabulate

def evaluate_correctness():
    real_results_path = "data/game_origin_results.csv"
    real_results = {}
    with open(real_results_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            game_id, _, _, _, _, actual_home_points, actual_away_points = row
            actual_winner = "home" if int(actual_home_points) > int(actual_away_points) else "away"
            real_results[game_id] = actual_winner, actual_home_points, actual_away_points

    our_results_path = "output/game_winner_summary.csv"
    our_results = {}
    with open(our_results_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            (game_id, our_winner, prob_home_low, prob_home_high, prob_away_low,
             prob_away_high, home_expected_score, away_expected_score) = row
            our_winner = "home" if home_expected_score > away_expected_score else "away"
            our_results[game_id] = (our_winner, prob_home_low, prob_home_high, prob_away_low,
                                     prob_away_high, home_expected_score, away_expected_score)

    # Join the two results by game_id and print output
    joined_results = []
    cols = ["game_id", "actual_winner",
            "actual_home_points", "actual_away_points",
            "our_winner",
            "prob_home_low", "prob_home_high",
            "prob_away_low", "prob_away_high",
            "home_expected_score", "away_expected_score"]
    for game_id in our_results:
        joined_results.append([game_id, *real_results[game_id], *our_results[game_id]])
    print(tabulate(joined_results, headers=cols))

    # Calculate the accuracy of our predictions
    correct_predictions = 0
    for game_id in our_results:
        if real_results[game_id][0] == our_results[game_id][0]:
            correct_predictions += 1
    accuracy = correct_predictions / len(our_results)
    print(f"Accuracy: {accuracy}")
    return

if __name__ == "__main__":
    evaluate_correctness()