import random
from collections import Counter

# Simulate games between two player strategies
def play(player1, player2, num_games, verbose=False):
    # Initialize previous moves and game results.
    p1_prev_play = ""
    p2_prev_play = ""
    results = {"p1": 0, "p2": 0, "tie": 0}
    
    # Win conditions
    wins = {"R": "S", "P": "R", "S": "P"}
    
    for _ in range(num_games):
        # Each player chooses a move based on the opponent's previous play
        p1_play = player1(p2_prev_play)
        p2_play = player2(p1_prev_play)

        if p1_play == p2_play:
            results["tie"] += 1
            winner = "Tie."
        elif wins[p1_play] == p2_play:
            results["p1"] += 1
            winner = "Player 1 wins."
        elif wins[p2_play] == p1_play:
            results["p2"] += 1
            winner = "Player 2 wins."

        if verbose:
            print("Player 1:", p1_play, "| Player 2:", p2_play)
            print(winner)
            print()

        p1_prev_play = p1_play
        p2_prev_play = p2_play

    games_won = results["p1"] + results["p2"]
    win_rate = 0 if games_won == 0 else results["p1"] / games_won * 100

    print("Final results:", results)
    print(f"Player 1 win rate: {win_rate}%")
    return win_rate

# Strategy: Quincy
# Cycles through a fixed pattern
def quincy(prev_play, counter=[0]):
    counter[0] += 1
    choices = ["R", "R", "P", "P", "S"]
    return choices[counter[0] % len(choices)]

# Strategy: Mrugesh
# Analyzes the opponent's last 10 moves and counters the most frequent move
def mrugesh(prev_opponent_play, opponent_history=[]):
    opponent_history.append(prev_opponent_play)
    last_ten = opponent_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)
    if most_frequent == "":
        most_frequent = "S"
    ideal_response = {"P": "S", "R": "P", "S": "R"}
    return ideal_response[most_frequent]

# Strategy: Kris
# Simply counters the opponent's last move, defaulting to "R" if no move is available
def kris(prev_opponent_play):
    if prev_opponent_play == "":
        prev_opponent_play = "R"
    ideal_response = {"P": "S", "R": "P", "S": "R"}
    return ideal_response[prev_opponent_play]

# Strategy: Abbey
# Uses frequency analysis of two-move patterns to predict the opponent's next move and counters it
def abbey(prev_opponent_play, opponent_history=[], play_order=[{
    "RR": 0, "RP": 0, "RS": 0, 
    "PR": 0, "PP": 0, "PS": 0, 
    "SR": 0, "SP": 0, "SS": 0,
}]):
    if not prev_opponent_play:
        prev_opponent_play = "R"
    opponent_history.append(prev_opponent_play)
    
    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    # Build potential patterns for prediction
    potential_plays = [prev_opponent_play + "R", prev_opponent_play + "P", prev_opponent_play + "S"]
    sub_order = {k: play_order[0][k] for k in potential_plays if k in play_order[0]}
    prediction = max(sub_order, key=sub_order.get)[-1]  # Get the predicted next move

    ideal_response = {"P": "S", "R": "P", "S": "R"}
    return ideal_response[prediction]

# Strategy: Human
# Takes user input for move
def human(prev_opponent_play):
    play = ""
    while play not in ["R", "P", "S"]:
        play = input("[R]ock, [P]aper, [S]cissors? ")
        print(play)
    return play

# Strategy: Random Player
# Plays a random move
def random_player(prev_opponent_play):
    return random.choice(["R", "P", "S"])

# Move counter: selects the winning move against the opponent's choice
counter_move = {"R": "P", "P": "S", "S": "R"}

# Tracks opponent's move patterns for prediction
steps = {}

# Strategy: Adaptive Pattern Predictor (player)
# Predicts opponent's move based on pattern history and counters it
def player(prev_play, opponent_history=[]):
    if prev_play != "":
        opponent_history.append(prev_play)

    n = 5  # Number of moves to consider for pattern prediction
    guess = "R"
    if len(opponent_history) > n:
        pattern = join(opponent_history[-n:])
        prev_pattern = join(opponent_history[-(n + 1):])
        steps[prev_pattern] = steps.get(prev_pattern, 0) + 1

        # Generate possible next move patterns
        possible = [pattern + "R", pattern + "P", pattern + "S"]
        for move in possible:
            steps.setdefault(move, 0)

        # Predict the opponent's next move based on the most frequent pattern
        predict = max(possible, key=lambda key: steps[key])
        guess = counter_move[predict[-1]]
    return guess

def join(moves):
    return "".join(moves)

# Run simulations
play(player, quincy, 1000)
play(player, mrugesh, 1000)
play(player, abbey, 1000)
play(player, kris, 1000)
