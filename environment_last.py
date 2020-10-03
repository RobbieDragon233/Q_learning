import time
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image, ImageGrab

np.random.seed(1)
PhotoImage = ImageTk.PhotoImage
UNIT = 100
HEIGHT = 5
WIDTH = 5


class Env(tk.Tk):
    def __init__(self):
        super(Env, self).__init__()
        self.start = [0,0]
        self.end = [5,5]
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('Q Learning')
        self.geometry('{0}x{1}'.format(HEIGHT * UNIT, HEIGHT * UNIT))
        self.shapes = self.load_images()
        self.canvas = self._build_canvas()
        self.texts = []

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height=HEIGHT * UNIT,
                           width=WIDTH * UNIT)
        # create grids
        for c in range(0, WIDTH * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = c, 0, c, HEIGHT * UNIT
            canvas.create_line(x0, y0, x1, y1)
        for r in range(0, HEIGHT * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = 0, r, HEIGHT * UNIT, r
            canvas.create_line(x0, y0, x1, y1)

        # add img to canvas
        self.soldier = canvas.create_image(50, 50, image=self.shapes[0])
        self.mountain1 = canvas.create_image(250, 50, image=self.shapes[1])
        self.mountain2 = canvas.create_image(350, 50, image=self.shapes[1])
        self.mountain3 = canvas.create_image(250, 150, image=self.shapes[1])
        self.mountain4 = canvas.create_image(350, 150, image=self.shapes[1])
        self.mountain5 = canvas.create_image(250, 250, image=self.shapes[1])
        self.mountain6 = canvas.create_image(50, 350, image=self.shapes[1])
        self.mountain7 = canvas.create_image(150, 350, image=self.shapes[1])
        self.mountain8 = canvas.create_image(250, 350, image=self.shapes[1])
        self.mountain9 = canvas.create_image(350, 350, image=self.shapes[1])
        self.mountain10 = canvas.create_image(50, 450, image=self.shapes[1])
        self.mountain11 = canvas.create_image(150, 450, image=self.shapes[1])
        self.mountain12 = canvas.create_image(250, 450, image=self.shapes[1])
        self.mountain13 = canvas.create_image(350, 450, image=self.shapes[1])
        
        self.reward = canvas.create_image(450, 50, image=self.shapes[3])
        
        
        
        
        self.city = canvas.create_image(self.end[0]*UNIT-UNIT/2, self.end[1]*UNIT-UNIT/2, image=self.shapes[2])

        # pack all
        canvas.pack()

        return canvas

    def load_images(self):
        soldier = PhotoImage(
            Image.open(r"F:\(1)Postgraduate\vsCode\freshMan\Project1\python\Q_learning\q\reinforcement_learning\img\soldier.jpg").resize((65, 65)))
        mountain = PhotoImage(
            Image.open(r"F:\(1)Postgraduate\vsCode\freshMan\Project1\python\Q_learning\q\reinforcement_learning\img\mountain.jpg").resize((65, 65)))
        reward = PhotoImage(
            Image.open(r"F:\(1)Postgraduate\vsCode\freshMan\Project1\python\Q_learning\q\reinforcement_learning\img\commander.jpg").resize((65, 65)))
        circle = PhotoImage(
            Image.open(r"F:\(1)Postgraduate\vsCode\freshMan\Project1\python\Q_learning\q\reinforcement_learning\img\city.jpg").resize((65, 65)))
        
        return soldier, mountain, reward

    def text_value(self, row, col, contents, action, font='Helvetica', size=10,
                   style='normal', anchor="nw"):
        if action == 0:
            origin_x, origin_y = 7, 42
        elif action == 1:
            origin_x, origin_y = 85, 42
        elif action == 2:
            origin_x, origin_y = 42, 5
        else:
            origin_x, origin_y = 42, 77

        x, y = origin_y + (UNIT * col), origin_x + (UNIT * row)
        font = (font, str(size), style)
        text = self.canvas.create_text(x, y, fill="black", text=contents,
                                       font=font, anchor=anchor)
        return self.texts.append(text)

    def print_value_all(self, q_table):
        for i in self.texts:
            self.canvas.delete(i)
        self.texts.clear()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                for action in range(0, 4):
                    state = [i, j]
                    if str(state) in q_table.keys():
                        temp = q_table[str(state)][action]
                        self.text_value(j, i, round(temp, 2), action)

    def coords_to_state(self, coords):
        x = int((coords[0] - 50) / 100)
        y = int((coords[1] - 50) / 100)
        return [x, y]

    def state_to_coords(self, state):
        x = int(state[0] * 100 + 50)
        y = int(state[1] * 100 + 50)
        return [x, y]

    def reset(self):
        self.update()
        time.sleep(0.005)
        x, y = self.canvas.coords(self.rectangle)
        self.canvas.move(self.rectangle, UNIT / 2 - x, UNIT / 2 - y)
        self.render()
        # return observation
        return self.coords_to_state(self.canvas.coords(self.rectangle))

    def step(self, action):
        
        return next_state, reward, done

    # 渲染环境
    def render(self):
        time.sleep(0.0003)
        self.update()
