import gym
from gym import spaces
from gym_pong.envs.pong_pygame import PongPygame


class PygameEnv(gym.Env):

    def __init__(self):
        self.ponggame = PongPygame()
        self.action_space = spaces.Discrete(3)

    # reset the game
    def reset(self):
        del self.ponggame
        self.ponggame = PongPygame()
        obs = self.ponggame.observe()
        # return first observed data from the game
        return obs

    def step(self, action):
        self.ponggame.action(action)  # perform action
        obs = self.ponggame.observe()  # calculate state
        reward = self.ponggame.reward()  # calculate reward
        done = self.ponggame.is_done()
        return obs, reward, done, {}

    def render(self, mode='human'):
        self.ponggame.view()

