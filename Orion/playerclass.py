import pygame
import math
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("ship.png").convert_alpha()
        self.width = 21
        self.xpos = 420
        self.ypos = 600
        self.depth = 20

        self.left = False
        self.right = False
        self.fwd = False
        self.bkwd = False

        self.lean = 0
        self.hvelocity = 0
        self.fvelocity = 0
        self.zvelocity = 0
        self.height = 0

        self.health = 100
        self.collision = False
        self.hitsound = pygame.mixer.Sound("explosion.wav")
        self.buffer = 0

        self.rect = self.image.get_rect()
        self.z = 720
    
    def render(self, screen):
        scale = self.z/720 + 0.4        #scale by distance from camera
        image = pygame.transform.scale(self.image, (int(self.rect.bottomright[0]*scale), int(self.rect.bottomright[1]*scale-(self.height/10))))
        image = pygame.transform.rotate(image, self.lean)   #lean the ship based on movement
        screen.blit(image, (self.xpos - int(image.get_width()), self.ypos-int(image.get_height()/2)))
    
    def findComponents(self):       #math function for finding components based on angle
        deltax = (self.xpos - 400)
        deltay = (self.ypos - 300)
        velocity = 2
        theta = math.atan2(deltay, deltax)
        ycomponent = velocity
        xcomponent = ycomponent/math.tan(theta)
        return xcomponent, ycomponent
    
    def move(self):

        if self.left and not self.right and self.xpos > (-self.ypos + 702):
            if self.hvelocity > -3:
                self.hvelocity -= 0.1

            if self.lean < 25:
                self.lean += 3
        elif self.right and not self.left and self.xpos < ((self.ypos+200) -98):
            if self.hvelocity < 3:
                self.hvelocity += 0.1

            if self.lean > -25:
                self.lean -= 3
        else:
            if self.hvelocity < -0.1:
                self.hvelocity += 0.05
            elif self.hvelocity > 0.1:
                self.hvelocity -= 0.05
            else:
                self.hvelocity = 0

            if self.lean < 0:
                self.lean += 3
            elif self.lean > 0:
                self.lean -= 3

        if self.fwd and not self.bkwd and self.z > 250:
            components = self.findComponents()
            self.xpos -= components[0]
            self.ypos -= components[1]
            self.z -= 5
        if self.bkwd and not self.fwd and self.z < 800:
            components = self.findComponents()
            self.xpos += components[0]
            self.ypos += components[1]
            self.z += 5
        
        self.xpos += self.hvelocity     #velocity is used to change positions to allow for acceleration
        self.ypos += self.fvelocity

        if self.buffer > 0:
            self.buffer -= 1

    def handleCollision(self):
        if self.buffer == 0:
            self.health -= 20
            self.buffer = 50        #50 frame invincibility window to avoid repeated collisions
            self.hitsound.play()
        
