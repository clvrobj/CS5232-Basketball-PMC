import re
import os
import math

def sigmoid(x, k=1):
    return 1 / (1 + math.exp(-k * x))

# Extract the probability of the game results from the probability file
def extractGameResultSoftmax(outputPathHome, outputPathAway):
    def extractGameResultProbabilities(outputPath):
        with open(outputPath, "r") as file:
            lines = file.readlines()
            probs = []
            for line in lines:
                # The probability of the game result
                if "The Assertion" in line:
                    # Fine all [0.12, 0.48]] in the line
                    prob = re.findall(r"\[.*\]", line)                    
                    if prob:
                        prob = prob[0].replace("[", "").replace("]", "").split(", ")
                        probs.append(float(prob[1]))
            if len(probs) > 0:
                # Return the lowest and highest probabilities from the probs list
                return min(probs), max(probs)

    # Get the probabilities of the home and away team
    probHome = extractGameResultProbabilities(outputPathHome)
    probAway = extractGameResultProbabilities(outputPathAway)
    print(f"ProbHome: {probHome}, ProbAway: {probAway}")
    if probHome and probAway:
        home_low, home_high = probHome
        away_low, away_high = probAway
        home_softmax = sigmoid(home_low - home_high)
        away_softmax = sigmoid(away_low - away_high)
        # return the winner of the game
        if home_softmax > away_softmax:
            return "home", probHome, probAway
        else:
            return "away", probHome, probAway
    return None
def writeLineToFile(filePath, line, mode):
    try:
        with open(filePath, mode) as file:
            file.write(line+'\n')
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    # Find all the game probability files in the output directory
    currentDir = os.getcwd()
    outputPath = currentDir + "/output"
    outputCSVPath = os.path.join(currentDir, "output", "game_winner_summary.csv")
    writeLineToFile(outputCSVPath, "game_id,team_type,prob_home_low,prob_home_high,prob_away_low,prob_away_high,winner", 'w')
    for root, dirs, files in os.walk(outputPath):
        for file in files:
            print(f"Processing file: {file}")
            if re.match(r"game_prob_[0-9]+_[a-zA-Z]+\.txt", file):
                print(f"Processing file: {file}")
                # Find the home and away team probability files
                game_id, team_type = os.path.basename(file).split(".")[0].split("_")[2:]
                outputPathHome = os.path.join(root, f"game_prob_{game_id}_home.txt")
                outputPathAway = os.path.join(root, f"game_prob_{game_id}_away.txt")
                # Predict the game result
                winner, probHome, probAway = extractGameResultSoftmax(outputPathHome, outputPathAway)
                if winner:
                    print(f"Game ID: {game_id}, Team type: {team_type}, Winner: {winner}")
                    writeLineToFile(outputCSVPath, f"{game_id},{team_type},{probHome[0]},{probHome[1]},{probAway[0]},{probAway[1]},{winner}", 'a')
                else:
                    print(f"Game ID: {game_id}, Team type: {team_type}, No winner")
                    writeLineToFile(outputCSVPath, f"{game_id},{team_type},{probHome[0]},{probHome[1]},{probAway[0]},{probAway[1]},", 'a')