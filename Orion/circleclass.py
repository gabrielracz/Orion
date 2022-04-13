import pygame
class GameCircle:                               #The circle is an invisible hitbox overlayed ontop of the ship's position
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
        self.colliding = False
        self.z = 0
        self.draw = False

    def render(self, screen):
        if self.draw:
            pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)

    def update(self, x, y, z, scale):
        self.position[0] = x
        self.position[1] = y
        self.z = z
        self.radius = 10 * scale