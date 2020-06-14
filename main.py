import gym
import gym_pong

env = gym.make('PyGamePong-v0')
done = False
episode_reward = 0
total_reward = 0
initial_state = env.reset()

for t in range(10000):
    env.render()
    action = env.action_space.sample()
    obs, r, done, _ = env.step(action)
    episode_reward += r

    # if the episode is terminated reset the environment to initial state
    if done:
        total_reward += episode_reward
        print("episode ", episode_reward)
        initial_state = env.reset()

print("total_reward: ", total_reward)
env.close()
