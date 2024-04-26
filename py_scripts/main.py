"""
Main module for the project.
"""
from get_game_stats import get_game_data
from run_game import run_all_games
from gen_pred_game_results import generate_game_results
from evaluate_with_actual_winner import evaluate_correctness

def main():
    # Get game stats from the web
    get_game_data()
    
    # Run all games
    run_all_games()

    # Generate game results
    generate_game_results()
    
    # Evaluate correctness
    evaluate_correctness()


if __name__ == "__main__":
    main()