import gym
import numpy as np
from gym import spaces
from gym_pong.envs.pong_pygame import PongPygame


class PygameEnv(gym.Env):

    def __init__(self):
        self.ponggame = PongPygame()
        self.action_space = spaces.Discrete(3)  # three actions -> move up, move down, don't move

        self.min_ball_pos_x = 0
        self.min_ball_pos_y = 55
        self.min_paddle_pos_x = 20  # 670 for the right paddle
        self.min_paddle_pos_y = 55

        self.max_ball_pos_x = 700
        self.max_ball_pos_y = 475
        self.max_paddle_pos_x = 20  # 670 for the right paddle
        self.max_paddle_pos_y = 400

        self.low_state = np.array(
            [self.min_ball_pos_x, self.min_ball_pos_y, self.min_paddle_pos_x, self.min_paddle_pos_y])
        self.high_state = np.array(
            [self.max_ball_pos_x, self.max_ball_pos_y, self.max_paddle_pos_x, self.max_paddle_pos_y])
        self.observation_space = spaces.Box(low=self.low_state, high=self.high_state, dtype=np.complex_)

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

    def reset_enemy(self):
        """
        Reset the game
        return:
            first observed data from the game
        """
        del self.ponggame
        self.ponggame = PongPygame()
        obs = self.ponggame.observe_enemy()
        return obs

    def step(self, action):
        """
        Apply the action.
        action:
            move up, move down, don't move
        return:
            the current state/ reward and if the episode is done
        """
        self.ponggame.action(action)
        obs = self.ponggame.observe()
        reward = self.ponggame.reward()
        done = self.ponggame.is_done()
        return obs, reward, done, {}

    def step_enemy(self, action):
        """
        Apply the action.
        action:
            move up, move down, don't move
        return:
            the current state/ reward and if the episode is done
        """
        self.ponggame.action_enemy(action)
        obs = self.ponggame.observe_enemy()
        reward = self.ponggame.reward_enemy()
        done = self.ponggame.is_done_enemy()
        return obs, reward, done, {}

    def render(self, mode='human'):
        self.ponggame.view()
