import pygame
import random
from pygame.locals import *
from qtree import *
from settings import *


def main():
    pygame.init()
    sc = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock()

    boundary = Rectangle(0, 0, width, height)
    quadtree = Quadtree(boundary, 1)

    points = [Point(random.uniform(0, width), random.uniform(0, height))
              for _ in range(500)]
    for point in points:
        quadtree.insert(point)

    while True:
        sc.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                p = Point(mx, my)
                quadtree.insert(p)

        quadtree.draw(sc)
        quadtree.draw_points(sc)
        mx, my = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)

        range_a = Rectangle(mx-50, my-50, 150, 150)
        pygame.draw.rect(sc, (0, 255, 0), (range_a.x,
                         range_a.y, range_a.w, range_a.h), 1)
        found = quadtree.query(range_a)
        for f in found:
            pygame.draw.circle(sc, (0, 255, 0), (f.x, f.y), 3)
        print(len(found))
        pygame.display.flip()
        clock.tick()


if __name__ == '__main__':
    main()
