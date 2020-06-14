import gym
import numpy as np
from gym import spaces
from gym_pong.envs.pong_pygame import PongPygame


class PygameEnv(gym.Env):

    def __init__(self):
        self.ponggame = PongPygame()
        self.action_space = spaces.Discrete(3)  # three actions -> move up, move down, don't move
        self.observation_space = spaces.Box(low=np.array([-8., -8.]), high=np.array([8., 8.]), dtype=np.float64) # Box(2,)

    def reset(self):
        """
        Reset the game
        return:
            first observed data from the game
        """
        del self.ponggame
        self.ponggame = PongPygame()
        obs = self.ponggame.observe()
        return obs

    def step(self, action):
        """
        Apply the action.
        action:
            a choice how to move (up, down, don't move)
        return:
            the current state/ reward and if the episode is done
        """
        self.ponggame.action(action)
        obs = self.ponggame.observe()
        reward = self.ponggame.reward()
        done = self.ponggame.is_done()
        return obs, reward, done, {}

    def render(self, mode='human'):
        self.ponggame.view()
