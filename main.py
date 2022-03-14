# Import the required libraries
from tkinter import *
from math import sin, cos, radians


class Paint:

    def __init__(self):
        # Global variables
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
        self.ratio = 0
        self.u1 = 0
        self.u2 = 0
        global click_num
        click_num = 0

        # Window instance
        win = Tk()
        win.title("Paint 2.0")
        win.resizable(width=False, height=False)
        win.geometry("850x800")

        # Canvas settings
        self.canvas = Canvas(win, width=850, height=800, background="white")
        self.canvas.grid(row=4, columnspan=10)
        self.canvas.configure(scrollregion=(-400, -400, 400, 400))

        frame = Frame(win)
        """ ### Buttons and Inputs ### """
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
        Entry(win, textvariable=self.raio, width=5).grid(row=0, column=5)

        # Geommetric transformations
        Label(win, text="Transformações").grid(row=1, column=0)
        Button(win, text="Translação", command=self.translation).grid(row=1,
                                                                      column=2)
        self.x1 = StringVar()
        Entry(win, textvariable=self.x1, width=5).grid(row=1, column=4)
        self.y1 = StringVar()
        Entry(win, textvariable=self.y1, width=5).grid(row=1, column=5)

        Button(win, text="Rotação", command=self.rotation).grid(row=1,
                                                                column=6)
        self.angle = StringVar()
        Entry(win, textvariable=self.angle, width=5).grid(row=1, column=7)

        Button(win, text="Escala", command=self.scale).grid(row=1, column=3)

        Button(win, text="Reflexão X",
               command=self.reflection_x).grid(row=2, column=2)
        Button(win, text="Reflexão Y",
               command=self.reflection_y).grid(row=2, column=3)
        Button(win, text="Reflexão XY",
               command=self.reflection_xy).grid(row=2, column=4)

        # Clipping functions
        Button(win, text="Cohen Clip",
               command=self.cohen_sutherland).grid(row=2, column=5)
        Button(win, text="Liang-Barsky",
               command=self.liang_barsky).grid(row=2, column=6)

        # Clipping window values
        Label(win, text="Xjmax:").grid(row=3, column=0)
        self.x_max = StringVar()
        Entry(win, textvariable=self.x_max, width=5).grid(row=3, column=1)
        Label(win, text="Yjmax:").grid(row=3, column=2)
        self.y_max = StringVar()
        Entry(win, textvariable=self.y_max, width=5).grid(row=3, column=3)
        Label(win, text="Xjmin:").grid(row=3, column=4)
        self.x_min = StringVar()
        Entry(win, textvariable=self.x_min, width=5).grid(row=3, column=5)
        Label(win, text="Yjmin:").grid(row=3, column=6)
        self.y_min = StringVar()
        Entry(win, textvariable=self.y_min, width=5).grid(row=3, column=7)

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
            if self.click_num == 0:  # detect first click
                x1 = event.x - 400
                y1 = event.y - 400
                self.click_num = 1
                self.draw_dda_line()
            elif self.click_num == 1:  # detect second click
                x2 = event.x - 400
                y2 = event.y - 400
                self.click_num = 0
        if transform:  # if dda function is called by a transformation function,
            x1 = self.new_x1  # use the new values instead of listen to clicks
            x2 = self.new_x2
            y1 = self.new_y1
            y2 = self.new_y2

        self.list = [x1, x2, y1, y2,
                     "dda_line"]  # save values for further transformations

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
                                width=2)  # draw point
        for i in range(passos):
            x = x + x_incr
            y = y + y_incr

            self.canvas.create_oval(round(x),
                                    round(y),
                                    round(x) + 1,
                                    round(y) + 1,
                                    fill="black",
                                    width=2)  # draw point
        # reset values for the next rasterization
        x1 = None
        x2 = None
        y1 = None
        y2 = None

        self.canvas.unbind(
            "<Button-1>"
        )  # detach click listener, you can only draw one line at a time

    def draw_brese_line_selected(self):
        self.canvas.bind("<Button-1>", self.draw_brese_line)

    def draw_brese_line(self, event, transform=False):
        global x1, y1, x2, y2

        if not transform:
            if self.click_num == 0:  # detect first click
                x1 = event.x - 400
                y1 = event.y - 400
                self.click_num = 1
                self.draw_brese_line()
            else:  # detect second click
                x2 = event.x - 400
                y2 = event.y - 400
                self.click_num = 0
        if transform:  # if bresenham function is called by a transformation function,
            x1 = self.new_x1  # it will use the new values instead of listen to clicks
            x2 = self.new_x2
            y1 = self.new_y1
            y2 = self.new_y2

        self.list = [x1, x2, y1, y2,
                     "brese_line"]  # save values for further transformations

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
                                width=2)  # draw point

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
                                        width=2)  # draw point
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
                                        width=2)  # draw point

        # reset values for the next rasterization
        x1 = None
        x2 = None
        y1 = None
        y2 = None

        self.canvas.unbind(
            "<Button-1>"
        )  # detach click listener, you can only draw one line at a time

    # Draw circunference
    def draw_circ_selected(self):
        self.canvas.bind("<Button-1>", self.draw_circ)

    # plot points function
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
            self.ratio = raio
            self.xc = event.x - 400
            self.yc = event.y - 400
            self.x = 0
            self.y = raio
        if transform:  # if circunference function is called by a transformation function,
            self.x = 0  # it will use the new values instead of listen to clicks
            self.y = self.ratio
            self.xc = self.new_x1
            self.yc = self.new_y1
            raio = self.ratio

        # save positions for further transformations
        self.list = [self.xc, self.x, self.yc, self.y, "circle"]

        p = 3 - (2 * raio)

        self.plot_circle_points()

        while self.x < self.y:
            if p < 0:
                p = p + 4 * self.x + 6
            else:
                p = p + 4 * (self.x - self.y) + 10
                self.y = self.y - 1
            self.x = self.x + 1
            self.plot_circle_points()

        self.canvas.unbind("<Button-1>")  # detach click listener

    """ Transformations """

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
            self.ratio = self.ratio * tx  # change ratio value for the new one
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

    def rotation(self):
        angle = int(self.angle.get())
        ratio = radians(angle)

        self.new_x1 = 0
        self.new_y1 = 0
        self.new_x2 = self.new_x2 - self.list[0]
        self.new_y2 = self.new_y2 - self.list[2]

        self.new_x2 = int((self.list[1] * cos(ratio)) -
                          (self.list[3] * sin(ratio)))
        self.new_y2 = int((self.list[1] * sin(ratio)) +
                          (self.list[3] * cos(ratio)))
        self.new_x1 = self.list[0]
        self.new_y1 = self.list[2]
        self.new_x2 = self.new_x2 + self.list[0]
        self.new_y2 = self.new_y2 + self.list[2]

        if self.list[4] == "dda_line":
            self.draw_dda_line(self, transform=True)
        elif self.list[4] == "circle":
            self.draw_circ(self, transform=True)
        elif self.list[4] == "brese_line":
            self.draw_brese_line(self, transform=True)

    def compute_code(self, x, y, x_max, y_max, x_min, y_min):
        code = 0
        if x < x_min:  # to the left of window
            code |= 1
        elif x > x_max:  # to the right of window
            code |= 2
        if y < y_min:  # below the window
            code |= 4
        elif y > y_max:  # above the window
            code |= 8

        return code

    def cohen_sutherland(self):
        # get input values
        x_max = int(self.x_max.get())
        y_max = int(self.y_max.get())
        x_min = int(self.x_min.get())
        y_min = int(self.y_min.get())

        # retrieve line initial and final points
        x1 = self.list[0]
        x2 = self.list[1]
        y1 = self.list[2]
        y2 = self.list[3]

        code1 = self.compute_code(x1, y1, x_max, y_max, x_min, y_min)
        code2 = self.compute_code(x2, y2, x_max, y_max, x_min, y_min)
        accept = False

        while True:
            if code1 == 0 and code2 == 0:
                accept = True
                break
            elif (code1 & code2) != 0:
                break
            else:
                x = 1.0
                y = 1.0
                if code1 != 0:
                    code_out = code1
                else:
                    code_out = code2
                if code_out & 8:
                    x = x1 + (x2 - x1) * \
                                    (y_max - y1) / (y2 - y1)
                    y = y_max
                elif code_out & 4:
                    x = x1 + (x2 - x1) * \
                                    (y_min - y1) / (y2 - y1)
                    y = y_min
                elif code_out & 2:
                    y = y1 + (y2 - y1) * \
                                    (x_max - x1) / (x2 - x1)
                    x = x_max
                elif code_out & 1:
                    y = y1 + (y2 - y1) * \
                                    (x_min - x1) / (x2 - x1)
                    x = x_min
                if code_out == code1:
                    x1 = x
                    y1 = y
                    code1 = self.compute_code(x1, y1, x_max, y_max, x_min,
                                              y_min)

                else:
                    x2 = x
                    y2 = y
                    code2 = self.compute_code(x2, y2, x_max, y_max, x_min,
                                              y_min)

        if accept:
            self.new_x1 = int(x1)
            self.new_x2 = int(x2)
            self.new_y1 = int(y1)
            self.new_y2 = int(y2)
            self.clear_canvas(
            )  # clear canvas so when the clip result is printed, only this will be visible
            self.draw_brese_line(
                self, transform=True)  # draw only the accepted parts
            print("Line accepted from %.2f, %.2f to %.2f, %.2f" %
                  (x1, y1, x2, y2))
        else:
            print("Line non accepted")

    def cliptest(self, p, q):
        result = True
        if p < 0.0:
            r = q / p
            if r > self.u2:
                result = False
            elif r > self.u1:
                self.u1 = r
        elif p > 0.0:
            r = q / p
            if r < self.u1:
                result = False
            elif r < self.u2:
                self.u2 = r
        elif q < 0.0:
            result = False

        return result

    def liang_barsky(self):
        # get input values
        x_max = int(self.x_max.get())
        y_max = int(self.y_max.get())
        x_min = int(self.x_min.get())
        y_min = int(self.y_min.get())

        # retrieve line initial and final points
        x1 = self.list[0]
        x2 = self.list[1]
        y1 = self.list[2]
        y2 = self.list[3]

        self.u1 = 0.0
        self.u2 = 1.0
        dx = x2 - x1
        dy = y2 - y1

        if self.cliptest(-dx, x1 - x_min):
            if self.cliptest(
                    dx,
                    x_max - x1,
            ):
                if self.cliptest(
                        -dy,
                        y1 - y_min,
                ):
                    if self.cliptest(dy, y_max - y1):
                        if self.u2 < 1.0:
                            x2 = x1 + self.u2 * dx
                            y2 = y1 + self.u2 * dy
                        if self.u1 > 0.0:
                            x1 = x1 + self.u1 * dx
                            y1 = y1 + self.u1 * dy
                        self.new_x1 = int(x1)
                        self.new_x2 = int(x2)
                        self.new_y1 = int(y1)
                        self.new_y2 = int(y2)
                        self.clear_canvas(
                        )  # clear canvas so when the clip result is printed, only this will be visible
                        self.draw_brese_line(
                            self,
                            transform=True)  # draw only the accepted parts
                        print("Line accepted from %.2f, %.2f to %.2f, %.2f" %
                              (x1, y1, x2, y2))
                    else:
                        print("Line non accepted")


paint_app = Paint()
