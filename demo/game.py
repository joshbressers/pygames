#!/usr/bin/python

import sys, random, time
import math
import pygame
from pygame.locals import *
pygame.mixer.pre_init(frequency=22050, size=-16, channels=8, buffer=256)

class SpaceObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x_vel = 0
        self.y_vel = 0
        self.real_x = 0
        self.real_y = 0
        self.spin = 0
        self.angle = 0

    def move_up(self):
        self.y_vel = self.y_vel - 0.1
    def move_down(self):
        self.y_vel = self.y_vel + 0.1
    def move_left(self):
        self.x_vel = self.x_vel - 0.1
    def move_right(self):
        self.x_vel = self.x_vel + 0.1

    def update(self):
        if self.spin:
            center = self.rect.center
            self.angle = self.angle + self.spin
            self.angle = self.angle % 360
            self.image = pygame.transform.rotate(self.original, self.angle)
            self.rect = self.image.get_rect(center=center)

        self.real_x = self.real_x + self.x_vel
        self.real_y = self.real_y + self.y_vel

        if self.real_x < -20:
            self.real_x = 660
        if self.real_x > 660:
            self.real_x = -20
        if self.real_y < -20:
            self.real_y = 500
        if self.real_y > 500:
            self.real_y = -20

        self.rect.centerx = self.real_x
        self.rect.centery = self.real_y

class Bullet(SpaceObject):

    def __init__(self, ship):
        SpaceObject.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.rect = self.image.get_rect(center=(ship.rect.centerx,
            ship.rect.centery))
        self.real_x = self.rect.centerx
        self.real_y = self.rect.centery
        self.image.fill((255, 255, 255))

        radians = math.radians(ship.angle)
        self.x_vel = math.cos(radians) * -2 + ship.x_vel
        self.y_vel = math.sin(radians) * 2 + ship.y_vel

        self.updates = 0

    def update(self):
        SpaceObject.update(self)

        if self.updates > 200:
            self.kill()
        else:
            self.updates = self.updates + 1

class Ship(SpaceObject):

    def __init__(self, x_vel = 0, y_vel = 0):
        SpaceObject.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load("rocket.png")
        self.image_fire = pygame.image.load("rocket-fire.png")
        #self.image.fill((0, 0, 255))
        #pygame.draw.polygon(self.image, (255, 255, 255),
        #    [(0, 10), (20, 2), (20, 18)])
        self.original = self.image
        self.rect = self.image.get_rect(center=(320,240))
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.real_x = self.rect.centerx
        self.real_y = self.rect.centery
        self.angle = 0
        self.spin = 0
        self.on_fire = 0

    def update(self):
        if self.on_fire:
            radians = math.radians(self.angle)
            self.x_vel = self.x_vel - (math.cos(radians) * 0.1)
            self.y_vel = self.y_vel + (math.sin(radians) * 0.1)
            self.image = pygame.transform.rotate(self.image_fire, self.angle)
        else:
            self.image = pygame.transform.rotate(self.original, self.angle)

        SpaceObject.update(self)

    def rotate(self, angle):
        self.spin = angle

    def thruster(self, on):
        if on:
            self.on_fire = 1
        else:
            self.on_fire = 0

class Rock(SpaceObject):

    def __init__(self, parent = None):
        SpaceObject.__init__(self)
        if parent is None: # one Big rock
            self.big = True
            self.image = pygame.image.load("rock-big.png")
            self.original = self.image
            self.rect = self.image.get_rect(center=(random.randrange(0, 640),
                random.randrange(0, 480)))
            self.real_x = self.rect.centerx
            self.real_y = self.rect.centery
        else: # Little rock (it's breaking up
            self.big = False
            self.image = pygame.image.load("rock-small.png")
            self.original = self.image
            self.rect = self.image.get_rect(center=(parent.rect.centerx,
                parent.rect.centery))
            self.real_x = self.rect.centerx
            self.real_y = self.rect.centery

        self.x_vel = random.random() * 4 - 2
        self.y_vel = random.random() * 4 - 2
        self.spin = random.random() * 4 - 2
        self.sound = pygame.mixer.Sound("asplode.wav")

    def asplode(self):
        new_rocks = []
        self.sound.play()
        if self.big:
            for i in range(3):
                new_rocks.append(Rock(self))
        self.kill()
        return new_rocks

def main():
    pygame.init()
    pygame.mixer.init()
    pew_pew = pygame.mixer.Sound("laser.wav")
    sprites = pygame.sprite.RenderUpdates()
    enemies = pygame.sprite.RenderUpdates()
    bullets = pygame.sprite.RenderUpdates()

    screen = pygame.display.set_mode([640, 480])
    background = pygame.Surface((640, 480))

    pygame.display.set_caption('A Game')
    clock = pygame.time.Clock()

    screen.blit(background, (0, 0))
    pygame.display.flip()

    ship = Ship()
    sprites.add(ship)

    for i in range(3):
        enemies.add(Rock())

    # Main Loop
    while 1:
        clock.tick(60) # 60 milliseconds

        event = pygame.event.poll() # Get our events
        if event.type == QUIT:
            return
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return
            elif event.key == K_UP: ship.thruster(True)
            elif event.key == K_LEFT: ship.rotate(2)
            elif event.key == K_RIGHT: ship.rotate(-2)
            elif event.key == K_SPACE:
                bullets.add(Bullet(ship))
                pew_pew.play()
        elif event.type == KEYUP:
            if event.key == K_LEFT: ship.rotate(0)
            if event.key == K_RIGHT: ship.rotate(0)
            if event.key == K_UP: ship.thruster(False)


        sprites.update()
        enemies.update()
        bullets.update()

        # Collide bad guys with the good guy
        collisions = pygame.sprite.groupcollide([ship], enemies, False,
            False)
        for i in collisions:
            font = pygame.font.Font(None, 120)
            text = font.render("Dead", 1, (255, 255, 255))
            textpos = text.get_rect(centerx=screen.get_width()/2,
                centery=screen.get_height()/2)
            rectlist = screen.blit(text, textpos)
            pygame.display.flip()
            time.sleep(2)
            return

        # See if the bullet hits anything
        collisions = pygame.sprite.groupcollide(enemies, bullets, False,
            False)
        for i in collisions:
            for j in i.asplode():
                enemies.add(j)
            if len(enemies) == 0:
                font = pygame.font.Font(None, 120)
                text = font.render("You Win", 1, (255, 255, 255))
                textpos = text.get_rect(centerx=screen.get_width()/2,
                    centery=screen.get_height()/2)
                rectlist = screen.blit(text, textpos)
                pygame.display.flip()
                time.sleep(2)
                return

        rectlist = enemies.draw(screen)
        pygame.display.update(rectlist)
        rectlist = bullets.draw(screen)
        pygame.display.update(rectlist)
        rectlist = sprites.draw(screen)
        pygame.display.update(rectlist)
        enemies.clear(screen, background)
        bullets.clear(screen, background)
        sprites.clear(screen, background)

if __name__ == '__main__':
    main()
