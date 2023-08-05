from pathlib import Path

import gym
import gym_d2d
# from gym_d2d.envs.path_loss import FooPathLoss

env_config = {
    'num_rbs': 5,
    'num_cellular_users': 5,
    'num_d2d_pairs': 3,
    'due_max_tx_power_dBm': 2,
    # 'path_loss_model': FooPathLoss,
    'device_config_file': Path.cwd() / 'device_config.json',
}
env = gym.make('D2DEnv-v0', env_config=env_config)

agent = 'D2DAgent()'
obs_dict = env.reset()
game_over = False
for _ in range(100):
    actions_dict = {}
    for agent_id, obs in obs_dict.items():
        action = env.action_space.sample()
        actions_dict[agent_id] = action

    obs_dict, rewards_dict, game_over, info = env.step(actions_dict)
    print(obs_dict)
