import re
import os
import math
import csv

DISCOUNT_FACTOR = 0.8

def sigmoid(x, k=1):
    return 1 / (1 + math.exp(-k * x))

# Extract the probability of the game results from the probability file
def extractGameResultSoftmax(outputPathHome, outputPathAway):
    def extractGameResultProbabilities(outputPath):
        with open(outputPath, "r") as file:
            lines = file.readlines()
            probs = []
            expected_score = 0
            for line in lines:
                # The probability of the game result
                if "The Assertion" in line:
                    # Fine all [0.12, 0.48]] in the line
                    prob = re.findall(r"\[.*\]", line)                    
                    if prob:
                        prob = prob[0].replace("[", "").replace("]", "").split(", ")
                        probs.append(float(prob[1]))
                        if "Score2Pass" in line:
                            tempScore = float(prob[1]) * 2
                            passNum = float(line[line.find("Score2Pass") + len("Score2Pass")])
                            tempScore = tempScore * pow(DISCOUNT_FACTOR, passNum) / 5
                            expected_score = expected_score + tempScore
                        elif "Score3Pass" in line:
                            tempScore = float(prob[1]) * 3
                            passNum = float(line[line.find("Score3Pass") + len("Score3Pass")])
                            tempScore = tempScore * pow(DISCOUNT_FACTOR, passNum) / 5
                            expected_score = expected_score + tempScore
            if len(probs) > 0:
                # Return the lowest and highest probabilities from the probs list
                return min(probs), max(probs), expected_score

    # Get the probabilities of the home and away team
    probHome = extractGameResultProbabilities(outputPathHome)
    probAway = extractGameResultProbabilities(outputPathAway)
    print(f"ProbHome: {probHome}, ProbAway: {probAway}")
    winner = None
    if probHome and probAway:
        home_low, home_high, home_expected_score = probHome
        away_low, away_high, away_expected_score = probAway
        home_softmax = sigmoid(home_low - home_high)
        away_softmax = sigmoid(away_low - away_high)
        # return the winner of the game
        if home_softmax > away_softmax:
            winner = "home" 
        else:
            winner =  "away"
    return winner, probHome, probAway, home_expected_score, away_expected_score


def generate_game_results():
    # Find all the game probability files in the output directory
    currentDir = os.getcwd()
    outputPath = currentDir + "/output"
    outputCSVPath = os.path.join(outputPath, "game_winner_summary.csv")
    with open(outputCSVPath, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["game_id",
                          "winner", 
                          "prob_home_low", 
                          "prob_home_high", 
                          "prob_away_low", 
                          "prob_away_high", 
                          "home_expected_score", 
                          "away_expected_score"])
    
        # Find all the game_id in the output directory
        game_ids = set()
        for root, dirs, files in os.walk(outputPath):
            for file in files:
                if re.match(r"game_prob_[0-9]+_[a-zA-Z]+\.txt", file):
                    game_id = os.path.basename(file).split(".")[0].split("_")[2]
                    game_ids.add(game_id)

        for game_id in game_ids:
            # Find the home and away team probability files
            outputPathHome = os.path.join(root, f"game_prob_{game_id}_home.txt")
            outputPathAway = os.path.join(root, f"game_prob_{game_id}_away.txt")
            # Predict the game result
            winner, probHome, probAway, home_expected_score, away_expected_score = \
                extractGameResultSoftmax(outputPathHome, outputPathAway)
            print(f"Game ID: {game_id}, Winner: {winner}")
            writer.writerow([game_id,
                            winner,
                            probHome[0],
                            probHome[1],
                            probAway[0],
                            probAway[1],
                            home_expected_score,
                            away_expected_score])


if __name__ == "__main__":
   generate_game_results()