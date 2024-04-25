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


if __name__ == "__main__":
    #### Set PAT Console, input and output path
    currentDir = os.getcwd()
    PATConsoleFilePath = "C:\\Program Files (x86)\\PAT343\\PAT3.Console.exe" # PAT3.Console.exe doesn't work in PAT 3.5.1. Use 3.4.3 or lower.
    pcspFilePath = currentDir + "\\game.pcsp"
    outputPath = currentDir + "\\output\\game_prob"

    # Create output directory if not exists
    if not os.path.exists(os.path.dirname(outputPath)):
        try:
            os.makedirs(os.path.dirname(outputPath))
        except OSError as exc:
            pass
    
    #### Find the game PCSP files
    for root, dirs, files in os.walk(currentDir+"\\pcsp_files"):
        for file in files:
            if re.match(r"game_[0-9]+_[a-zA-Z]+\.pcsp", file):
                pcspFilePath = os.path.join(root, file)
                # Extract the game ID and team type from file name
                game_id, team_type, _ = os.path.basename(pcspFilePath).split(".")[0].split("_")[1:]
                print("Predicting game ID: ", game_id, " Team type: ", team_type)
                outputPathTmp = f"{outputPath}_{game_id}_{team_type}.txt"
                executePATConsole(PATConsoleFilePath, pcspFilePath, outputPathTmp)
                print(f"done for {game_id}_{team_type}")
        
