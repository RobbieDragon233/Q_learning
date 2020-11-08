# 问题1.不应该碰到错误就结束 fix
# 问题2.迭代是不是有问题，初始点的奖励惩罚始终为0 fix
# 问题3.前期突破太慢，寻路很久才能到
# 问题4.惩罚、奖励与学习率的关系，怎么才能迭代次数最少
# 问题5.怎么生成（0,1）的随机数 fix：生成两个随机数加和除二，总不能这么倒霉两个都等于0吧

import numpy as np
import copy
import random
from environment import environment
from collections import defaultdict
import time

class QLearningAgent:
    def __init__(self, actions):
        # actions = [0, 1, 2, 3]
        self.i = 0 #debug
        self.actions = actions
        self.learning_rate = 0.8 #0.4 #0.6
        self.discount_factor = 0.3 # (random.uniform(0, 1)+random.uniform(0, 1))/2 #0.38 #0.5
        self.epsilon = 0.1
        self.deep_learning_factor = 0.9
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
        # self.q_table = defaultdict(lambda: [-999.0, -999.0, -999.0, -999.0])
    

    def get_max_index(self, arr):
        def second_max(lt):
            d={}         #设定一个空字典
            for i, v in enumerate(lt):#利用函数enumerate列出lt的每个元素下标i和元素v
                d[v]=i   #把v作为字典的键，v对应的值是i
            lt.sort(reverse=True)    #运用sort函数对lt元素排
            y=lt[1]      #此时lt中第二小的下标是1，求出对应的元素就是字典对应的键
            print(d[y])
            return d[y]  #根据键找到对应值就是所找的下标
        def my_max(arr):
            # tmp_arr = sorted(arr, key=abs)
            tmp_arr = sorted(arr)
            return tmp_arr[0]
        lt = copy.copy(arr)
        try:
            while(1):
                del lt[lt.index(0)]
        except:
            pass
        return arr.index(max(arr))

    def get_path(self, agent):
        path = [[0,0]]
        row = path[0][0]
        col = path[0][1]
        # row和col是从0开始的，但是在append到path上面就都加了一
        while(row!=5 or col!=5):
            action = agent.get_max_index(agent.q_table[str([row, col])])
            agent.q_table[str([row, col])] = [0,0,0,0]
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
    def learn(self, state, action, reward, next_state, n_next_state):
        current_q = self.q_table[state][action]
        # 贝尔曼方程更新
        # new_q = reward + self.discount_factor * max(self.q_table[next_state])
        # self.q_table[state][action] += self.learning_rate * (new_q - current_q)
        # 改进新方法1对应：
        # n_n_score = -100
        # for index, n_n in enumerate(n_next_state):
        #     tmp = copy.copy(self.q_table[str(n_n)])
        #     tmp.append(n_n_score)
        #     n_n_score = max(tmp)
        # 改进方法2对应：
        # print("state:",state)
        # print("next_state:",next_state)
        # print("n_next_state:",n_next_state)
        n_n_score =  max(self.q_table[n_next_state])
        # print(n_next_state)
        new_q = reward + self.discount_factor * (self.deep_learning_factor \
            * max(self.q_table[next_state]) + \
                (1-self.deep_learning_factor)*n_n_score)
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)
        # 改进方法3对应：在n_next步的时候加入了方向的考虑
        


    # 从Q-table中选取动作
    def get_action(self, state, no_greedy = False):
        if(no_greedy):
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
            return action
        
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
    # f = open("output.txt","w")
    env = environment()
    agent = QLearningAgent(actions=list(range(env.n_actions)))
    for i in range(1):
        start = time.time()
        i = 0
        for episode in range(500):
            state = env.reset()
            while True:
                # env.render()
                # agent产生动作
                action = agent.get_action(str(state))
                tp, next_state, reward, done, true_action = env.step(action)
                
                # 更新Q表
                # 一种下两步的确定方法（存在不收敛的情况）
                # n_next_state = env.check_get(next_state)
                # n_next_state.remove(state)
                # 另一种下两步的确定方法:
                n_next_state = env.getFutureStep(agent.get_action(str(next_state), no_greedy = True))
                

                agent.learn(str(state), true_action, reward, str(next_state), str(n_next_state))
                state = next_state
                # print(state)
                # env.print_value_all(agent.q_table)
                # 当到达终点就终止游戏开始新一轮训练
                if done:
                    i += 1
                    # print(i)
                    break
        print("It can work here!")
        # print(agent.q_table)
        path = agent.get_path(agent)
        end = time.time()
        print("time:", end-start)
        print("now:", end)
        print("time:", end - start)
        print("learning_rate:%s; discount_factor:%s"%(agent.learning_rate,agent.discount_factor))
        print(path)

        # str1 = "time:" + str(end-start)+ "\n"
        # f.write(str1)
        # str2 = "learning_rate:" + str(agent.learning_rate) + "discount_factor:" + str(agent.discount_factor) + "\n"
        # f.write(str2)
        # f.write(str(path) + "\n")
