import gym
from gym import spaces
import pygame
from gym_pong.envs.pong_pygame import PongPygame

class PygameEnv(gym.Env):

    def __init__(self):
        self.ponggame = PongPygame()
        self.action_space = spaces.Discrete(3)

    def reset(self):
        del self.ponggame
        self.ponggame = PongPygame()
        obs = self.ponggame.observe()
        return obs

    def step(self, action):
        self.ponggame.action(action)
        reward = self.ponggame.reward()
        obs = self.ponggame.observe()
        done = self.ponggame.is_done()
        return obs, reward, done, {}

    def render(self, mode='human'):
        self.ponggame.view()

