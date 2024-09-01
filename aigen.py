import random

def simulate_monty_hall(num_trials=1000):
    switch_wins = 0
    stay_wins = 0

    for _ in range(num_trials):
        doors = [0, 0, 1]  # Two goats (0) and one car (1)
        random.shuffle(doors)  # The prizes are randomly assigned

        # The contestant's initial choice is random
        choice = random.choice([0, 1, 2])

        # Monty opens a door
        monty_opens = 0
        for i in range(3):
            if i != choice and doors[i] == 0:
                monty_opens = i
                break

        # If the contestant switches their choice
        switch_choice = 3 - choice - monty_opens
        if doors[switch_choice] == 1:
            switch_wins += 1

        # If the contestant stays with their initial choice
        if doors[choice] == 1:
            stay_wins += 1

    print(f"Switching wins: {switch_wins/num_trials*100}% of the time")
    print(f"Staying wins: {stay_wins/num_trials*100}% of the time")

simulate_monty_hall()