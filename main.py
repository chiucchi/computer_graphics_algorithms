# Import the required libraries
from tkinter import *


class Paint:

    def __init__(self):
        # Variables
        self.click_num = 0
        self.xc = 0
        self.yc = 0
        self.x = 0
        self.y = 0
        self.list = []
        self.new_x1 = 0
        self.new_x2 = 0
        self.new_y1 = 0
        self.new_y2 = 0

        # Window instance
        win = Tk()
        win.title("Paint 2.0")
        win.resizable(width=False, height=False)
        win.geometry("850x800")

        # Canvas settings
        self.canvas = Canvas(win, width=850, height=800, background="white")
        self.canvas.grid(row=3, columnspan=10)
        self.canvas.configure(scrollregion=(-400, -400, 400, 400))

        frame = Frame(win)

        global click_num
        click_num = 0
        """  Buttons and Inputs """
        # Rasterization (lines and circunferences)
        Label(win, text="Retas").grid(row=0, column=0)
        Button(win, text="DDA",
               command=self.draw_dda_line_selected).grid(row=0, column=1)

        Button(win, text="Bresenham",
               command=self.draw_brese_line_selected).grid(row=0, column=2)

        Button(win, text="Circunferência",
               command=self.draw_circ_selected).grid(row=0, column=3)
        Label(win, text="Digite o raio:").grid(row=0, column=4)
        self.raio = StringVar()
        Entry(win, textvariable=self.raio).grid(row=0, column=5)
        # Geommetric transformations
        Label(win, text="Transformações").grid(row=1, column=0)
        Button(win, text="Translação", command=self.translation).grid(row=1,
                                                                      column=2)
        self.x1 = StringVar()
        Entry(win, textvariable=self.x1, width=5).grid(row=1, column=3)
        self.y1 = StringVar()
        Entry(win, textvariable=self.y1, width=5).grid(row=1, column=4)

        Button(win, text="Rotação", command=self.draw_dda_line).grid(row=1,
                                                                     column=5)

        Button(win, text="Escala", command=self.scale).grid(row=1, column=6)

        Button(win, text="Reflexão X",
               command=self.reflection_x).grid(row=2, column=2)
        Button(win, text="Reflexão Y",
               command=self.reflection_y).grid(row=2, column=3)
        Button(win, text="Reflexão XY",
               command=self.reflection_xy).grid(row=2, column=4)

        # Clear canvas
        clear_button = Button(win, text="Limpar", command=self.clear_canvas)
        clear_button.grid(row=2, column=0)

        win.mainloop()

    def clear_canvas(self):
        self.list = []
        self.canvas.delete(ALL)

    # Draw lines
    def draw_dda_line_selected(self):
        self.canvas.bind("<Button-1>", self.draw_dda_line)

    def draw_dda_line(self, event, transform=False):
        global x1, y1, x2, y2

        if not transform:
            if self.click_num == 0:  # primeiro clique
                x1 = event.x - 400
                y1 = event.y - 400
                self.click_num = 1
                self.draw_dda_line()
            elif self.click_num == 1:  # segundo clique
                x2 = event.x - 400
                y2 = event.y - 400
                self.click_num = 0
        if transform:
            x1 = self.new_x1
            x2 = self.new_x2
            y1 = self.new_y1
            y2 = self.new_y2

        self.list = [x1, x2, y1, y2, "dda_line"]

        passos = 0
        x_incr = 0
        y_incr = 0
        dx = x2 - x1
        dy = y2 - y1

        if (abs(dx) > abs(dy)):
            passos = abs(dx)
        else:
            passos = abs(dy)

        x_incr = dx / passos
        y_incr = dy / passos
        x = x1
        y = y1
        self.canvas.create_oval(round(x),
                                round(y),
                                round(x) + 1,
                                round(y) + 1,
                                fill="black",
                                width=2)  # desenha o ponto

        for i in range(passos):
            x = x + x_incr
            y = y + y_incr

            self.canvas.create_oval(round(x),
                                    round(y),
                                    round(x) + 1,
                                    round(y) + 1,
                                    fill="black",
                                    width=2)  # desenha o ponto
        print(x1, x2, y1, y2)
        x1 = None
        x2 = None
        y1 = None
        y2 = None

        self.canvas.unbind("<Button-1>")

    def draw_brese_line_selected(self):
        self.canvas.bind("<Button-1>", self.draw_brese_line)

    def draw_brese_line(self, event, transform=False):
        global x1, y1, x2, y2

        if not transform:
            if self.click_num == 0:  # primeiro clique
                x1 = event.x - 400
                y1 = event.y - 400
                self.click_num = 1
                self.draw_brese_line()
            else:  # segundo clique
                x2 = event.x - 400
                y2 = event.y - 400
                self.click_num = 0
        if transform:
            x1 = self.new_x1
            x2 = self.new_x2
            y1 = self.new_y1
            y2 = self.new_y2

        self.list = [x1, x2, y1, y2, "brese_line"]

        dx = x2 - x1
        dy = y2 - y1
        x_incr = 0
        y_incr = 0

        if dx >= 0:
            x_incr = 1
        else:
            x_incr = -1
            dx = -dx
        if dy >= 0:
            y_incr = 1
        else:
            y_incr = -1
            dy = -dy

        x = x1
        y = y1

        self.canvas.create_oval(round(x),
                                round(y),
                                round(x) + 1,
                                round(y) + 1,
                                fill="black",
                                width=2)  # desenha o ponto

        p = 0
        const1 = 0
        const2 = 0

        if dy < dx:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)

            for i in range(dx):
                x = x + x_incr
                if (p < 0):
                    p = p + const1
                else:
                    y = y + y_incr
                    p = p + const2

                self.canvas.create_oval(round(x),
                                        round(y),
                                        round(x) + 1,
                                        round(y) + 1,
                                        fill="black",
                                        width=2)  # desenha o ponto
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            for k in range(dy):
                y = y + y_incr
                if (p < 0):
                    p = p + const1
                else:
                    x = x + x_incr
                    p = p + const2
                self.canvas.create_oval(round(x),
                                        round(y),
                                        round(x) + 1,
                                        round(y) + 1,
                                        fill="black",
                                        width=2)  # desenha o ponto

        # zerando tudo
        x1 = None
        x2 = None
        y1 = None
        y2 = None

        self.canvas.unbind("<Button-1>")

    # Draw circunference
    def draw_circ_selected(self):
        self.canvas.bind("<Button-1>", self.draw_circ)

    def plot_circle_points(self):
        self.canvas.create_oval(self.xc + self.x,
                                self.yc + self.y, (self.xc + self.x) + 1,
                                (self.yc + self.y) + 1,
                                fill="black",
                                width=2)
        self.canvas.create_oval(self.xc - self.x,
                                self.yc + self.y, (self.xc - self.x) + 1,
                                (self.yc + self.y) + 1,
                                fill="black",
                                width=2)
        self.canvas.create_oval(self.xc + self.x,
                                self.yc - self.y, (self.xc + self.x) + 1,
                                (self.yc - self.y) + 1,
                                fill="black",
                                width=2)
        self.canvas.create_oval(self.xc - self.x,
                                self.yc - self.y, (self.xc - self.x) + 1,
                                (self.yc - self.y) + 1,
                                fill="black",
                                width=2)
        self.canvas.create_oval(self.xc + self.y,
                                self.yc + self.x, (self.xc + self.y) + 1,
                                (self.yc + self.x) + 1,
                                fill="black",
                                width=2)
        self.canvas.create_oval(self.xc - self.y,
                                self.yc + self.x, (self.xc - self.y) + 1,
                                (self.yc + self.x) + 1,
                                fill="black",
                                width=2)
        self.canvas.create_oval(self.xc + self.y,
                                self.yc - self.x, (self.xc + self.y) + 1,
                                (self.yc - self.x) + 1,
                                fill="black",
                                width=2)
        self.canvas.create_oval(self.xc - self.y,
                                self.yc - self.x, (self.xc - self.y) + 1,
                                (self.yc - self.x) + 1,
                                fill="black",
                                width=2)

    def draw_circ(self, event, transform=False):
        raio = int(self.raio.get())
        if not transform:
            self.xc = event.x - 400
            self.yc = event.y - 400
            self.x = 0
            self.y = raio
        if transform:
            self.x = 0
            self.y = raio
            self.xc = self.new_x1
            self.yc = self.new_y1

        # save positions for further transformations
        self.list = [self.xc, self.yc, self.x, self.y, "circle"]

        p = 3 - 2 * raio

        self.plot_circle_points()

        while self.x < self.y:
            if p < 0:
                p = p + 4 * self.x + 6
            else:
                p = p + 4 * (self.x - self.y) + 10
                self.y = self.y - 1
            self.x = self.x + 1
            self.plot_circle_points()

        self.canvas.unbind("<Button-1>")

    # Transformations
    def translation(self):
        tx = int(self.x1.get())
        ty = int(self.y1.get())

        self.new_x1 = self.list[0] + tx
        self.new_x2 = self.list[1] + tx
        self.new_y1 = self.list[2] + ty
        self.new_y2 = self.list[3] + ty

        if self.list[4] == "dda_line":
            self.draw_dda_line(self, transform=True)
        elif self.list[4] == "circle":
            self.draw_circ(self, transform=True)
        elif self.list[4] == "brese_line":
            self.draw_brese_line(self, transform=True)

    def scale(self):
        tx = int(self.x1.get())
        ty = int(self.y1.get())

        self.new_x1 = self.list[0] * tx
        self.new_x2 = self.list[1] * tx
        self.new_y1 = self.list[2] * ty
        self.new_y2 = self.list[3] * ty

        if self.list[4] == "dda_line":
            self.draw_dda_line(self, transform=True)
        elif self.list[4] == "circle":
            self.draw_circ(self, transform=True)
        elif self.list[4] == "brese_line":
            self.draw_brese_line(self, transform=True)

    def reflection_x(self):
        self.new_x1 = self.list[0] * 1
        self.new_x2 = self.list[1] * 1
        self.new_y1 = self.list[2] * -1
        self.new_y2 = self.list[3] * -1

        if self.list[4] == "dda_line":
            self.draw_dda_line(self, transform=True)
        elif self.list[4] == "circle":
            self.draw_circ(self, transform=True)
        elif self.list[4] == "brese_line":
            self.draw_brese_line(self, transform=True)

    def reflection_y(self):
        self.new_x1 = self.list[0] * -1
        self.new_x2 = self.list[1] * -1
        self.new_y1 = self.list[2] * 1
        self.new_y2 = self.list[3] * 1

        if self.list[4] == "dda_line":
            self.draw_dda_line(self, transform=True)
        elif self.list[4] == "circle":
            self.draw_circ(self, transform=True)
        elif self.list[4] == "brese_line":
            self.draw_brese_line(self, transform=True)

    def reflection_xy(self):
        self.new_x1 = self.list[0] * -1
        self.new_x2 = self.list[1] * -1
        self.new_y1 = self.list[2] * -1
        self.new_y2 = self.list[3] * -1

        if self.list[4] == "dda_line":
            self.draw_dda_line(self, transform=True)
        elif self.list[4] == "circle":
            self.draw_circ(self, transform=True)
        elif self.list[4] == "brese_line":
            self.draw_brese_line(self, transform=True)


paint_app = Paint()
