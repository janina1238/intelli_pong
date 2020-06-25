import gym
import gym_pong
import tensorflow
from stable_baselines.common.env_checker import check_env

env = gym.make('PyGamePong-v0')
check_env(env)

done = False
episode_reward = 0
total_reward = 0
initial_state = env.reset()

for t in range(10000):
    env.render()
    action = env.action_space.sample()
    obs_space = env.observation_space
    obs, r, done, _ = env.step(action)
    episode_reward += r

    # if the episode is terminated reset the environment to initial state
    if done:
        total_reward += episode_reward
        print("episode_reward: ", episode_reward)
        episode_reward = 0
        initial_state = env.reset()

# total reward of all episodes
print("total_reward: ", total_reward)
env.close()
