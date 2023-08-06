from turtle import Turtle
import tkinter as TK
import math

class CoolTurtle(Turtle):

    def __rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def fillrgba(self, r, g, b, a):
        hex_val = self.__rgb_to_hex((r, g, b))
        self.fillcolor(hex_val)

    def ellipse(self, a, b, deg=360):
        (cx, cy) = self.position()
        n = 100
        # draw the first point with pen up
        t = angle = 0
        x = cx + a*math.cos(t)*math.cos(math.radians(angle))-b*math.sin(t)*math.sin(math.radians(angle))
        y = cy + a*math.cos(t)*math.sin(math.radians(angle))+b*math.sin(t)*math.cos(math.radians(angle))
        self.up()
        self.goto(x,y)
        self.down()
        (xi, yi) = self.position()
        # draw the rest with pen down
        for i in range(n):
            x = cx + a*math.cos(t)*math.cos(math.radians(angle))-b*math.sin(t)*math.sin(math.radians(angle))
            y = cy + a*math.cos(t)*math.sin(math.radians(angle))+b*math.sin(t)*math.cos(math.radians(angle))
            self.goto(x,y)    
            t += math.radians(-deg)/n

        # close the shape
        if deg == 360:
            self.goto(xi, yi)

    def done(self):
        TK.mainloop()
