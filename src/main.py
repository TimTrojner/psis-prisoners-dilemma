import numpy as np
from players.random_player import Random
from playground import PlayGround

def main():
    print("Welcome to the Prisoner's Dilemma!")
    results = []
    player1 = Random()
    player2 = Random()
    game = PlayGround(player1, player2, "Random1", "Random2", num_games=100)
    game.run()
    results.append((game.score_player1, game.score_player2))
    print(f"Player 1 ({game.player1_name}) score: {game.score_player1}")
    print(f"Player 2 ({game.player2_name}) score: {game.score_player2}")

    if game.score_player1 < game.score_player2:
        print(f"{game.player1_name} wins!")
    elif game.score_player2 < game.score_player1:
        print(f"{game.player2_name} wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()