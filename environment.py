import random
import copy

class environment:
    def __init__(self):
        self.env_map = [[0, -1, -1, 0, 0, 0], 
        [0, -1, 0, 0, -1, 0], 
        [0, -1, -1, 0, -1, 0], 
        [0, 0, -1, 0, -1, 0], 
        [-1, 0, -1, 0, -1, 0],
        [-1, 0, 0, 0, -10, 0]]
        self.start = [0,0]
        self.end = [5,5]
        self.action_space = [0, 1, 2, 3] # ['u', 'd', 'l', 'r']
        
        self.ROW = len(self.env_map)
        self.COL = len(self.env_map[0])
        self.env_map[self.end[0]][self.end[1]] = 1
        self.now = self.start
        self.n_actions = len(self.action_space)

    def reset(self):
        self.now = copy.copy(self.start)
        return self.start
    
    def step(self, action):
        # 赋值赋的是引用
        tp_now = copy.copy(self.now)
        if action == 0:  # up
            if tp_now[0] > 0:
                tp_now[0] -= 1
        elif action == 1:  # down
            if tp_now[0] < self.ROW-1:
                tp_now[0] = tp_now[0] + 1
        elif action == 2:  # left
            if tp_now[1] > 0:
                tp_now[1] -= 1
        elif action == 3:  # right
            if tp_now[1] < self.COL - 1:
                tp_now[1] += 1
        if(tp_now == self.now):
            choice = copy.copy(self.action_space)
            choice.remove(action)
            return self.step(random.choice(choice))
        else:
            self.now = tp_now
            next_state = self.now
            reward = self.env_map[self.now[0]][self.now[1]]
            if(self.now == self.end):
                done = True
            else:
                done = False
        return next_state, reward, done, action

# if __name__ == "__main__":
#     env = environment()
#     for i in range(15):
#         print(i)
#         next_state, reward, done = env.step(1)
#         print(next_state, reward)
        