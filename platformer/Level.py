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
import Sprites
import pygame

class Level():
    "Class for building a level"

    def __init__(self, level_file):
        self.filename = level_file
        fh = open(self.filename)

        self.level_sprites = pygame.sprite.RenderUpdates()
        self.character_sprites = pygame.sprite.RenderUpdates()

        row = 0
        col = 0

        for i in fh.readlines():
            row = 0
            i.rstrip()
            if i[0] == '#':
                continue

            for j in i:
                if j == ' ':
                    pass
                elif j == 'R':
                    self.level_sprites.add(Sprites.AnimateImageBox('data/graphics/red-brick.png',
[row, col]))
                elif j == 'r':
                    self.level_sprites.add(Sprites.AnimateImageBox('data/graphics/red-brick-animate.png',
[row, col]))
                elif j == 'B':
                    self.character_sprites.add(Sprites.Character("data/graphics/bad-guy.png", [row, col], 2, True))
                row = row + 32
            col = col + 32

    def get_sprites(self):
        return (self.level_sprites, self.character_sprites)
