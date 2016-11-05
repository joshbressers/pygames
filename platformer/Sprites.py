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
import pygame.transform
from pygame.locals import *
from pygame.color import THECOLORS

class AnimateImageBox(pygame.sprite.Sprite):
    "This is an image is animated"

    def __init__(self, image_filename, initial_position):
        pygame.sprite.Sprite.__init__(self)

        self.master_image = pygame.image.load(image_filename)
        master_width, master_height = self.master_image.get_size()
        self.num_images = int(master_width/32)
        self.cur_image = 0

        self.images = []

        for i in xrange(self.num_images):
            self.images.append(self.master_image.subsurface((i*32,0,32,32)))

        self.image = self.images[self.cur_image]
        self.rect = self.images[0].get_rect()
        self.rect.topleft = initial_position
        self.static = True
        self.face_right = True
        self.character = False
        self.next_animate_time = 0
        self.animate_delay = 300

    def update(self, current_time):
        # Update every 10 milliseconds = 1/100th of a second.
        if self.next_animate_time < current_time:
            if self.cur_image >= self.num_images:
                self.cur_image = 0

            if self.face_right:
                self.image = self.images[self.cur_image]
            else:
                self.image = pygame.transform.flip(
                    self.images[self.cur_image], True, False)
            self.cur_image = self.cur_image + 1

            self.next_animate_time = current_time + self.animate_delay

class Box(AnimateImageBox):

    def __init__(self, image_filename, initial_position):
        AnimateImageBox.__init__(self, image_file, initial_position)
        self.bounce = 0

    def update(self, current_time):
        AnimateImageBox.update(self, current_time)
        self.next_update_time = 0

        if self.next_update_time < current_time:
            if self.bounce > 0:
                self.bounce = self.bounce - 1
            self.rect.top = self.rect.top - self.bounce
            self.next_update_time = current_time + 10

    def bounce(self):
        self.bounce = 5

class Character(AnimateImageBox):

    def __init__(self, image_file, initial_position, xvelocity = 0,
    bounce = False):
        AnimateImageBox.__init__(self, image_file, initial_position)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.yvelocity = 1
        self.bounce = bounce
        self.xvelocity = xvelocity
        self.next_update_time = 0 # update() hasn't been called yet.
        self.static = False
        self._old_top = 0
        self.character = True
        self.animate_delay = 75

    def update(self, current_time):
        AnimateImageBox.update(self, current_time)
        # Update every 10 milliseconds = 1/100th of a second.
        if self.next_update_time < current_time:

            # X velocity doesn't rely on gravity
            if self.xvelocity != 0:
                self.rect.right = self.rect.right + self.xvelocity
                if self.xvelocity > 0:
                    self.face_right = True
                else:
                    self.face_right = False

            # Gravity
            if self.yvelocity < 10:
                self.yvelocity = self.yvelocity + 1

            # See if we're falling
            if self.rect.top != self._old_top:
                self.static = False
                self._old_top = self.rect.top

            self.rect.top = self.rect.top + self.yvelocity

            self.next_update_time = current_time + 10

    def jump(self, start = True):
        # Jump
        if start:
            if self.static:
                self.yvelocity = -20
                self.static = False
        # Stop jumping
        else:
            if self.yvelocity < 0:
                self.yvelocity = 0

    def collide(self, other_character = None):
        if other_character:
            print "Dead"
        if self.bounce:
            self.xvelocity = self.xvelocity * -1
