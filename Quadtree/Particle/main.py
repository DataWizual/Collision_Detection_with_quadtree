import pygame
import random
from pygame.locals import *
from qtree import *
from settings import *
from particle import *


def initialize_particles(num_particles):
    particles = pygame.sprite.Group()
    for _ in range(num_particles):
        particles.add(Particle(random.randint(
            0, width), random.randint(0, height)))
    return particles


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    particles = initialize_particles(2000)

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        boundary = Rectangle(0, 0, width, height)
        quad_tree = Quadtree(boundary, 4)

        for particle in particles:
            # quad_tree.draw(screen)
            point_p = Point(particle.x, particle.y, particle)
            quad_tree.insert(point_p)
            particle.move()
            particle.render(screen)
            particle.set_highlight(False)
            range_area = Circle(
                particle.x, particle.y, particle.r*2, particle.r*2)
            found = quad_tree.query(range_area)
            if found:
                for f in found:
                    other_particle = f.userdata
                    if particle != other_particle and\
                            particle.intersects(other_particle):
                        particle.set_highlight(True)
                        other_particle.set_highlight(True)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
