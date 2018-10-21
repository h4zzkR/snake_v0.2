import pygame
import sys
import random
import time


def get_pos(screen_width, screen_height):
    food_pos = (random.randrange(1, screen_width / 10) * 10, random.randrange(1, screen_height / 10) * 10)
    #ТОЛЬКО ТАК И РАБОТАЕТ, НЕ ТРОГАТЬ
    return food_pos

class Snake():

    def __init__(self):
        self.screen_width = 720
        self.screen_height = 400
        self.snake_body = [[200, 50], [190, 50], [180, 50]]
        self.head = [self.snake_body[0][0], self.snake_body[0][1]]
        self.snake_color = pygame.Color(255, 255, 255)
        self.state = "RIGHT"
        self.move = self.state
        self.food_pos = get_pos(self.screen_width, self.screen_height)
        self.food_color = self.snake_color

    def __set__(self):
        pygame.display.set_caption('Snake')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.fps = pygame.time.Clock()
        self.background = pygame.transform.scale(pygame.image.load('images/grass.png'),
                                                 (self.screen_width, self.screen_height))

    def sort_direction(self):
        if any((self.move == "EXIT",
                self.move == "LEFT" and not self.state == "RIGHT",
                self.move == "RIGHT" and not self.state == "LEFT",
                self.move == "UP" and not self.state == "DOWN",
                self.move == "DOWN" and not self.state == "UP")):
            self.state = self.move

    def change_position(self):
        if self.state == "EXIT":
            pygame.quit()
            sys.exit()
        elif self.state == "RIGHT":
            self.head[0] += 10
        elif self.state == "LEFT":
            self.head[0] -= 10
        elif self.state == "UP":
            self.head[1] -= 10
        elif self.state == "DOWN":
            self.head[1] += 10

    def snake_move(self):
        self.snake_body.insert(0, list(self.head))
        if self.head[0] == self.food_pos[0] and self.head[1] == self.food_pos[1]:
            self.food_pos = get_pos(self.screen_width, self.screen_height)
        else:
            self.snake_body.pop()

    def draw_snake(self):
        self.screen.blit(self.background, (0, 0))
        for box in self.snake_body:
            pygame.draw.rect(self.screen, self.snake_color, pygame.Rect(box[0], box[1], 10, 10))

    def logic(self):
        if self.head[0] > self.screen_width-10 or \
                self.head[0] < 0 or self.head[1] > \
                self.screen_height-10 or self.head[1] < 0:
            self.game_over()
        else:
            for box in self.snake_body[1:]:
                if (box[0] == self.head[0] and
                        box[1] == self.head[1]):
                    self.game_over()
                    break

    def draw_food(self):
        pygame.draw.rect(self.screen, self.get_color(), pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))
        #draw KWADRATIC!!!

    def get_color(self):
        colors = (pygame.Color(255, 0, 0), pygame.Color(0, 255, 0),
                  pygame.Color(255, 255, 255), pygame.Color(165, 42, 42))
        return colors[random.randrange(0, 4)]

    def game_over(self):
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

#OH, OH, IT`S MAGIC, MAN!
snake = Snake()
snake.__set__()


def event():
    move = ""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.key == 100:
                move = "RIGHT"
            elif event.key == 97:
                move = "LEFT"
            elif event.key == 119:
                move = "UP"
            elif event.key == 115:
                move = "DOWN"
            elif event.key == 27:
                print(event.key)
                time.sleep(3)
    snake.move = move


def render():
    snake.fps.tick(28)
    pygame.display.flip()

while True:
    event()
    snake.sort_direction()
    snake.change_position()
    snake.snake_move()
    snake.draw_snake()
    snake.draw_food()
    snake.logic()
    #is our snake alive
    render()

#TODO make more food, not one, snake is hungry
