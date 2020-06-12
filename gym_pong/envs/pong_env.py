import gym
from gym import spaces
import pygame
from gym_pong.envs.pong_pygame import PongPygame

class PygameEnv(gym.Env):

    def __init__(self):
        self.ponggame = PongPygame()
        self.action_space = spaces.Discrete(3)

    def step(self, action):
        self.ponggame.action(action)
        reward = self.ponggame.reward()

        return reward

    def render(self, mode='human'):
        self.ponggame.view()

