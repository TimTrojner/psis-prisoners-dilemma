from players.random_player import Random
from players.t4t import TIT_FOR_TAT
from players.all_d import ALL_D
from players.joss import JOSS
from players.tester import Tester
from playground import PlayGround
import pandas as pd
import numpy as np

def run_tournament(show_individual_games=False):
    print("Welcome to the Prisoner's Dilemma Tournament!")
    
    # Define all strategies
    strategies = [
        (Random(), "Random"),
        (TIT_FOR_TAT(), "TitForTat"),
        (ALL_D(), "AlwaysDefect"),
        (JOSS(), "JOSS"),
        (Tester(), "Tester")
    ]
    
    # Create results matrix
    num_strategies = len(strategies)
    results = np.zeros((num_strategies, num_strategies))
    
    # Run tournament
    for i, (player1, name1) in enumerate(strategies):
        for j, (player2, name2) in enumerate(strategies):
            if i != j:  # Don't play against self (or optionally do with i <= j)
                # Reset players before each match
                player1.reset()
                player2.reset()
                
                # Run the match
                game = PlayGround(player1, player2, name1, name2, num_games=100)
                game.run(show_choices_and_results=show_individual_games)
                
                # Store results (lower score is better)
                results[i, j] = game.score_player1
                
                print(f"{name1} vs {name2}: {game.score_player1} - {game.score_player2}")
    
    # Create and display results table
    strategy_names = [name for _, name in strategies]
    results_df = pd.DataFrame(results, index=strategy_names, columns=strategy_names)
    
    print("\nResults Table (lower score is better):")
    print(results_df)
    
    # Calculate average performance
    average_scores = results_df.mean(axis=1).sort_values()
    print("\nRanking (Average Score):")
    for rank, (name, score) in enumerate(average_scores.items(), 1):
        print(f"{rank}. {name}: {score:.2f}")

def main():
    run_tournament(show_individual_games=False)  # Set to True to see each move

if __name__ == "__main__":
    main()