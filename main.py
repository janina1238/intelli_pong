import gym
import gym_pong
from stable_baselines.common.env_checker import check_env
from stable_baselines import A2C, PPO2
from stable_baselines.common.policies import MlpPolicy

env = gym.make('PyGamePong-v0')

check_env(env)

"""
Training from the left paddle with the A2C Algorithm
"""
'''
model = A2C(MlpPolicy, env, verbose=1, n_steps=32, ent_coef=0.0, vf_coef=0.5)  # instantiate the agent
model.learn(total_timesteps=int(2e6))  # training
#model.save("ppo2_2e6_rightagent-vel20_randomballXY_20_nsteps2048.zip")
model.save("a2c_2e6_leftagent-vel20_randomballXY_20_nsteps32_ent_coef0_vf_coef05_enemymodel.zip")
'''
model_left = A2C.load("a2c_2e6_leftagent-vel20_randomballXY_20_nsteps32_ent_coef0_vf_coef05_enemymodel.zip")  # load trained agent

"""
Training from the right paddle with the PPO2 Algorithm
"""
'''
model = PPO2(MlpPolicy, env, verbose=1, n_steps=2048)  # instantiate the agent
model.learn(total_timesteps=int(2e6))  # training
model.save("ppo2_2e6_rightagent-vel20_randomballXY_20_nsteps2048.zip")  # save the agent
'''
model_right = PPO2.load("ppo2_2e6_rightagent-vel20_randomballXY_20_nsteps2048.zip")  # load trained agent

done = False
episode_reward = 0
episode_reward_enemy = 0
total_reward = 0
total_reward_enemy = 0

obs = env.reset()
obs_e = env.reset_enemy()

for t in range(25000):

    action, _states = model_left.predict(obs)
    # action = env.action_space.sample()

    action_e, _states_e = model_right.predict(obs_e)
    # action_e = env.action_space.sample()
    obs, r, done, _ = env.step(action)
    obs_e, r_e, done_e, _e = env.step_enemy(action_e)
    env.render()

    episode_reward += r
    episode_reward_enemy += r_e

    # if the episode is terminated reset the environment to initial state
    if done:

        total_reward += episode_reward
        total_reward_enemy += episode_reward_enemy

        print("episode_reward_paddle_a: ", episode_reward)
        print("episode_reward_paddle_b: ", episode_reward_enemy)

        episode_reward = 0
        episode_reward_enemy = 0

        obs = env.reset()
        obs_e = env.reset_enemy()

# total reward of all episodes
print("total_reward_paddle_left: ", total_reward)
print("total_reward_paddle_right: ", total_reward_enemy)
env.close()
