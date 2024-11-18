import pygame, sys, psutil

from GUI import *
from QAgent import *
from SnakeGame import *

ROWS = 5
COLS = 5
CELL_SIZE = 80
GAME_SPEED = 5

TRAINING = False 
EPISODES = 50000

def monitor_memory():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    return mem

def run_training(agent: QAgent, game: SnakeGame, gui : GUI):
    for episode in range(1, EPISODES + 1):
        game.reset_game()
        total_reward = 0
        done = False

        while not done:
            state = game.get_state()
            action = agent.choose_action(state)
            next_state, reward, done = game.move_snake(action)
            agent.update_q_table(state, action, reward, next_state)
            total_reward += reward

            # gui.draw_elements()

            if game.is_game_over():
                done = True

        agent.decay_epsilon()
        memory_used = monitor_memory()
        print(f"Episode {episode}/{EPISODES} - Total Reward: {total_reward:.1f}  - Memory Used: {memory_used:.2f} MB")

        # Save the Q-table periodically
        if episode % 1000 == 0:
            agent.save_q_table()

    agent.save_q_table()

if __name__ == "__main__":
    game = SnakeGame(ROWS, COLS, CELL_SIZE)
    gui = GUI(game, GAME_SPEED)
    agent = QAgent(ROWS, COLS)

    if TRAINING:
        run_training(agent, game, gui)
        print("Training finished, saving Q-table...")
    else:
        try:
            agent.epsilon = 0  # Exploit only (no exploration)

            while True:
                game.reset_game()
                done = False

                while not done:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            print("Exiting game by X...")
                            pygame.quit()
                            sys.exit()
                    
                    state = game.get_state()
                    action = agent.choose_action(state)
                    next_state, reward, done = game.move_snake(action)
                    
                    if game.is_game_over():
                        done = True
                    
                    gui.draw_elements()

                pygame.time.delay(100)

        except KeyboardInterrupt:
            print("Exiting game by ctrl+c...")
            pygame.quit()
            sys.exit()