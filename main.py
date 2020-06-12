import gym
import gym_pong

env = gym.make('PyGamePong-v0')
#intial_state = env.reset()

while True:
    env.render()
    action = env.action_space.sample()
    env.step(action)
    # obs, r, done, _ = env.step(action)

env.close()