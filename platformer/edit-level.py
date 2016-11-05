#!/usr/bin/env python

# Copyright 2010 Josh Bressers
#
# This file is part of Platformer.
#
# Platformer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Platformer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Platformer.  If not, see <http://www.gnu.org/licenses/>.

import os, sys
import pygame
import pdb
import pygame.sprite
from pygame.locals import *
from pygame.color import THECOLORS

import Sprites
import Level


def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Teh Platformz')
    pygame.mouse.set_visible(1)
    background = pygame.Surface([1024, 768])
    background.fill(THECOLORS["black"])
    screen.blit(background, [0,0])

    the_level = Level.Level("data/levels/level1.dat")
    (level, characters) = the_level.get_sprites()
    the_hero = Sprites.Character("data/graphics/hero-small.png", [40,40])
    characters.add(the_hero)

    done = False
    # Main loop
    while not done:

        # Check for input
        for e in pygame.event.get():
            if e.type == QUIT:
                done = True
                break
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    done = True
                    break

        level.update(pygame.time.get_ticks())
        #characters.update(pygame.time.get_ticks())

        rectlist = level.draw(screen)
        rectlist.extend(characters.draw(screen))
        pygame.display.update(rectlist)

        pygame.time.delay(10)
        level.clear(screen, background)
        characters.clear(screen, background)

    print "Done"
    return

if __name__ == "__main__":
    main()
