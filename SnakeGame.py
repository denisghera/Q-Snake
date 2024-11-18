import random

class SnakeGame:
    def __init__(self, rows: int, cols: int, cell_size: int):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.reset_game()

    def reset_game(self):
        self.snake_pos = [(self.cols // 2, self.rows // 2)]  # Snake starts at center
        self.food_pos = self.place_food()  # Place first food
        self.direction = 'UP'
        self.game_over = False

    def place_food(self):
        while True:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (y, x) not in self.snake_pos:
                return (y, x)
            
    def is_game_over(self):
        head_y, head_x = self.snake_pos[0]

        if head_y < 0 or head_y >= self.rows or head_x < 0 or head_x >= self.cols:
            self.game_over = True
            return True

        if self.snake_pos[0] in self.snake_pos[1:]:
            self.game_over = True
            return True

        if len(self.snake_pos) >= self.rows * self.cols:  # If snake occupies all available cells
            self.game_over = True
            return True

        return False


    def move_snake(self, action: str):
        if action == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif action == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif action == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif action == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

        head_y, head_x = self.snake_pos[0]

        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1

        # Insert new head at the new position
        self.snake_pos.insert(0, (head_y, head_x))

        # Check if the snake has eaten the food
        if (head_y, head_x) == self.food_pos:
            go = self.is_game_over()
            if not go:
                self.food_pos = self.place_food()
            return self.get_state(), 10, self.is_game_over()  # Reward for eating food
        else:
            if self.is_game_over():
                return self.get_state(), -10, True  # Negative reward for game over
            # Remove tail segment
            self.snake_pos.pop()
            return self.get_state(), -0.1, self.is_game_over()  # Small negative reward for moving extra

    def get_snake_pos(self):
        return self.snake_pos

    def get_food_pos(self):
        return self.food_pos

    def get_state(self):
        head_y, head_x = self.snake_pos[0]
        food_y, food_x = self.food_pos
        
        danger_up = int(head_y == 0 or (head_y - 1, head_x) in self.snake_pos)
        danger_down = int(head_y == self.rows - 1 or (head_y + 1, head_x) in self.snake_pos)
        danger_left = int(head_x == 0 or (head_y, head_x - 1) in self.snake_pos)
        danger_right = int(head_x == self.cols - 1 or (head_y, head_x + 1) in self.snake_pos)

        return (head_y, head_x, food_y, food_x, danger_up, danger_down, danger_left, danger_right)
