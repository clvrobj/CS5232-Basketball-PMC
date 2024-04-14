import subprocess
import os

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
    pcspFilePath = currentDir+"\\game.pcsp"
    outputPath = currentDir+"\\result"

    #### Run Game
    for i in range(3):
        outputPathTmp = f"{outputPath}{i}"
        executePATConsole(PATConsoleFilePath, pcspFilePath, outputPathTmp)
        print(f"done {i}")
        
