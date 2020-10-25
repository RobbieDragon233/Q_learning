# 同样数据的结果 时间0.6-1.2s
# learning_rate ['0.7230173205613866'] 
# discount_factor ['0.3719903014248088']

import re

a = []
path_correct = str([[1, 1], [2, 1], [3, 1], [4, 1], [4, 2], [5, 2], [6, 2], [6, 3], [6, 4], [5, 4], [4, 4], [3, 4], [2, 4], [1, 4], [1, 5], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6]])

f = open(r"F:\(1)Postgraduate\vsCode\freshMan\Project1\python\Q_learning\q\reinforcement_learning\Q-learning\nohup.txt")
fw = open(r"F:\(1)Postgraduate\vsCode\freshMan\Project1\python\Q_learning\q\reinforcement_learning\Q-learning\wrong.txt", "w")
fw_opt = open(r"F:\(1)Postgraduate\vsCode\freshMan\Project1\python\Q_learning\q\reinforcement_learning\Q-learning\opt.txt", "w")
pattern1 = re.compile(r"(?<=learning_rate:)\d+\.?\d*")
pattern2 = re.compile(r"(?<=discount_factor:)\d+\.?\d*")
line3 = f.readline()
while line3:
    tmp = []
    line1 = f.readline()
    cost_time = re.findall(r"\d+\.?\d*", line1)
    line2 = f.readline()
    learning_rate = pattern1.findall(line2)
    discount_factor = pattern2.findall(line2)
    line3 = f.readline()
    path = line3.replace("\n", "")
    tmp = [cost_time, learning_rate, discount_factor, path]
    if(path == path_correct):
        pass
    else:
        fw.write(line1)
        fw.write(line2)
        fw.write(line3)
    a.append(tmp)
f.close()
fw.close()

a.sort()
print(a[1])
print(a[-1])
# for i in range(10):
#     fw_opt.write(str(a[i]))

 
