import gym
import gym_pong

env = gym.make('PyGamePong-v0')
#intial_state = env.reset()
episode_reward = 0

while True:
    env.render()
    action = env.action_space.sample()
    # env.step(action)
    # obs, r, done, _ = env.step(action)
    r = env.step(action)
    episode_reward += r
    print(episode_reward)

env.close()