import sys, pygame, random
from random import randint
from pygame import Vector2

#Init---------------------------------------------------------------------------
pygame.init()
title_font = pygame.font.Font(None, 60)
score_font= pygame.font.Font(None, 60)

#Constants-----------------------------------------------------------------------
TICK_SPEED = 999999
CELL_SIZE = 30
CELL_NUM = 25
OFFSET = 75

WIDTH, HEIGHT = CELL_SIZE*CELL_NUM, CELL_SIZE*CELL_NUM

LIGHT_BLUE = (20, 51, 112)
DARK_BLUE = (4, 23, 61)

#Classes-------------------------------------------------------------------------
class Snake:
    def __init__(self):
        self.body = [Vector2(11,13), Vector2(10,13), Vector2(9,13)]
        self.direction = Vector2(1, 0)
        self.next_direction = self.direction #prevents conflicting key presses

    def move(self):
        self.direction = self.next_direction #prevents conflicting key presses
        self.body = self.body[:-1]
        self.body.insert(0, self.body[0] + self.direction)


    def draw(self):
        for each in self.body:
            snake_body = pygame.Rect(OFFSET + each.x * CELL_NUM, OFFSET + each.y * CELL_NUM, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, DARK_BLUE, snake_body, 0, 9)

class Food:
    def __init__(self, snake_body):
        self.coords = self.random_position(snake_body)

    def draw(self):
        food_body = pygame.Rect(OFFSET + self.coords.x * CELL_NUM , OFFSET + self.coords.y * CELL_NUM, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 0, 0), food_body)

    def random_cell(self):
        x = randint(0, CELL_NUM - 1)
        y = randint(0, CELL_NUM - 1)
        return Vector2(x, y)

    def random_position(self, snake_body):
        coords = self.random_cell()

        while coords in snake_body:
            coords = self.random_cell()
        return coords

class Main:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = True
        self.score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self):
        if self.state:
            self.snake.move()
            self.eat_food()
            self.check_collision()

    def eat_food(self):
        if self.snake.body[0] == self.food.coords:
            self.score += 1
            self.food.coords =  self.food.random_position(self.snake.body)
            self.snake.body.insert(0, self.snake.body[0] + self.snake.direction)

    def check_collision(self):

        #collision with wall
        if  not 0 <= self.snake.body[0].x < CELL_SIZE or not 0 <= self.snake.body[0].y < CELL_SIZE:
            self.game_over()

        #collision with snake body
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.body = [Vector2(11, 13), Vector2(10, 13), Vector2(9, 13)]
        self.snake.direction = Vector2(1, 0)
        self.food.coords = self.food.random_position(self.snake.body)
        self.state = False

#Main Code-----------------------------------------------------------------------
screen = pygame.display.set_mode((2 * OFFSET + WIDTH, 2 * OFFSET + HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("snoke game")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 100)

main = Main()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SNAKE_UPDATE:
                main.update()

        if event.type == pygame.KEYDOWN:
            if main.state == False:
                main.score = 0
                main.state = True
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and main.snake.direction != Vector2(0, 1):
                main.snake.next_direction = Vector2(0, -1) #direction updates once per move cycle
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and main.snake.direction != Vector2(0, -1):
                main.snake.next_direction = Vector2(0, 1)
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and main.snake.direction != Vector2(-1, 0):
                main.snake.next_direction = Vector2(1, 0)
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and main.snake.direction != Vector2(1, 0):
                main.snake.next_direction = Vector2(-1, 0)

    screen.fill(LIGHT_BLUE)

    title_surface = title_font.render("Retro Snoke",True ,DARK_BLUE)
    screen.blit(title_surface, (OFFSET-5, 20))

    score_surface = score_font.render(str(main.score), True, DARK_BLUE)
    screen.blit(score_surface, (WIDTH + 10, 20))

    main.draw()
    pygame.draw.rect(screen, DARK_BLUE,(OFFSET - 5, OFFSET - 5, WIDTH + 10, HEIGHT + 10) ,5)
    pygame.display.update()
    clock.tick(TICK_SPEED)









