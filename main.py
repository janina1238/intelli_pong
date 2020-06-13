import gym
import gym_pong


env = gym.make('PyGamePong-v0')
# intial_state = env.reset()
total_reward = 0
state = env.reset()

for t in range(5000):
    env.render()
    action = env.action_space.sample()
    obs, r, done, _ = env.step(action)
    total_reward += r
    # print(episode_reward)

    if done:
        print(total_reward)
        state = env.reset()

env.close()
