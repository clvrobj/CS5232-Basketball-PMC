# CS5232-Basketball-PMC

## Prerequisites
* Download and install the executable PAT from [PAT-Process Analysis Toolkit](https://pat.comp.nus.edu.sg/?page_id=2660)
* Insatll Python and run `pip install -r requirements.txt` to install the required python packages.

## Steps
* Run the `main.py` to execute the entire pipeline `python py_scripts/main.py`
* You can also run the scripts individually by executing the scripts in the `py_scripts` folder.

## Components


* The `main.py` script will execute the following scripts in the following order:
    * `get_game_stats.py`: This script will fetch the game data and generate PCSP files.
    * `run_game.py`: This script will run the PCSP module to generate the game probability result.
    * `gen_pred_game_results.py`: This script will predict the result of the games.
    * `evaluate_with_actual_winner.py`: This script will evaluate the prediction results and compare with the actual winner.
* Folders
    * All the executable scripts are located in the `py_scripts` folder
    * `data`: Contains the game data and origin game results in the CSV format.
    * `pcsp_files`: Contains the PCSP files generated from the game data.
    * `output`: Contains the prediction results and evaluation results.

