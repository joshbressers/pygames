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
    screen = pygame.display.set_mode((800, 608))
    pygame.display.set_caption('Teh Platformz')
    pygame.mouse.set_visible(1)
    background = pygame.Surface([800, 608])
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
                elif e.key == K_z:
                    the_hero.jump()
                elif e.key == K_n:
                    characters.sprites()[0].jump()
                elif e.key == K_m:
                    characters.sprites()[0].collide()
                elif e.key == K_d:
                    # Launch a debugger
                    pdb.set_trace()
                elif e.key == K_RIGHT:
                    the_hero.xvelocity = 3
                elif e.key == K_LEFT:
                    the_hero.xvelocity = -3

            elif e.type == KEYUP:
                if e.key == K_z:
                    the_hero.jump(False)
                elif e.key == K_n:
                    characters.sprites()[0].jump(False)
                elif e.key == K_RIGHT or e.key == K_LEFT:
                    the_hero.xvelocity = 0

        level.update(pygame.time.get_ticks())
        characters.update(pygame.time.get_ticks())

        all_sprites = []
        all_sprites.extend(level)
        all_sprites.extend(characters)

        collisions = pygame.sprite.groupcollide(characters, all_sprites, False, False)
        for i in collisions.keys():
            new_rect = None
            character = None
            hit_sprites = []

            for j in collisions[i]:
                if j is i: # Skip the case where we collide with ourself
                    continue
                if j.character: character = j
                if new_rect is None:
                    new_rect = j.rect
                else:
                    new_rect = new_rect.union(j.rect)
                hit_sprites.append(j)

            if new_rect is None:
                continue

            # We have 9 cases:
            # Up
            if i.xvelocity == 0 and i.yvelocity < 0:
                if i.rect.top <= new_rect.bottom:
                    i.rect.top = new_rect.bottom - 1
                    i.yvelocity = 0

            # Up-Right
            elif i.xvelocity > 0 and i.yvelocity < 0:
                # Hit a corner
                if new_rect.width > i.rect.width and \
                new_rect.height > i.rect.height:
                    i.rect.top = new_rect.centery + 1
                    i.rect.right = new_rect.centerx - 1
                    i.yvelocity = 0
                    i.collide(character)
                # Hit a side
                elif new_rect.clip(i.rect).height >= i.rect.height:
                    i.rect.right = new_rect.left - 1
                    i.collide(character)
                # Hit a bottom
                elif i.rect.clip(new_rect).width >= i.rect.width:
                    i.yvelocity = 0
                    i.rect.top = new_rect.bottom + 1

            # Right
            elif i.xvelocity > 0 and i.yvelocity == 0:
                if i.rect.right >= new_rect.left:
                    i.rect.right = new_rect.left - 1
                    i.collide(character)

            # Down-Right
            elif i.xvelocity > 0 and i.yvelocity > 0:
                # Hit a corner
                if new_rect.width > i.rect.width and \
                new_rect.height > i.rect.height:
                    i.rect.bottom = new_rect.centery
                    i.rect.right = new_rect.centerx - 1
                    i.yvelocity = 0
                    i.static = True
                    i.collide(character)
                # Hit a side
                elif new_rect.clip(i.rect).height >= i.rect.height:
                    i.rect.right = new_rect.left - 1
                    i.collide(character)
                # Hit a floor
                elif i.rect.clip(new_rect).width >= i.rect.width:
                    i.rect.bottom = new_rect.top
                    i.yvelocity = 0
                    i.static = True
                # Hit an edge
                elif new_rect.clip(i.rect).width > 0 and \
                new_rect.centery > i.rect.centery:
                    i.rect.bottom = new_rect.top

            # Down
            elif i.xvelocity == 0 and i.yvelocity > 0:
                if i.rect.bottom >= new_rect.top:
                    i.rect.bottom = new_rect.top
                    i.yvelocity = 0
                    i.static = True

            # Down-Left
            elif i.xvelocity < 0 and i.yvelocity > 0:
                # Hit a corner
                if new_rect.width > i.rect.width and \
                new_rect.height > i.rect.height:
                    i.rect.bottom = new_rect.centery - 1
                    i.rect.left = new_rect.centerx + 1
                    i.yvelocity = 0
                    i.static = True
                    i.collide(character)
                # Hit a side
                elif new_rect.clip(i.rect).height >= i.rect.height:
                    i.rect.left = new_rect.right + 1
                    i.collide(character)
                # Hit a floor
                elif new_rect.clip(i.rect).width >= i.rect.width:
                    i.rect.bottom = new_rect.top
                    i.yvelocity = 0
                    i.static = True
                # Hit an edge
                elif new_rect.clip(i.rect).width > 0 and \
                new_rect.centery > i.rect.centery:
                    i.rect.bottom = new_rect.top

            # Left
            elif i.xvelocity < 0 and i.yvelocity == 0:
                if i.rect.left <= new_rect.right:
                    i.rect.left = new_rect.right + 1
                    i.collide(character)

            # Up-Left
            elif i.xvelocity < 0 and i.yvelocity < 0:
                # Hit a corner
                if new_rect.width > i.rect.width and \
                new_rect.height > i.rect.height:
                    i.rect.top = new_rect.centery + 1
                    i.rect.left = new_rect.centerx + 1
                    i.yvelocity = 0
                    i.static = True
                    i.collide(character)
                # Hit a side
                elif new_rect.clip(i.rect).height >= i.rect.height:
                    i.rect.left = new_rect.right + 1
                    i.collide(character)
                # Hit a bottom
                elif new_rect.clip(i.rect).width >= i.rect.width:
                    i.yvelocity = 0
                    i.rect.top = new_rect.bottom + 1
                # Hit a corner

            # Standing still - This never happens
            elif i.xvelocity == 0 and i.yvelocity == 0:
                i.collide(character)


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
