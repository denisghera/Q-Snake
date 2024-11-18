import math, pickle, random, os

class QAgent:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.q_table = {}
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995  # Decay rate for epsilon
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.alpha = 0.7  # Increased learning rate for faster adaptation
        self.gamma = 0.95  # Higher discount factor for longer-term rewards
        self.state_action_counts = {}
        self.load_q_table()

    def choose_action(self, state):
        state_str = str(state)
        
        if state_str not in self.q_table or len(self.q_table[state_str]) == 0:
            return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        
        if random.random() < self.epsilon:
            return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        else:
            return max(self.q_table[state_str], key=self.q_table[state_str].get, default=random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']))

    def update_q_table(self, state, action, reward, next_state):
        state_str = str(state)
        next_state_str = str(next_state)

        if state_str not in self.q_table:
            self.q_table[state_str] = {a: 0 for a in ['UP', 'DOWN', 'LEFT', 'RIGHT']}
        if next_state_str not in self.q_table:
            self.q_table[next_state_str] = {a: 0 for a in ['UP', 'DOWN', 'LEFT', 'RIGHT']}
        
        # Update the state-action count to track how often this pair has been visited
        if (state_str, action) not in self.state_action_counts:
            self.state_action_counts[(state_str, action)] = 0
        self.state_action_counts[(state_str, action)] += 1
        
        # Dynamic learning rate to make the agent more confident over time
        count = self.state_action_counts[(state_str, action)]
        dynamic_alpha = 1 / (1 + math.log(1 + count))

        # Q-learning update formula with dynamic alpha
        current_q = self.q_table[state_str][action]
        max_future_q = max(self.q_table[next_state_str].values())
        new_q = (1 - dynamic_alpha) * current_q + dynamic_alpha * (reward + self.gamma * max_future_q)
        self.q_table[state_str][action] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save_q_table(self):
        filename = f'q_table_{self.rows}x{self.cols}.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self):
        filename = f'q_table_{self.rows}x{self.cols}.pkl'
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
                print("Q-Table loaded from file...")
        else:
            print("Q-Table file wasn't found. Starting fresh...")
