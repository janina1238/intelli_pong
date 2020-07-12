from gym.envs.registration import register

register(
    id='PyGamePong-v0',
    entry_point='gym_pong.envs:PygameEnv'
)