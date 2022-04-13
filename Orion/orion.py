import pygame
import math
import time
import random
from lineclass import Line
from playerclass import Player
from structureclass import Structure
from circleclass import GameCircle

WIDTH = 800
HEIGHT = 800
framerate = 60
delta = 1
lines = []
gameover = False
player = None
hitcircle = None
flybox = False
fonts = {}
score = 0
cooldown = 0

def main():
    global elapsed, score, elapsed
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    elapsed = 0
    init()

    while not gameover:
        handle_inputs()
        render(screen)
        update()
        clock.tick(framerate)
        elapsed += (1/40)
    print("\n\nYou survived for: " + "{:.2f}".format(elapsed) + " seconds.")
    print("and scanned " + str(score) + " units of data.\n\n")

def handle_inputs():
    global gameover, player, flybox
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameover = True

            if event.key == pygame.K_a:
                player.left = True
            if event.key == pygame.K_d:
                player.right = True
            if event.key == pygame.K_w:
                player.fwd = True
            if event.key == pygame.K_s:
                player.bkwd = True
            if event.key == pygame.K_LSHIFT:
                player.up = True
            if event.key == pygame.K_LCTRL:
                player.down = True
            if event.key == pygame.K_m:
                flybox = not flybox
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.left = False
            if event.key == pygame.K_d:
                player.right = False
            if event.key == pygame.K_w:
                player.fwd = False
            if event.key == pygame.K_s:
                player.bkwd = False

def update():
    global lines, player, hitcircle, gameover
    if player.health == 0:
        gameover = True

    game_manager()
    for l in lines:
        l.rotate(2)
        if len(l.lines) == 0:
            lines.remove(l)
    player.move()
    hitcircle.update(player.xpos - 15*((player.z/720+0.4)), player.ypos, player.z, player.z/720 + 0.4)
    checkCollisions()
    return

def game_manager():     #This manages the spawning of structures and the progression of difficulty. Basically the more score, the more difficult structures begin spawning with random parameters
    global elapsed, lines, score, cooldown
    styles = ["wall", "tri", "plus", "wheel", "spiral"]
    if score < 30:
        level = 1
    elif score < 150:
        level = 2
    elif score < 250:
        level = 3
    elif score < 550:
        level = 4
    elif score < 750:
        level = 5
    else:
        level = 6

    if level == 1:
        spawntimer = random.randint(1,80)
        if score == 0 and spawntimer == 1 and len(lines) < 1:
            lines.append(Structure("wall", 150, 1, 7, 1, 2))
        if len(lines) < 1 and spawntimer == 1:
            lines.append(Structure("wall", random.randint(1,3)*50 + 100, random.randint(-4,4)*50 + 1, 7, 1, random.randint(1,3)))
    if level == 2:
        spawntimer = random.randint(1,120)
        if len(lines) < 1 and spawntimer == 1:
            lines.append(Structure("tri", random.randint(1,3)*50 + 100, random.randint(-4,4)*50 + 1, random.randint(6,15), 1, random.randint(2,3)))
    if level == 3:
        spawntimer = random.randint(1,120)
        if len(lines) < 2 and spawntimer == 1 and cooldown == 0:
            decider = random.randint(1,2)
            if decider == 1:
                lines.append(Structure("plus", 200, random.randint(-3,3)*50 + 1, random.randint(6,20), 1, 2))
                cooldown = 220
            else:
                lines.append(Structure("tri", 200, random.randint(-4,4)*50 + 1, random.randint(6,13), 1, random.randint(2,3)))
                cooldown = 220
    if level == 4:
        spawntimer = random.randint(1,120)
        if len(lines) < 2 and spawntimer == 1 and score < 400:
            lines.append(Structure("plus", 200, 240, 15, 1, 2))
            lines.append(Structure("plus", 200, -240, 15, 1, -2))
        elif len(lines) < 2 and spawntimer == 1:
            lines.append(Structure("tri", 200, 240, 15, 1, 4))
            lines.append(Structure("tri", 200, -240, 15, 1, -4))
    if level == 5:
        spawntimer = random.randint(1,120)
        if len(lines) < 1 and spawntimer == 1:
            rand = random.randint(1,2)
            if rand == 1:
                rotation = -2
            else:
                rotation = 2
            lines.append(Structure("wheel", random.randint(1,2)*50 + 100, random.randint(-2,2)*50 + 1, 13, 1, rotation))
            cooldown = 300
    if level == 6:
        spawntimer = random.randint(1,120)
        entity = random.randint(0,4)
        if len(lines) < 2 and spawntimer == 1 and cooldown == 0:
            rand = random.randint(1,2)
            if rand == 1:
                rotation = -1
            else:
                rotation = 1

            if entity == 1:
                lines.append(Structure("wall", random.randint(1,4)*50 + 100, random.randint(-5,5)*50 + 1, random.randint(5,25), 1, rotation * random.randint(2,4)))
                cooldown = 120
            elif entity == 2:
                lines.append(Structure("tri", random.randint(1,4)*50 + 100, random.randint(-4,4)*50 + 1, random.randint(7,20), 1, rotation * random.randint(2,4)))
                cooldown = 160
            elif entity == 3:
                lines.append(Structure("plus", random.randint(1,4)*50 + 100, random.randint(-4,4)*50 + 1, random.randint(10,15), 1, rotation * random.randint(2,4)))
                cooldown = 160
            elif entity == 4:
                lines.append(Structure("wheel", random.randint(1,2)*50 + 100, random.randint(-2,2)*50 + 1, random.randint(10,15), 1, rotation*2))
                cooldown = 200
            elif entity == 5:
                lines.append(Structure("spiral", random.randint(1,2)*50 + 100, random.randint(-2,2)*50 + 1, random.randint(15,25), 1, rotation*2))
                cooldown = 200


    if cooldown > 0:
        cooldown -= 1
def render(screen):
    global HEIGHT, WIDTH, lines, player, hitcircle, flybox, intro 
    #background
    screen.fill((0,0,0))


    #FlyBox
    if flybox:
        colour = (215, 255, 0)
        pygame.draw.aaline(screen, colour, (80 ,700), (280, 450))
        pygame.draw.aaline(screen, colour, (720 ,700), (520, 450))

        pygame.draw.aaline(screen, colour, (80 ,700), (80, 450))#V1
        pygame.draw.aaline(screen, colour, (280 ,450), (280, 355))#V2
        pygame.draw.aaline(screen, colour, (80 ,450), (280, 355))#H

        pygame.draw.aaline(screen, colour, (720 ,700), (720, 450))#-V1
        pygame.draw.aaline(screen, colour, (520 ,450), (520, 355))#-V2ws
        pygame.draw.aaline(screen, colour, (720 ,450), (520, 355))#-H

        pygame.draw.aaline(screen, colour, (80 ,700), (720, 700))#HB
        pygame.draw.aaline(screen, colour, (280 ,450), (520, 450))#HT


    player.render(screen)
    hitcircle.render(screen)
    hud(screen)
    #gameobjects
    for l in lines:
        l.render(screen)
   
    pygame.display.update()

def hud(screen):        #Handles printing of player information
    global HEIGHT, WIDTH, player, elapsed, fonts

    timetext = fonts["time"].render("Time:   " + "{:.2f}".format(elapsed), False, (255,255,255))
    screen.blit(timetext, (10,10))

    healthtext = fonts["time"].render("Health: ""{:3d}".format(player.health), False, (255, 255, 255))
    screen.blit(healthtext, (10, 30))

    scoretext = fonts["health"].render("[ " + str(score) + " ]", False, (215,255,0))
    screen.blit(scoretext, (370, 70))
    return


def init():
    global lines, player, hitcircle, fonts
    pygame.font.init()
    # pygame.mixer.music.load("Go.mp3")  #backingtrack
    # background = pygame.mixer.Channel(0)
    # background.set_volume(0.3)
    # background.play(pygame.mixer.Sound("./Go.mp3"), -1)

    fonts["time"] = pygame.font.SysFont('Consolas', 18)
    fonts["health"] = pygame.font.SysFont('Consolas', 18)


    player = Player()
    hitcircle = GameCircle([player.xpos, player.ypos], 10)      #player's hitbox is the circle
    return

def checkCollisions():      #Check every segment of every line of every structure of the stage
    global lines, hitcircle, player, score
    for structure in lines:
        for line in structure.lines:
            if abs(line.z - hitcircle.z) < 19:
                for segment in line.segments:
                    if detect_collision_line_circ(segment, hitcircle):
                        player.handleCollision()
                        break
                if math.sqrt((hitcircle.position[0] - line.origin[0])**2 + (hitcircle.position[1] - line.origin[1])**2) < (line.z/3) and line.passed == False:
                    score += 1
                    line.passed = True

def detect_collision_line_circ(line_points, circle):
    (u_sol, u_eol) = line_points
    (u_sol_x, u_sol_y) = u_sol
    (u_eol_x, u_eol_y) = u_eol

    (v_ctr, v_rad) = (circle.position, circle.radius)
    (v_ctr_x, v_ctr_y) = v_ctr
    
    t = ((v_ctr_x - u_sol_x) * (u_eol_x - u_sol_x) + (v_ctr_y - u_sol_y) * (u_eol_y - u_sol_y)) / ((u_eol_x - u_sol_x) ** 2 + (u_eol_y - u_sol_y) ** 2)

    t = max(min(t, 1), 0)

    w_x = u_sol_x + t * (u_eol_x - u_sol_x)
    w_y = u_sol_y + t * (u_eol_y - u_sol_y)
    
    d_sqr = (w_x - v_ctr_x) ** 2 + (w_y - v_ctr_y) ** 2
    
    if (d_sqr <= v_rad ** 2):
        return True  # the point of collision is (int(w_x), int(w_y))
        
    else:
        return False

if __name__ == "__main__":
    main()

