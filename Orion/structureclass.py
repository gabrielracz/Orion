from lineclass import Line
import random
class Structure():                                                  #This class is a convenient way to group and store differing configurations of lines.
    def __init__(self, style, xv, yv, depth, scale, rotate):
        self.style = style
        self.xv = xv
        self.yv = yv
        self.depth = depth
        self.scale = scale
        self.lines = []
        self.build()
        self.rotationspeed = rotate
        
    def build(self):            #All of that disgusting math is to create the 3D effect where each depth of line is slightly slower than the one infront.
        WIDTH = 800
        HEIGHT = 800
        if self.style == "wall":
            for i in range(self.depth):
                self.lines.append(Line([WIDTH/2, HEIGHT/2-100], 90, [[-1,1]], self.xv - (i*5), self.yv- self.yv/abs(self.yv)*(i*(abs(self.yv)/40))))
        if self.style == "tri":
            for i in range(self.depth):
                for x in range(0,360,120):
                    self.lines.append(Line([WIDTH/2, HEIGHT/2-100], x, [[0,1]], self.xv - (i*5), self.yv - self.yv/abs(self.yv)*(i*(abs(self.yv)/40))))
        if self.style == "plus":
            for i in range(self.depth):
                self.lines.append(Line([WIDTH/2, HEIGHT/2-100], 90, [[-1,1]], self.xv - (i*5), self.yv- self.yv/abs(self.yv)*(i*(abs(self.yv)/40))))
                self.lines.append(Line([WIDTH/2, HEIGHT/2-100], 0, [[-1,1]], self.xv - (i*5), self.yv- self.yv/abs(self.yv)*(i*(abs(self.yv)/40))))
        if self.style == "spiral":
            for i in range(self.depth):
                self.lines.append(Line([WIDTH/2, HEIGHT/2-100], i*10, [[-1,1]], self.xv - (i*5), self.yv - self.yv/abs(self.yv)*(i*(abs(self.yv)/40))))
        if self.style == "star":
            for i in range(self.depth):
                for x in range(0, 180, 30):
                        self.lines.append(Line([WIDTH/2, HEIGHT/2-100], x, [[-1,-0.2], [0.2,1]], self.xv - (i*5), self.yv- self.yv/abs(self.yv)*(i*(abs(self.yv)/40))))
        if self.style == "wheel":
            space = random.randint(30,60)
            for i in range(self.depth):
                for x in range(0, 180, 20):
                    if x < space:
                        pass
                    else:
                        self.lines.append(Line([WIDTH/2, HEIGHT/2-100], x+(i*2), [[-1,1]], self.xv - (i*5), self.yv- self.yv/abs(self.yv)*(i*(abs(self.yv)/40))))

    def render(self, screen):
        for line in self.lines:     #call render to all of this structure's line
            line.render(screen)
    
    def rotate(self, deg = 1):
        for line in self.lines:         #rotate all lines
            if line.rotate(self.rotationspeed) == False:
                self.lines.remove(line)
