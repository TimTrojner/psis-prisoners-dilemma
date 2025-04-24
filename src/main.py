from players.random_player import Random
from players.t4t import TIT_FOR_TAT
from players.all_d import ALL_D
from players.niceguy import NICE_GUY
from players.joss import JOSS
from players.grudgeHolder import GrudgeHolder
from players.tester import Tester
from players.qlearning_player import QLearningPlayer
from playground import PlayGround
import matplotlib.pyplot as plt

def train_q_table(num_training_games=500000):
    """Nauči Q-tabelo skozi veliko število iger in jo vrne"""
    print("Treniram Q-tabelo...")
    
    # Ustvari Q-Learning igralca z nižjo stopnjo raziskovanja za treniranje
    qlearner = QLearningPlayer(
        learning_rate=0.2, 
        discount_factor=0.99, 
        exploration_rate=0.3,  # Višja vrednost za več raziskovanja med učenjem
        history_length=3
    )
    
    # Seznam strategij za trening
    training_strategies = [
        (TIT_FOR_TAT(), "TitForTat"),
        (ALL_D(), "AlwaysDefect"),
        (Random(), "Random"),
        (JOSS(), "JOSS"),
        (Tester(), "Tester"),
        (GrudgeHolder(), "GrudgeHolder")
    ]
    
    # Treniraj proti vsaki strategiji
    for strategy, name in training_strategies:
        print(f"  - Treniram proti {name}...")
        games_per_strategy = num_training_games // len(training_strategies)
        
        for _ in range(games_per_strategy):
            # Ponastavi nasprotnikovo zgodovino
            strategy.__init__()
            qlearner.past_actions = []
            qlearner.num_games = 0
            qlearner.last_state = None
            qlearner.last_action = None
            
            # Igraj eno igro s 100 potezami
            playground = PlayGround(qlearner, strategy, "QLearn", name, 100)
            playground.run(show_choices_and_results=False)
    
    print(f"Učenje končano! Q-tabela vsebuje {len(qlearner.q_table)} stanj.")
    return qlearner.q_table

pretrained_q_table = train_q_table(num_training_games=500000)

def tournament_round(strategies, num_games, show_individual_games=False):
   
    scores = {name: 0 for _, name in strategies}
    game_count = 0
    all_results = []
    
    if num_games > 1000:
        sample_freq = max(1, num_games // 1000)  
    else:
        sample_freq = 1
    
    # Track cumulative scores by game number for each strategy
    strategy_scores_by_game = {name: [] for _, name in strategies}
    
    # Each strategy plays against every other strategy
    for i, (strategy1, name1) in enumerate(strategies):
        for j, (strategy2, name2) in enumerate(strategies):
            if i >= j:  # Skip duplicate pairings and self-play
                continue
            
            game_count += 1
            if not show_individual_games:
                print(f"Game {game_count}: {name1} vs {name2} ({num_games} rounds)")
            
            # Reset strategy histories
            if name1 == "QLearn":
                strategy1.past_actions = []
                strategy1.num_games = 0
                strategy1.last_state = None
                strategy1.last_action = None
            else:
                strategy1.reset()

            if name2 == "QLearn":
                strategy2.past_actions = []
                strategy2.num_games = 0
                strategy2.last_state = None
                strategy2.last_action = None
            else:
                strategy2.reset()
            
            # Create and run the game
            playground = PlayGround(
                strategy1, 
                strategy2, 
                name1, 
                name2, 
                num_games
            )
            playground.run(show_choices_and_results=show_individual_games)
            
            # Record the results
            scores[name1] += playground.score_player1
            scores[name2] += playground.score_player2
            
            # For large game counts, sample the cumulative scores at regular intervals
            if num_games > 1000:
                sampled_p1 = [playground.cumulative_score_p1[i] for i in range(0, num_games, sample_freq)]
                sampled_p2 = [playground.cumulative_score_p2[i] for i in range(0, num_games, sample_freq)]
                game_indices = list(range(0, num_games, sample_freq))
                
                # Add the final score if it's not already included
                if (num_games - 1) % sample_freq != 0:
                    sampled_p1.append(playground.cumulative_score_p1[-1])
                    sampled_p2.append(playground.cumulative_score_p2[-1])
                    game_indices.append(num_games - 1)
            else:
                sampled_p1 = playground.cumulative_score_p1
                sampled_p2 = playground.cumulative_score_p2
                game_indices = list(range(num_games))
            
            # Store detailed results for later analysis
            all_results.append({
                'player1': name1,
                'player2': name2,
                'score1': playground.score_player1,
                'score2': playground.score_player2,
                'cumulative_score_p1': sampled_p1,
                'cumulative_score_p2': sampled_p2,
                'game_indices': game_indices
            })
            
            # Update running average scores by game
            # For large tournaments, we'll only track sampled points
            for game_idx, p1_score, p2_score in zip(
                game_indices, 
                sampled_p1, 
                sampled_p2
            ):
                # Ensure we have enough slots in our arrays
                while len(strategy_scores_by_game[name1]) <= game_idx:
                    strategy_scores_by_game[name1].append(0)
                while len(strategy_scores_by_game[name2]) <= game_idx:
                    strategy_scores_by_game[name2].append(0)
                
                # Add the scores
                strategy_scores_by_game[name1][game_idx] += p1_score
                strategy_scores_by_game[name2][game_idx] += p2_score
    
    return scores, all_results, strategy_scores_by_game

def run_tournament(show_individual_games=False):
    """
    Run multiple tournaments with different numbers of games and analyze the results
    """
    print("Welcome to the Prisoner's Dilemma Tournament!")


        # Ustvari igralca z natrenirano tabelo in nižjo stopnjo raziskovanja
    qlearner = QLearningPlayer(
        learning_rate=0.05,  # Nižja vrednost za stabilnejše učenje
        discount_factor=0.99, 
        exploration_rate=0.05,  # Nižja vrednost - manj naključnosti v turnirju
        history_length=3,
        pretrained_q_table=pretrained_q_table
    )
    
    # Define all strategies
    strategies = [
        (Random(), "Random"),
        (TIT_FOR_TAT(), "TitForTat"),
        (ALL_D(), "AlwaysDefect"),
        (JOSS(), "JOSS"),
        (Tester(), "Tester"),
        (qlearner, "QLearn"),
        (NICE_GUY(), "NiceGuy"),
        (GrudgeHolder(), "GrudgeHolder")
    ]
    
    # Run a range of small and large tournament sizes
    num_games_options = [5, 10, 50, 100, 500, 1000, 10000]
    num_tournaments = 3  # Reduced for faster execution
    
    # Store results from all tournaments
    all_tournament_scores = {}
    all_tournament_details = {}
    
    # Run tournaments with different numbers of games
    for num_games in num_games_options:
        print(f"\nRunning tournament with {num_games} games per match...")
        
        # Run multiple tournaments and average the results
        avg_scores = {name: 0 for _, name in strategies}
        tournament_details = []
        cumulative_scores_by_strategy = {name: [] for _, name in strategies}
        total_games_played = {name: 0 for _, name in strategies}
        
        for t in range(num_tournaments):
            print(f"Tournament {t+1}/{num_tournaments}")

            
            # Create a fresh copy of strategies for each tournament
            fresh_strategies = [
                (Random(), "Random"),
                (TIT_FOR_TAT(), "TitForTat"),
                (ALL_D(), "AlwaysDefect"),
                (JOSS(), "JOSS"),
                (Tester(), "Tester"),
                (NICE_GUY(), "NiceGuy"),
                (qlearner, "QLearn"), 
                (GrudgeHolder(), "GrudgeHolder")
            ]
            
            scores, details, strategy_scores_by_game = tournament_round(
                fresh_strategies, 
                num_games, 
                show_individual_games
            )
            
            # Accumulate scores
            for name in avg_scores:
                avg_scores[name] += scores[name]
                
            tournament_details.append({
                'scores': scores,
                'details': details,
                'strategy_scores_by_game': strategy_scores_by_game
            })
            
            # Track cumulative scores - need to handle variable-length arrays
            for name, score_history in strategy_scores_by_game.items():
                # Extend cumulative_scores_by_strategy[name] if needed
                if len(cumulative_scores_by_strategy[name]) < len(score_history):
                    cumulative_scores_by_strategy[name].extend([0] * (len(score_history) - len(cumulative_scores_by_strategy[name])))
                
                # Add scores
                for i, score in enumerate(score_history):
                    cumulative_scores_by_strategy[name][i] += score
                    total_games_played[name] = max(total_games_played[name], i+1)
        
        # Average the scores
        for name in avg_scores:
            avg_scores[name] /= num_tournaments
            
        # Print results
        print("\nAverage scores after", num_tournaments, "tournaments:")
        for name, score in sorted(avg_scores.items(), key=lambda x: x[1]):
            print(f"{name}: {score:.2f} years in prison")
            
        # Store for later visualization
        all_tournament_scores[num_games] = avg_scores
        all_tournament_details[num_games] = {
            'tournament_details': tournament_details,
            'cumulative_scores_by_strategy': cumulative_scores_by_strategy,
            'total_games_played': total_games_played
        }
    
    # Visualize the results
    visualize_tournament_results(all_tournament_scores, all_tournament_details)

def visualize_tournament_results(all_tournament_scores, all_tournament_details):

    # Set up a colorful palette for strategies
    strategy_colors = {
        'Random': 'blue',
        'TitForTat': 'green',
        'AlwaysDefect': 'red',
        'JOSS': 'purple',
        'Tester': 'orange',
        'NiceGuy': 'yellow',
        'QLearn': 'cyan',
        'GrudgeHolder': 'pink'
    }
    
    # Extract data for plotting
    game_counts = sorted(all_tournament_scores.keys())
    strategies = list(all_tournament_scores[game_counts[0]].keys())
    
    # 1. Performance across different game counts
    plt.figure(figsize=(12, 8))
    
    for strategy in strategies:
        scores = [all_tournament_scores[count][strategy] for count in game_counts]
        plt.plot(game_counts, scores, marker='o', label=strategy, color=strategy_colors[strategy], linewidth=2)
    
    plt.title('Strategy Performance Across Different Tournament Lengths', fontsize=16)
    plt.xlabel('Number of Games per Match', fontsize=14)
    plt.ylabel('Average Years in Prison (Lower is Better)', fontsize=14)
    plt.xscale('log')  # Use log scale for x-axis to better show differences
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('strategy_performance_by_game_count.png', dpi=300)
    plt.close()
    
    # 2. Performance during a single match (for each game count)
    for num_games in [g for g in game_counts if g <= 1000]:
        if num_games not in all_tournament_details:
            continue
            
        plt.figure(figsize=(12, 8))
        cumulative_data = all_tournament_details[num_games]['cumulative_scores_by_strategy']
        total_games = all_tournament_details[num_games]['total_games_played']
        
        for strategy, scores in cumulative_data.items():
            # Only plot up to the number of games we actually have data for
            game_count = total_games[strategy]
            if game_count > 0:
                x = range(1, min(len(scores) + 1, game_count + 1))
                y = scores[:len(x)]
                plt.plot(x, y, label=strategy, color=strategy_colors[strategy], linewidth=2)
        
        plt.title(f'Cumulative Score During {num_games}-Game Tournament', fontsize=16)
        plt.xlabel('Game Number', fontsize=14)
        plt.ylabel('Cumulative Years in Prison (Lower is Better)', fontsize=14)
        if num_games > 100:
            plt.xscale('log')  # Use log scale for large game counts
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'cumulative_score_{num_games}_games.png', dpi=300)
        plt.close()
    
    # 3. Strategy ranking across different game counts
    plt.figure(figsize=(12, 8))
    
    # Calculate ranks (1 is best = lowest prison time)
    ranks_by_game_count = {}
    for count in game_counts:
        scores = all_tournament_scores[count]
        sorted_strategies = sorted(scores.keys(), key=lambda s: scores[s])
        ranks = {strategy: i+1 for i, strategy in enumerate(sorted_strategies)}
        ranks_by_game_count[count] = ranks
    
    # Plot ranks
    for strategy in strategies:
        ranks = [ranks_by_game_count[count][strategy] for count in game_counts]
        plt.plot(game_counts, ranks, marker='o', label=strategy, color=strategy_colors[strategy], linewidth=2)
    
    plt.title('Strategy Ranking Across Different Tournament Lengths (Lower is Better)', fontsize=16)
    plt.xlabel('Number of Games per Match', fontsize=14)
    plt.ylabel('Rank (1 = Best)', fontsize=14)
    plt.xscale('log')  # Use log scale for x-axis
    plt.yticks(range(1, len(strategies) + 1))
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('strategy_ranking_by_game_count.png', dpi=300)
    plt.close()
    
    # 4. Bar chart comparing strategy performance for specific game counts
    for num_games in [10, 100, 10000]:
        if num_games not in all_tournament_scores:
            continue
            
        plt.figure(figsize=(10, 6))
        
        scores = all_tournament_scores[num_games]
        sorted_items = sorted(scores.items(), key=lambda x: x[1])
        strategies_sorted = [item[0] for item in sorted_items]
        scores_sorted = [item[1] for item in sorted_items]
        
        bars = plt.bar(strategies_sorted, scores_sorted, color=[strategy_colors[s] for s in strategies_sorted])
        
        plt.title(f'Strategy Performance with {num_games} Games per Match', fontsize=16)
        plt.ylabel('Average Years in Prison (Lower is Better)', fontsize=14)
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(f'strategy_comparison_{num_games}_games.png', dpi=300)
        plt.close()
    
    # 5. Average scores normalized by tournament length
    plt.figure(figsize=(12, 8))
    
    for strategy in strategies:
        # Calculate average score per game
        normalized_scores = [all_tournament_scores[count][strategy] / count for count in game_counts]
        plt.plot(game_counts, normalized_scores, marker='o', label=strategy, color=strategy_colors[strategy], linewidth=2)
    
    plt.title('Average Score Per Game Across Tournament Lengths', fontsize=16)
    plt.xlabel('Number of Games per Match', fontsize=14)
    plt.ylabel('Avg Years in Prison Per Game (Lower is Better)', fontsize=14)
    plt.xscale('log')  # Use log scale for x-axis
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('normalized_scores_by_game_count.png', dpi=300)
    plt.close()
    
    # 6. Strategy convergence - at what tournament length does the ranking stabilize?
    plt.figure(figsize=(14, 10))
    
    # Prepare the plot with 5 subplots (one per strategy)
    fig, axs = plt.subplots(len(strategies), 1, figsize=(12, 3*len(strategies)), sharex=True)
    fig.suptitle('Strategy Performance Relative to Tournament Length', fontsize=16)
    
    for i, strategy in enumerate(strategies):
        y_values = [all_tournament_scores[count][strategy] for count in game_counts]
        axs[i].plot(game_counts, y_values, marker='o', color=strategy_colors[strategy], linewidth=2)
        axs[i].set_ylabel('Years in Prison', fontsize=12)
        axs[i].set_title(f"{strategy}", fontsize=14)
        axs[i].grid(True, alpha=0.3)
    
    axs[-1].set_xlabel('Number of Games per Match', fontsize=14)
    axs[-1].set_xscale('log')
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.savefig('strategy_convergence.png', dpi=300)
    plt.close()
    
    print("\nVisualization complete! All plots have been saved as PNG files.")

def main():
    run_tournament(show_individual_games=False)  # Set to True to see each move

if __name__ == "__main__":
    main()
