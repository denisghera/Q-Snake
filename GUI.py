import pygame
from SnakeGame import SnakeGame

class GUI:
    def __init__(self, game : SnakeGame, speed : int):
        self.game = game
        self.speed = speed
        pygame.init()
        self.screen = pygame.display.set_mode((game.cols * game.cell_size, game.rows * game.cell_size))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

    def draw_elements(self):
        # Draw environment
        self.screen.fill((0, 0, 0))
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                pygame.draw.rect(self.screen, (255, 255, 255), (col * self.game.cell_size, row * self.game.cell_size, self.game.cell_size, self.game.cell_size), 1)  # Border width 1

        # Draw head of snake
        head_y, head_x = self.game.get_snake_pos()[0]
        pygame.draw.rect(self.screen, (0, 255, 0), (head_x * self.game.cell_size, head_y * self.game.cell_size, self.game.cell_size, self.game.cell_size)) 
        
        # Draw body of snake if it exists
        if len(self.game.get_snake_pos()) > 1:
            for y, x in self.game.get_snake_pos()[1:]:
                pygame.draw.rect(self.screen, (255, 255, 0), (x * self.game.cell_size, y * self.game.cell_size, self.game.cell_size, self.game.cell_size))

        # Draw food
        food_y, food_x = self.game.get_food_pos()
        pygame.draw.rect(self.screen, (255, 0, 0), (food_x * self.game.cell_size, food_y * self.game.cell_size, self.game.cell_size, self.game.cell_size))

        pygame.display.flip()
        self.clock.tick(self.speed)
