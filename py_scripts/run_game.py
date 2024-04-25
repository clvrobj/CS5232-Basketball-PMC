"""
This script runs the PAT Console for all the games in the pcsp_files directory.
Output raw PAT verification results are saved in the output directory. E.g. output/game_prob_1_home.txt
"""
import subprocess
import os
import re

def executePATConsole(PATConsoleFilePath, pcspFilePath, outputPath):
    arguments = [
        "-pcsp",
        pcspFilePath,
        outputPath
    ]
    try:
        subprocess.run([PATConsoleFilePath] + arguments)
    except FileNotFoundError:
        print(f"File '{PATConsoleFilePath}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_and_create_output_dir():
    currentDir = os.getcwd()
    outputPath = currentDir + "\\output\\game_prob"
    # Create output directory if not exists
    if not os.path.exists(os.path.dirname(outputPath)):
        try:
            os.makedirs(os.path.dirname(outputPath))
        except OSError as exc:
            pass

def run_one_game(game_id, team_type):
    check_and_create_output_dir()
    #### Set PAT Console, input and output path
    currentDir = os.getcwd()
     # Note: PAT3.Console.exe doesn't work in PAT 3.5.1. Use 3.4.3 or lower.
    PATConsoleFilePath = "C:\\Program Files (x86)\\PAT343\\PAT3.Console.exe"
    pcspFilePath = currentDir + f"\\pcsp_files\\game_{game_id}_{team_type}.pcsp"
    outputPath = currentDir + f"\\output\\game_prob_{game_id}_{team_type}.txt"
    
    print("Predicting game ID: ", game_id, " Team type: ", team_type)
    executePATConsole(PATConsoleFilePath, pcspFilePath, outputPath)
    print(f"Done for {game_id}_{team_type}")
    return

def run_all_games():
    check_and_create_output_dir()

    currentDir = os.getcwd()
    for root, dirs, files in os.walk(currentDir+"\\pcsp_files"):
        for file in files:
            if re.match(r"game_[0-9]+_[a-zA-Z]+\.pcsp", file):
                pcspFilePath = os.path.join(root, file)
                # Extract the game ID and team type from file name
                game_id, team_type = os.path.basename(pcspFilePath).split(".")[0].split("_")[1:]
                run_one_game(game_id, team_type)

    return

if __name__ == "__main__":
    run_all_games()
        
