import pygame
import sys
import random
import math
from pygame.locals import *
import time
pygame.init()

# constants
SPEED = 1
WIDTH = 1200
HEIGHT = 800
ACCEL = .00045

# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graveyard Shift !!!")
background = pygame.image.load("images/background.png").convert()
gameover = pygame.image.load("images/gameover.jpg").convert()

# char 1 = main character
# char 2 = zombies
# char 3 = mines
# char 4 = fire
# char 5 = sink hole


class Sprite:
    def __init__(self, img_name, char):
        img = pygame.image.load(img_name).convert()

        # direction of MC prior to attack
        self.type = 1

        # SH counter
        self.counter = 0
        self.limit = 5
        walkD = ""
        
        self.charType = char
        self.life = 3
        self.attackT = -1
        self.attackD = "z"
        self.fTimer = random.random()*1500 + 3000
        self.onFire = False
        self.active = False

        tgtw = 30
        tgth = int(img.get_height() * (tgtw/float(img.get_width())))

        tgtvw = 45
        tgtvh = int(img.get_height() * (tgtvw/float(img.get_width())))

        tgtow = 55
        tgtoh = int(img.get_height() * (tgtow/float(img.get_width()*1.5)))

        tgtww = 80
        tgtwh = int(img.get_height() * (tgtww/float(img.get_width()*1.5)))

        # if sprite is the Main Character
        if char == 1:
            self.W_R = pygame.image.load("images/Undertaker_walkRight.gif").convert()
            self.W_R = pygame.transform.scale(self.W_R, (tgtw, tgth))
            
            self.W_L = pygame.image.load("images/Undertaker_walkLeft.gif").convert()
            self.W_L = pygame.transform.scale(self.W_L, (tgtw, tgth))
            
            self.W_U = pygame.image.load("images/Undertaker_walkUpRight.gif").convert()
            self.W_U = pygame.transform.scale(self.W_U, (tgtw, tgth))

            self.A_R = pygame.image.load("images/Undertaker_attackRight.gif").convert()
            self.A_R = pygame.transform.scale(self.A_R, (tgtow, tgtoh))

            self.A_L = pygame.image.load("images/Undertaker_attackLeft.gif").convert()
            self.A_L = pygame.transform.scale(self.A_L, (tgtow, tgtoh))

            self.A_U = pygame.image.load("images/Undertaker_attackUpRight.gif").convert()
            self.A_U = pygame.transform.scale(self.A_U, (tgtvw, tgtvh))

            self.A_D = pygame.image.load("images/Undertaker_attackDownRight.gif").convert()
            self.A_D = pygame.transform.scale(self.A_D, (tgtvw, tgtvh))
            self.pos = Vector2d(600, 400)
            self.img = pygame.transform.scale(img, (tgtw, tgth))
            
        elif char == 2:
            self.Z_F = pygame.image.load("images/zombie_fire.gif").convert()
            rpos = random.random()*4
            if rpos <= 1:
                self.pos = Vector2d(0 - random.random()*200, random.random()*800)
            elif rpos <= 2:
                self.pos = Vector2d(random.random()*1200, 0 - random.random()*200)
            elif rpos <= 3:
                self.pos = Vector2d(random.random()*200 + 1200, random.random()*800)
            elif rpos <= 4:
                self.pos = Vector2d(random.random()*1200, random.random()*200 + 800)
            self.img = pygame.transform.scale(img, (tgtw, tgth))
        elif char == 3 or char == 4:
            self.pos = Vector2d(random.random()*800, random.random()*800)
            self.img = pygame.transform.scale(img, (tgtw, tgth))
        elif char == 5:
            self.it = pygame.image.load(img_name).convert()
            self.img = pygame.transform.scale(self.it, (tgtww, tgtwh))
            self.pos = Vector2d(-50, -50)
        else:
            self.pos = Vector2d(0, 0)
            self.img = pygame.transform.scale(img, (tgtw, tgth))

        self.vel = Vector2d(0, 0)
        self.tgt = Vector2d(0, 0)

    def set_target(self, loc, tick):
        self.tgt = loc.copy()
        self.tgt.subtract(self.pos)
        self.tgt.normalize()
        self.pos.x += self.tgt.x/20 * tick
        self.pos.y += self.tgt.y/20 * tick

    def collides(self, sp, char, tick):

        # x,y, width and height for self
        x1 = self.pos.x
        y1 = self.pos.y
        w1 = self.img.get_width()
        h1 = self.img.get_height()

        # x,y, width and height for sp
        x2 = sp.pos.x
        y2 = sp.pos.y
        w2 = sp.img.get_width()
        h2 = sp.img.get_height()

        if x1 > x2 and x1 < x2+w2 or x1+w1 > x2 and x1+w1 < x2+w2:
            if y1 > y2 and y1 < y2+h2 or y1+h1 > y2 and y1+h1 < y2+h2:
                if char == 1:
                    # colliding with zombie
                    if sp.charType == 2 and self.attackT > 0:
                        # zombie on right was hit
                        if self.attackD == "r":
                            if x1+w1-(w1/2) > x2 and x1+w1-(w1/2) < x2+w2 or x1+w1 > x2 and x1+w1 < x2+w2:
                                zombies.remove(sp)
                                self.counter += 1
                            else:
                                self.life -= 1
                        elif self.attackD == "d":
                            if y1+h1-(h1/2) > y2 and y1+h1-(h1/2) < y2+h2 or y1+h1 > y2 and y1+h1 < y2+h2:
                                zombies.remove(sp)
                                self.counter += 1
                            else:
                                self.life -= 1
                        elif self.attackD == "l":
                            if x1 > x2 and x1 < x2+w2 or x1+(w1/2) > x2 and x1+(w1/2) < x2+w2:
                                zombies.remove(sp)
                                self.counter += 1
                            else:
                                self.life -= 1
                        elif self.attackD == "u":
                            if y1 > y2 and y1 < y2+h2 or y1+(h1/2) > y2 and y1+(h1/2) < y2+h2:
                                zombies.remove(sp)
                                self.counter += 1
                            else:
                                self.life -= 1
                    else:
                        self.life -= 1
                elif char == 2:
                    sp.pos.x -= sp.tgt.x/10 * tick
                    sp.pos.y -= sp.tgt.y/10 * tick
                elif char == 3:
                    return True
                elif char == 4 or char == 5:
                    return True
        else:
            return False
                    
    def update(self, char, tick, SH):

        # upper and lower boundary
        if self.img.get_height()+ self.pos.y > HEIGHT:
            self.pos.y = HEIGHT - self.img.get_height()
            self.vel.y = 0
        elif self.pos.y < 0:
            self.pos.y = 0
            self.vel.y=0

        # right and left boundary
        if self.img.get_width() + self.pos.x > WIDTH:
            self.pos.x = WIDTH - self.img.get_width()
            self.vel.x = 0
        elif self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0

        # if hole is active
        dist = math.sqrt(math.pow(SH.pos.x - self.pos.x, 2)+math.pow(SH.pos.y - self.pos.y, 2))
        
        if SH.active and dist < 150:
            if SH.pos.x < self.pos.x:
                self.vel.x += -1 * ACCEL * tick
            else:
                self.vel.x += ACCEL * tick

            if SH.pos.y < self.pos.y:
                self.vel.y += -1 * ACCEL * tick
            else:
                self.vel.y += ACCEL * tick
        
            self.pos.x = self.pos.x + self.vel.x * tick
            self.pos.y = self.pos.y + self.vel.y * tick

        if char == 1:
            self.pos.x = self.pos.x + self.vel.x * tick
            self.pos.y = self.pos.y + self.vel.y * tick
            
    def draw(self, screen):
        screen.blit(self.img, self.pos.tolist())

    def set_random(self):
        self.set_target(Vector2d(random.random() * WIDTH, random.random() * HEIGHT))
        

class Vector2d:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mag = 0

    def subtract(self, v):
        self.x = self.x - v.x
        self.y = self.y - v.y

    def magnitude(self):
        self.mag = math.sqrt(self.x*self.x + self.y*self.y)
        return self.mag

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            self.x /= mag
            self.y /= mag

    def add(self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y

    def tolist(self):
        return self.x, self.y

    def copy(self):
        c = Vector2d(self.x, self.y)
        return c

    def multiply(self, a):
        self.x = self.x * a
        self.y = self.y * a


# main character
MC = Sprite ("images/Undertaker_walkRight.gif", 1)

# some zombies
zombies = []
for i in range(0, 1):
    zombies.append(Sprite("images/zombie.gif", 2))

# mines
mines = []
for mine in range(0, 8):
    mines.append(Sprite("images/mine.JPEG", 3))

# fire that spawns from mines
fire = []

# sinkhole
SH = Sprite("images/ring.gif", 5)
SH.timeLeft = 0
ztime = 0

# while the MC is alive. he has 3 lives
prev_time = pygame.time.get_ticks()
while MC.life >= 0:
    
    time_t = pygame.time.get_ticks()
    tick = time_t - prev_time
    prev_time = time_t

    screen.blit(background, [0, 0])

    pygame.event.pump()

    if MC.counter >= MC.limit:
        power = pygame.image.load("images/ring.gif").convert()
        power = pygame.transform.scale(power, (50, 50))
        screen.blit(power, [10, 10])
        
    # zombie spawning
    if ztime > 1000:
        for i in range(0, 1):
            zombies.append(Sprite("images/zombie.gif", 2))
        ztime = 0
    else:
        ztime = ztime + tick
    
    # time limit in attack
    if MC.attackT < 0:
        if MC.type == 1:
            MC.img = MC.W_R
        elif MC.type == 2:
            MC.img = MC.W_L
        else:
            MC.img = MC.W_U
    else:
        MC.attackT = MC.attackT - tick

    # time limit on sink hole
    if SH.timeLeft > 1500:
        SH.active = False
        SH.pos.x = -50
        SH.pos.y = -50
    else:
        SH.timeLeft = SH.timeLeft + tick
    
    # zombies on fire, this is when they die
    for z in zombies:
        if z.fTimer <= 0 and z.onFire:
            ztmp = z.pos
            zombies.remove(z)
            f = Sprite( "images/fire.gif", 4 )
            f.pos = ztmp
            fire.append(f)
        elif z.onFire:
            z.fTimer = z.fTimer - tick
        
    # events
    for evt in pygame.event.get():
        if evt.type == QUIT:
            pygame.quit()
            sys.exit()
        elif evt.type == KEYDOWN and evt.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif evt.type == MOUSEBUTTONDOWN:
            newtgt = pygame.mouse.get_pos()

        # register the events of the main character.
        if evt.type == KEYDOWN:
            if evt.key == ord('w'):
                MC.img = MC.W_U
                MC.vel.y = -.15
                MC.type = 3
                MC.walkD = "u"
            elif evt.key == ord('a'):
                MC.img = MC.W_L
                MC.vel.x = -.15
                MC.type = 2
                MC.walkD = "l"
            elif evt.key == ord('s'):
                MC.img = MC.W_R
                MC.vel.y = .15
                MC.type = 1
                MC.walkD = "d"
            elif evt.key == ord('d'):
                MC.img = MC.W_R
                MC.vel.x = .15
                MC.type = 1
                MC.walkD = "r"
            elif evt.key == ord(' ') and MC.counter >= MC.limit:
                if MC.walkD == "l":
                    SH.pos.x = MC.pos.x - 200
                    SH.pos.y = MC.pos.y
                elif MC.walkD == "r":
                    SH.pos.x = MC.pos.x + 200
                    SH.pos.y = MC.pos.y
                elif MC.walkD == "u" :
                    SH.pos.y = MC.pos.y - 200
                    SH.pos.x = MC.pos.x
                elif MC.walkD == "d":
                    SH.pos.y = MC.pos.y + 200
                    SH.pos.x = MC.pos.x
                SH.active = True
                SH.timeLeft = 0
                MC.limit += 1
                MC.counter = 0

        if evt.type == KEYUP:
            if evt.key == ord('w'):
                MC.vel.y = 0
            elif evt.key == ord('a'):
                MC.vel.x = 0
            elif evt.key == ord('s'):
                MC.vel.y = 0
            elif evt.key == ord('d'):
                MC.vel.x = 0
                
            if evt.key == K_UP:
                MC.img = MC.A_U
                MC.attackT = 250
                MC.attackD = "u"
                MC.walkD = "u"
                MC.type = 3
            elif evt.key == K_RIGHT:
                MC.img = MC.A_R
                MC.collides(MC, 1, tick)
                MC.attackT = 250
                MC.attackD = "r"
                MC.walkD = "r"
                MC.type = 1
            elif evt.key == K_DOWN:
                MC.img = MC.A_D
                MC.attackT = 250
                MC.attackD = "d"
                MC.walkD = "d"
                MC.type = 1
            elif evt.key == K_LEFT:
                MC.img = MC.A_L
                MC.attackT = 250
                MC.attackD = "l"
                MC.walkD = "l"
                MC.type = 2
                
    # zombies colliding with each other
    i = 1
    for zombie in zombies:
        for z2 in range(i,len(zombies)):
            zombie.collides(zombies[z2], 2, tick)
        i += 1

    # mines vs zombies
    explode = False
    zIndx = []
    mIndx = []
    for m in range(0, len(mines)):
        for z in range(0, len(zombies)):
            if mines[m].collides(zombies[z], 3,tick):
                zIndx.append(zombies[z])
                explode = True
        if explode:
            mIndx.append(mines[m])
            break
    # remove zombie and mine that collided and spawn the fire.
    for z in zIndx:
        zombies.remove(z)
    for m in mIndx:
        tmp = m.pos
        mines.remove(m)
        f = Sprite("images/fire.gif", 4)
        f.pos = tmp
        fire.append(f)

    # burning zombies
    for f in fire:
        for z in zombies:
            if f.collides(z, 4, tick):
                z.img = z.Z_F
                z.onFire = True

    # sink hole vs everything else
    for zom in zombies:
        if SH.collides(zom, 5,tick):
            zombies.remove(zom)
    for f in fire:
        if SH.collides(f, 5,tick):
            fire.remove(f)

    # Shovel colliding with zombies, fire, mines and sinkhole
    for z in zombies:
        MC.collides(z, 1, tick)
    for f in fire:
        MC.collides(f, 1, tick)
    for m in mines:
        MC.collides(m, 1, tick)
    MC.collides(SH, 1, tick)

    # update and draw zombies
    for zombie in zombies:
        zombie.set_target(MC.pos, tick)
        zombie.update(2, tick, SH)
        zombie.draw(screen)

    # update and draw mines
    for mine in mines:
        mine.draw(screen)

    # update and draw fire
    for f in fire:
        f.update(4, tick, SH)
        f.draw(screen)

    # update and draw MC
    MC.update(1, tick, SH)
    MC.draw(screen)

    # sink hole
    if SH.active:
        SH.draw(screen)
    
    pygame.display.flip()

time.sleep(1)
gameover = pygame.transform.scale(gameover, (1200, 800))
screen.blit(gameover, [0, 0])
pygame.display.flip()
time.sleep(2)
pygame.quit()
sys.exit()

