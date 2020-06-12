import gym
from gym import spaces
import pygame
from gym_pong.envs.pong_pygame import PongPygame

class PygameEnv(gym.Env):

    def __init__(self):
        self.pygame = PongPygame()
        self.action_space = spaces.Discrete(3)

    def step(self, action):
        self.pygame.action(action)

    def render(self, mode='human'):
        self.pygame.view()

