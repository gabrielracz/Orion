import math
import pygame
class Line:
    def __init__(self, origin, angle, intervals, speed, yv):
        self.origin = origin        # This is the origin point that the line will rotate around
        self.angle = angle          # This is the initial angle that the line will face, in degrees
        self.intervals = intervals  # This is a list of tuples representing the visible segments that create gaps
        self.speed = speed
        self.segments = []          # Represents the actual segments we'll draw, handled in update
        self.z = 0
        self.yv = yv
        self.passed = False
    
    def render(self, screen):
        if self.passed:
            color = (215, 255, 0)
        else:
            color = (255,255,255)
        for seg in self.segments:
            pygame.draw.aaline(screen, color, seg[0], seg[1])

    def rotate(self, deg=1):
        if self.z > 900:
            return False
        self.angle = (self.angle + deg)
        self.z = 5.3*(self.origin[1]-300)
        self.origin[0] += self.yv/990
        self.origin[1] += self.speed/990
        self._update_line_segments()
        return True

    def _update_line_segments(self):
        self.segments = []
        for partial_line in self.intervals:
            sol_x = self.origin[0] + math.cos(math.radians(self.angle)) * self.z/4 * partial_line[0]        #scale the line based on z, the proximity to the camera
            sol_y = self.origin[1] + math.sin(math.radians(self.angle)) * self.z/4 * partial_line[0]
            
            # ...and the end of the line...
            eol_x = self.origin[0] + math.cos(math.radians(self.angle)) * self.z/4 * partial_line[1]
            eol_y = self.origin[1] + math.sin(math.radians(self.angle)) * self.z/4 * partial_line[1]
            
            # ...and then add that line to the list
            self.segments.append( ((sol_x, sol_y), (eol_x, eol_y)) ) 