import gym
import gym_pong
from stable_baselines.common.env_checker import check_env
from stable_baselines import A2C, DQN, PPO2
from stable_baselines.common.policies import MlpPolicy
# from stable_baselines.deepq.policies import MlpPolicy

env = gym.make('PyGamePong-v0')
check_env(env)

'''
model = A2C(MlpPolicy, env, verbose=1)  # instantiate the agent
model.learn(total_timesteps=25000)  # training
model.save("a2c_3")  # save the agent

model = A2C.load("a2c_3")  # load trained agent
'''

done = False
episode_reward = 0
total_reward = 0
obs = env.reset()

for t in range(25000):
    # action, _states = model.predict(obs)
    action = env.action_space.sample()
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
