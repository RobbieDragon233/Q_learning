# 问题1.不应该碰到错误就结束 fix
# 问题2.迭代是不是有问题，初始点的奖励惩罚始终为0 fix
# 问题3.前期突破太慢，寻路很久才能到
# 问题4.惩罚、奖励与学习率的关系，怎么才能迭代次数最少
# 问题5.怎么生成（0,1）的随机数 fix：生成两个随机数加和除二，总不能这么倒霉两个都等于0吧

import numpy as np
import random
from environment import environment
from collections import defaultdict
import time

class QLearningAgent:
    def __init__(self, actions):
        # actions = [0, 1, 2, 3]
        self.actions = actions
        self.learning_rate = (random.uniform(0, 1)+random.uniform(0, 1))/2
        self.discount_factor = (random.uniform(0, 1)+random.uniform(0, 1))/2
        self.epsilon = 0.1
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    
    def get_max_index(self, arr):
        return arr.index(max(arr))

    def get_path(self, agent):
        path = [[0,0]]
        row = path[0][0]
        col = path[0][1]
        # row和col是从0开始的，但是在append到path上面就都加了一
        while(row!=5 or col!=5):
            action = agent.get_max_index(agent.q_table[str([row, col])])
            if action == 0:
                row = row - 1
            elif action == 1:
                row = row + 1
            elif action == 2:
                col = col - 1
            else:
                col = col + 1
            path.append([row+1, col+1])
            # 为什么这个print在里面就会出错？？？debug没问题，运行就有问题
            # print(path)
        path[0]=[1,1]
        return path

        # q_table.index(max(q_table(path[i])) # action
        

    # 采样 <s, a, r, s'>
    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        # 贝尔曼方程更新
        new_q = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)

    # 从Q-table中选取动作
    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # 贪婪策略随机探索动作
            action = np.random.choice(self.actions)
        else:
            # 从q表中选择
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
        return action

    @staticmethod
    def arg_max(state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)


if __name__ == "__main__":
    env = environment()
    agent = QLearningAgent(actions=list(range(env.n_actions)))
    for i in range(100000):
        start = time.time()
        for episode in range(5000):
            state = env.reset()
            while True:
                # env.render()
                # agent产生动作
                action = agent.get_action(str(state))
                next_state, reward, done, true_action = env.step(action)
                # 更新Q表
                agent.learn(str(state), true_action, reward, str(next_state))
                state = next_state
                # print(state)
                # env.print_value_all(agent.q_table)
                # 当到达终点就终止游戏开始新一轮训练
                if done:
                    break
        path = agent.get_path(agent)
        end = time.time()
        print("time:", end - start)
        print("learning_rate:%s; discount_factor:%s"%(agent.learning_rate,agent.discount_factor))
        print(path)
