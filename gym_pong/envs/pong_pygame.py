import numpy as np
import pygame
import random
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60


class Paddle:

    def __init__(self, pos, size, _render=None):
        self.pos = pos  # position of the paddle on the x and y axes
        self.size = size  # size of the paddle, width and height

        self.x = self.pos[0]  # position of the paddle on the x axis
        self.y = self.pos[1]  # position of the paddle on the y axis

        self.width = self.size[0]  # width of the paddle
        self.height = self.size[1]  # height of the paddle

        self._render = _render  # surface
        self.velocity = 10
        self.direction = 'Up'

    # draw a paddle
    def draw(self):
        rect = pygame.draw.rect(self._render, WHITE, pygame.Rect(self.x, self.y, self.width, self.height))
        return rect

    # animate the right paddle!!
    def animate(self):
        if self.y < 55:
            self.direction = 'Down'

        elif self.y > 400:
            self.direction = 'Up'

        if self.direction == 'Down':
            self.y += self.velocity

        elif self.direction == 'Up':
            self.y -= self.velocity

        self.draw()

    def update(self):
        # check position
        if self.y < 55:
            self.y = 55
        elif self.y > 500 - self.height:
            self.y = 500 - self.height


class Ball:

    def __init__(self, pos, size, _render=None):

        self.pos = pos  # starting position of the ball on the x and y axes
        self.size = size  # size of the ball

        self.x = self.pos[0]  # starting position of the ball on the x axis
        self.y = self.pos[1]  # starting position of the ball on the y axis

        self.width = self.size[0]  # width of the ball
        self.height = self.size[1]  # height of the ball

        self._render = _render  # surface
        self.velocity = randint(4, 8)  # speed

        self.direction = random.choice([-self.velocity, self.velocity]), random.choice([-self.velocity, self.velocity])
        self.dx, self.dy = self.direction
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.scoreA = 0
        self.scoreB = 0
        self.reward_flag = 0

    # draw ball
    def draw(self):
        rect = pygame.draw.rect(self._render, WHITE, self.rect)
        return rect

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check if the ball is bouncing against any of the 4 walls
        # switch direction if they do and update score
        if self.rect.y < 55:
            self.dy *= -1
        elif self.rect.y > 500 - self.height:
            self.dy *= -1
        elif self.rect.x > 700 - self.width:
            self.scoreA += 1
            self.reward_flag = 1
            self.dx *= -1
        elif self.rect.x < 25 - self.width:
            self.scoreB += 1
            self.reward_flag = 2
            self.dx *= -1

    def check_collision(self, paddle_a, paddle_b):
        # switch direction when ball collides with paddle
        if self.rect.colliderect(paddle_a.draw()):
            self.dx = self.velocity
        if self.rect.colliderect(paddle_b.draw()):
            self.dx = -self.velocity


class PongPygame:

    def __init__(self):
        self.w = 700  # screen width
        self.h = 500  # screen height

        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))  # initialize the screen
        self.clock = pygame.time.Clock()

        self.paddle_a = Paddle((20, 200), (10, 100), self.screen)  # first paddle object
        self.paddle_b = Paddle((670, 200), (10, 100), self.screen)  # second paddle object

        self.ball = Ball((337.5, random.randint(100, 400)), (25, 25), self.screen)  # ball object

        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)  # set score

        self.state_array = np.zeros([2, 2])

    # set action for the left paddle
    def action(self, action):
        if action == 0:
            self.paddle_a.y -= self.paddle_a.velocity  # move up
        if action == 1:
            self.paddle_a.y += self.paddle_a.velocity  # move down
        # action == 2, don't move

        self.ball.update()
        self.paddle_a.update()
        self.ball.check_collision(self.paddle_a, self.paddle_b)

    # amount of reward achieved by the previous action
    def reward(self):
        reward = 0
        # point for the agent -> reward +1
        if self.ball.reward_flag == 1:
            reward = 1
            self.ball.reward_flag = 0
            return reward
        # point for the enemy -> reward -1
        if self.ball.reward_flag == 2:
            reward = -1
            self.ball.reward_flag = 0
            return reward
        return reward

    def is_done(self):
        done = False
        # if one of the players reach 10 points
        if self.ball.scoreA == 10 or self.ball.scoreB == 10:
            done = True
        return done

    def observe(self):
        x = self.ball.rect.x
        y = self.ball.rect.y

        new_frame = [x, y]  # set the current x and y position of the ball
        prev_frame = self.state_array[0]  # move the current frame to previous frame
        self.state_array[1] = prev_frame  # set previous frame in pos 1
        self.state_array[0] = new_frame  # set current frame in pos 0

        # subtract the previous frame from the current one so we are only processing on changes in the game
        # (direction of the ball)
        if 0 not in self.state_array[1]:
            state = self.state_array[0] - self.state_array[1]
            return state

    def view(self):
        # draw game
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                '''
                if event.key == pygame.K_w:
                    self.paddle_a.rect.move_ip(0, -4)
                if event.key == pygame.K_s:
                    self.paddle_a.rect.move_ip(0, 4)
                '''
                if event.key == pygame.K_UP:
                    self.paddle_b.rect.move_ip(0, -4)
                if event.key == pygame.K_DOWN:
                    self.paddle_b.rect.move_ip(0, 4)

        self.screen.fill(BLACK)  # reset the latest frame

        # draw field lines
        pygame.draw.line(self.screen, WHITE, [349, 0], [349, 500], 5)  # vertical field line
        pygame.draw.line(self.screen, WHITE, [0, 50], [700, 50], 5)  # horizontal field line

        # draw paddles
        self.paddle_a.draw()  # draw left paddle on the field
        self.paddle_b.draw()  # draw right paddle on the field

        # draw ball
        self.ball.draw()

        # set score
        score_left = self.fontObj.render(str(self.ball.scoreA), True, WHITE)
        score_right = self.fontObj.render(str(self.ball.scoreB), True, WHITE)

        # display score
        self.screen.blit(score_left, (170, 10))  # left score
        self.screen.blit(score_right, (525, 10))  # right score

        self.paddle_b.animate()

        pygame.display.update()
