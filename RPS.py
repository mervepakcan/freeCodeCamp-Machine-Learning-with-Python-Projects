import random

def player(prev_play, opponent_history=[], play_counts={"R": 0, "P": 0, "S": 0}, strategies={}, strategy=None):
    if prev_play:
        opponent_history.append(prev_play)
        play_counts[prev_play] += 1

    # Step 1: First few rounds - collect data
    if len(opponent_history) < 50:
        return random.choice(["R", "P", "S"])  # Random play for first few moves

    # Step 2: Determine opponent strategy
    if strategy is None:
        # Check if the opponent plays randomly
        move_counts = list(play_counts.values())
        max_diff = max(move_counts) - min(move_counts)
        if max_diff < 10:  # If move distribution is balanced, assume random bot
            strategy = "random"

        # Check if the opponent follows a cycle
        last_moves = "".join(opponent_history[-10:])
        for cycle_length in range(2, 6):
            pattern = last_moves[-cycle_length:]
            if last_moves.count(pattern) > 1:
                strategy = "cycle"
                strategies["cycle_pattern"] = pattern
                break

        # Check if the opponent is reacting to my moves
        if strategy is None and len(opponent_history) > 5:
            if opponent_history[-5:] == ["R", "P", "S", "R", "P"]:
                strategy = "reactive"

        # Default to frequency-based strategy if no other pattern found
        if strategy is None:
            strategy = "frequency"

    # Step 3: Apply strategy
    if strategy == "random":
        return random.choice(["R", "P", "S"])  # Play randomly if opponent is random

    elif strategy == "cycle":
        # Predict the next move in the cycle
        cycle_pattern = strategies["cycle_pattern"]
        predicted_next_move = cycle_pattern[len(opponent_history) % len(cycle_pattern)]
        counter_moves = {"R": "P", "P": "S", "S": "R"}
        return counter_moves[predicted_next_move]

    elif strategy == "reactive":
        # Assume opponent reacts to our previous move, so we play unpredictably
        return random.choice(["R", "P", "S"])

    elif strategy == "frequency":
        # Counter the most frequent move
        most_common = max(play_counts, key=play_counts.get)
        counter_moves = {"R": "P", "P": "S", "S": "R"}
        return counter_moves[most_common]

    return "R"  # Default fallback


