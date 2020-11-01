import random
import copy

class environment:
    def __init__(self):
        self.i = 0
        self.env_map = [[0, -1, -1, 0, 0, 0], 
        [0, -1, 0, 0, -1, 0], 
        [0, -1, -1, 0, -1, 0], 
        [0, 0, -1, 0, -1, 0], 
        [-1, 0, -1, 0, -1, 0],
        [-1, 0, 0, 0, -1, 0]]
        self.start = [0,0]
        self.end = [5,5]
        self.action_space = [0, 1, 2, 3] # ['u', 'd', 'l', 'r']
        
        self.ROW = len(self.env_map)
        self.COL = len(self.env_map[0])
        self.env_map[self.end[0]][self.end[1]] = 5
        self.now = self.start
        self.n_actions = len(self.action_space)

    def reset(self):
        self.now = copy.copy(self.start)
        return self.start
    
    def check_next_step(self, action, t_now=1):
        if(t_now == 1):
            tp_now = copy.copy(self.now)
        else:
            tp_now = copy.copy(t_now)
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
            try:
                choice.remove(action)
            except:
                self.i = self.i+1
                print("*"*20,self.i)
            return self.check_next_step(random.choice(choice))
        else:
            return tp_now, action

    def step(self, action):
        # 赋值赋的是引用
        # 检测下一步位置是否合法
        next_state, action = self.check_next_step(action)
        self.now = copy.copy(next_state)
        n_next_state, n_action = self.check_next_step(action, t_now = next_state)

        reward = self.env_map[self.now[0]][self.now[1]]
        if(self.now == self.end):
            done = True
        else:
            done = False
        return n_next_state, next_state, reward, done, action#, n_action

    def check(self, state):
        if(state[0] < 0 or state[0] >= self.ROW):
            return False
        if(state[1] < 0 or state[1] >= self.COL):
            return False
        return True

    def check_get(self, state):
        n_n_state = []
        x = [1,1,1,0,0,-1,-1,-1]
        y = [-1,0,1,-1,1,-1,0,1]
        for i in range(8):
            new_state = [state[0]+x[i],state[1]+y[i]]
            if(self.check(new_state)):
                n_n_state.append(new_state)
        return n_n_state
    
if __name__ == "__main__":
    env = environment()
    print(env.step(1))
    print(env.now)