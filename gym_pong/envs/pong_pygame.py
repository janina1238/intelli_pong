import numpy as np
import pygame
from random import randint
from random import choice
from random import uniform
import math

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
        self.velocity = 20
        self.direction = 'Up'  # only used for the right paddle animation

    def draw(self):
        """
        return:
            a rect shaped paddle
        """
        rect = pygame.draw.rect(self._render, WHITE, pygame.Rect(self.x, self.y, self.width, self.height))
        return rect

    def animate(self):
        """
        Animate the right paddle
        """
        if self.y < 55:
            self.direction = 'Down'

        elif self.y > 400:
            self.direction = 'Up'

        if self.direction == 'Down':
            self.y += self.velocity

        elif self.direction == 'Up':
            self.y -= self.velocity

    def update(self):
        """
        Update the position of the paddle if it reaches the border
        """
        if self.y < 55:
            self.y = 55
        elif self.y > 500 - self.height:
            self.y = 500 - self.height


class PaddleEnemy:

    def __init__(self, pos, size, _render=None):
        self.pos = pos  # position of the paddle on the x and y axes
        self.size = size  # size of the paddle, width and height

        self.x = self.pos[0]  # position of the paddle on the x axis
        self.y = self.pos[1]  # position of the paddle on the y axis

        self.width = self.size[0]  # width of the paddle
        self.height = self.size[1]  # height of the paddle

        self._render = _render  # surface
        self.velocity = 20
        self.direction = 'Up'  # only used for the right paddle animation

    def draw(self):
        """
        return:
            a rect shaped paddle
        """
        rect = pygame.draw.rect(self._render, WHITE, pygame.Rect(self.x, self.y, self.width, self.height))
        return rect

    def animate(self):
        """
        Animate the right paddle
        """
        if self.y < 55:
            self.direction = 'Down'

        elif self.y > 400:
            self.direction = 'Up'

        if self.direction == 'Down':
            self.y += self.velocity

        elif self.direction == 'Up':
            self.y -= self.velocity

    def update(self):
        """
        Update the position of the paddle if it reaches the border
        """
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
        self.velocity = 7 # randint(4, 8)  # set a random velocity at the beginning of every episode

        self.direction = choice([-self.velocity, self.velocity]), choice([-self.velocity, self.velocity])
        self.dx, self.dy = self.direction

        self.c = math.sqrt(self.dx**2 + self.dy**2)

        self.scoreA = 0  # left paddle score
        self.scoreB = 0  # right paddle score
        self.reward_flag = 0  # changes if a player gets a point
        self.reward_flag_enemy = 0

    def draw(self):
        """
        return:
            a rect shaped ball
        """
        rect = pygame.draw.rect(self._render, WHITE, pygame.Rect(self.x, self.y, self.width, self.height))
        return rect

    def update(self):
        """
        Update the position of the ball in every frame.
        Check if the ball collides with any of the 4 walls.
        Switch direction if it does and update score.
        For a varying angle, slightly change the dx value.
        Then correct the dy value, so the velocity stays the same.
        """
        self.x += self.dx
        self.y += self.dy
        rand_x = 700 / 2  # choice([(700 / 2), (700 - self.width)])  # (700-30)])
        rand_y = choice([55, 305, (500 - self.height)])
        rand_dx = choice([-(self.velocity + uniform(-1.5, 1.5)), (self.velocity + uniform(-1.5, 1.5))])

        if self.y < 55:
            self.dy *= -1
        elif self.y > 500 - self.height:
            self.dy *= -1
        elif self.x > 700 - self.width:
            self.scoreA += 1
            self.reward_flag = 1
            self.reward_flag_enemy = 2
            self.x = rand_x
            self.y = rand_y
            self.dx = rand_dx
        elif self.x < 0:
            self.scoreB += 1
            self.reward_flag = 2
            self.reward_flag_enemy = 1
            self.x = rand_x
            self.y = rand_y
            self.dx = rand_dx

    def check_collision(self, paddle_a, paddle_b):
        """
        Check if the ball collides with one of the paddles and change the direction.
        For a varying angle, slightly change the dx value.
        Then correct the dy value, so the velocity stays the same.
        paddle_a:
            left paddle to check collision
        paddle_b:
            right paddle to check collision
        """
        if self.draw().colliderect(paddle_a.draw()):
            self.dx = (self.velocity + uniform(-1.5, 1.5))
            if self.dy < 0:
                self.dy = math.sqrt(self.c ** 2 - self.dy ** 2) * -1
            else:
                self.dy = math.sqrt(self.c ** 2 - self.dy ** 2)

        if self.draw().colliderect(paddle_b.draw()):
            self.dx = -(self.velocity + uniform(-1.5, 1.5))
            if self.dy < 0:
                self.dy = math.sqrt(self.c ** 2 - self.dy ** 2) * -1
            else:
                self.dy = math.sqrt(self.c ** 2 - self.dy ** 2)


class PongPygame:

    def __init__(self):
        self.w = 700  # screen width
        self.h = 500  # screen height

        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))  # initialize the screen
        self.clock = pygame.time.Clock()  # to control how fast the screen updates

        self.paddle_a = Paddle((20, 200), (10, 100), self.screen)  # first paddle object
        self.paddle_b = Paddle((670, 200), (10, 100), self.screen)  # second paddle object

        self.ball = Ball((337.5, randint(100, 400)), (25, 25), self.screen)  # ball object

        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)  # set score font

        self.ball_array = np.zeros([2, 2])
        self.paddle_array = np.zeros([2, 2])

        self.sum_reward = 0

    def action(self, action):
        """
        action:
            move up, move down, don't move
        """
        if action == 0:
            self.paddle_a.y -= self.paddle_a.velocity  # move up
        if action == 1:
            self.paddle_a.y += self.paddle_a.velocity  # move down
        # action == 2, don't move

        self.paddle_a.update()
        self.ball.check_collision(self.paddle_a, self.paddle_b)
        self.ball.update()

    def action_enemy(self, action):
        """
        action:
            move up, move down, don't move
        """
        if action == 0:
            self.paddle_b.y -= self.paddle_b.velocity  # move up
        if action == 1:
            self.paddle_b.y += self.paddle_b.velocity  # move down
        # action == 2, don't move

        self.paddle_b.update()
        self.ball.check_collision(self.paddle_a, self.paddle_b)
        #self.ball.update()

    def reward(self):
        """
        return:
            reward if one player gets a point
        """
        reward = 0
        # point for the agent -> reward +1
        if self.ball.reward_flag == 1:
            reward += 1
            self.ball.reward_flag = 0
            return reward
        # point for the enemy -> reward -1
        if self.ball.reward_flag == 2:
            reward -= 1
            self.ball.reward_flag = 0
            return reward
        return reward

    def reward_enemy(self):
        """
        return:
            reward if one player gets a point
        """
        reward = 0
        # point for the agent -> reward +1
        if self.ball.reward_flag_enemy == 1:
            reward += 1
            self.ball.reward_flag_enemy = 0
            return reward
        # point for the enemy -> reward -1
        if self.ball.reward_flag_enemy == 2:
            reward -= 1
            self.ball.reward_flag_enemy = 0
            return reward
        return reward

    def is_done(self):
        """
        return:
            true if a player reaches 10 points
        """
        done = False
        if self.ball.scoreA == 10 or self.ball.scoreB == 10:
            done = True
            self.ball.dx = -(self.ball.velocity + uniform(-1.5, 1.5))
            print("ScoreA: " + str(self.ball.scoreA))
        return done

    def is_done_enemy(self):
        """
        return:
            true if a player reaches 10 points
        """
        done = False
        if self.ball.scoreA == 10 or self.ball.scoreB == 10:
            done = True
            self.ball.dx = -(self.ball.velocity + uniform(-1.5, 1.5))
            print("ScoreB: " + str(self.ball.scoreB))
        return done

    def observe(self):
        """
        return:
            state of the ball (direction) if prev_frame is not 0
        """
        ball_x = self.ball.x
        ball_y = self.ball.y
        paddle_x = self.paddle_a.x
        paddle_y = self.paddle_a.y
        state = np.zeros([4])

        state[0] = ball_x
        state[1] = ball_y
        state[2] = paddle_x
        state[3] = paddle_y
        return state

    def observe_enemy(self):
        """
        return:
            state of the ball (direction) if prev_frame is not 0
        """
        ball_x = self.ball.x
        ball_y = self.ball.y
        paddle_x = self.paddle_b.x
        paddle_y = self.paddle_b.y
        state = np.zeros([4])

        state[0] = ball_x
        state[1] = ball_y
        state[2] = paddle_x
        state[3] = paddle_y
        return state

    def view(self):
        """
        Draw the game
        """
        self.clock.tick(FPS)  # Limit to 60 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    quit()

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

        pygame.display.update()
