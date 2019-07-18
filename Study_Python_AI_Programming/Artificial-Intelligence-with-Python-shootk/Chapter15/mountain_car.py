import gym
import numpy as np
from gym import wrappers
import matplotlib.pyplot as plt
from time import sleep


def get_status(_observation):
    env_low = env.observation_space.low  # 位置と速度の最小値
    env_high = env.observation_space.high  # 　位置と速度の最大値
    env_dx = (env_high - env_low) / 40  # 40等分
    # 0〜39の離散値に変換する
    position = int((_observation[0] - env_low[0]) / env_dx[0])
    velocity = int((_observation[1] - env_low[1]) / env_dx[1])
    return position, velocity


def update_q_table(_q_table, _action, _observation, _next_observation, _reward, _episode):

    alpha = 0.1  # 学習率
    gamma = 0.9  # 時間割引き率

    next_position, next_velocity = get_status(_next_observation)
    next_max_q_value = max(_q_table[next_position][next_velocity])

    position, velocity = get_status(_observation)
    q_value = _q_table[position][velocity][_action]

    _q_table[position][velocity][_action] = q_value + \
        alpha * (_reward + gamma * next_max_q_value - q_value)

    return _q_table


def get_action(_env, _q_table, _observation, _episode):
    epsilon = 0.01
    np.random.seed(10)
    if np.random.uniform(0, 1) > epsilon:
        position, velocity = get_status(observation)
        _action = np.argmax(_q_table[position][velocity])
    else:
        _action = np.random.choice([0, 1, 2])
    return _action


def get_demo_action(_env, _q_table, _observation, _episode):
    position, velocity = get_status(observation)
    return np.argmax(_q_table[position][velocity])


if __name__ == '__main__':

    env = gym.make('MountainCar-v0')
    env.reset()

    q_table = np.zeros((40, 40, 3))

    rewards = []
    for episode in range(10000):
        total_reward = 0
        observation = env.reset()

        for _ in range(200):

            # ε-グリーディ法で行動を選択
            action = get_action(env, q_table, observation, episode)

            next_observation, reward, done, _ = env.step(action)

            # Qテーブルの更新
            q_table = update_q_table(
                q_table, action, observation, next_observation, reward, episode)
            total_reward += reward

            observation = next_observation

            if done:
                # doneがTrueになったら１エピソード終了
                if episode % 100 == 0:
                    print('episode: {}, total_reward: {}'.format(
                        episode, total_reward))
                rewards.append(total_reward)
                break
    print(rewards.index(max(rewards)), max(rewards))
    env_demo = env
    observation = env.reset()
    env.render()
    sleep(10)
    for _ in range(200):
        next_observation, reward, done, _ = env_demo.step(action)
        observation = next_observation
        action = get_demo_action(env_demo, q_table, observation, episode)
        env.step(action)
        env.render()
        if done:
            break
    env.close()
    env_demo.close()

    plt.figure()
    plt.xlabel("Episode")
    plt.ylabel("TotalReward")
    plt.grid(True)
    plt.plot(rewards)
    plt.show()
