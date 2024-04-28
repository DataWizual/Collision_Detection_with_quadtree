import random
import pygame
import numpy as np
from settings import *


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.r = 2
        self.particle = pygame.Surface((10, 10))
        self.rect = self.particle.get_rect()
        self.highlight = False
        self.speed = 4
        self.angle = random.uniform(np.pi/2, 1.25*np.pi)

    def intersects(self, other):
        return other.rect.colliderect(self.rect)

    def set_highlight(self, value):
        self.highlight = value

    def move(self):
        # self.speedx, self.speedy = self.speed * \
        #     np.cos(self.angle), -self.speed *\
        #     np.sin(self.angle)
        # self.x += self.speedx
        # self.y += self.speedy
        # self.wrap_around()
        self.x += random.randint(-4, 4)
        self.y += random.randint(-4, 4)

    def wrap_around(self):
        if self.x < 5:
            angel_d = self.angle_direction(-0.25, 0.25)
            self.angle += angel_d * 0.1
        elif self.x >= width-5:
            angel_d = self.angle_direction(0.75, 1.25)
            self.angle += angel_d * 0.1
        elif self.y < 5:
            angel_d = self.angle_direction(1.25, 1.75)
            self.angle += angel_d * 0.1
        elif self.y >= height-5:
            angel_d = self.angle_direction(0.25, 0.75)
            self.angle += angel_d * 0.1

    def angle_direction(self, start, end):
        angle_dir = random.uniform(start * np.pi, end * np.pi)
        angle_diff = (angle_dir - self.angle +
                      np.pi) % (2 * np.pi) - np.pi
        return angle_diff

    def render(self, screen):
        if self.highlight:
            pygame.draw.circle(self.particle, (0, 255, 0),
                               (5, 5), self.r)
        else:
            pygame.draw.circle(self.particle, (0, 0, 255),
                               (5, 5), self.r)
        screen.blit(self.particle, self.rect)
        self.rect.center = (self.x, self.y)
