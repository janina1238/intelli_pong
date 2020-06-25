import gym
import gym_pong
import tensorflow
from stable_baselines.common.env_checker import check_env
from stable_baselines import DQN
from stable_baselines.deepq.policies import MlpPolicy

env = gym.make('PyGamePong-v0')
check_env(env)

model = DQN(MlpPolicy, env, verbose=1)  # instantiate the agent
model.learn(total_timesteps=40000)  # training
model.save("deepq_pong")  # save the agent
del model  # remove to demonstrate saving and loading
model = DQN.load("deepq_pong")  # load trained agent

done = False
episode_reward = 0
total_reward = 0
obs = env.reset()

for t in range(25000):
    action, _states = model.predict(obs)
    # action = env.action_space.sample()
    obs, r, done, _ = env.step(action)
    env.render()

    episode_reward += r

    # if the episode is terminated reset the environment to initial state
    if done:
        total_reward += episode_reward
        print("episode_reward: ", episode_reward)
        episode_reward = 0
        obs = env.reset()

# total reward of all episodes
print("total_reward: ", total_reward)
env.close()
