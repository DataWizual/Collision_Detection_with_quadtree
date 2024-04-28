import pygame
from settings import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (self.x <= point.x and
                self.x + self.w > point.x and
                self.y <= point.y and
                self.y + self.h > point.y)

    def intersect(self, range):
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)


class Quadtree:
    def __init__(self, boundary, n):
        self.boundary = boundary
        self.capacity = n
        self.points = []
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        ne = Rectangle(x + w/2, y, w/2, h/2)
        self.northeast = Quadtree(ne, self.capacity)
        nw = Rectangle(x, y, w/2, h/2)
        self.northwest = Quadtree(nw, self.capacity)
        se = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.southeast = Quadtree(se, self.capacity)
        sw = Rectangle(x, y + h/2, w/2, h/2)
        self.southwest = Quadtree(sw, self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return

        if not self.divided:
            if len(self.points) < self.capacity:
                self.points.append(point)
            else:
                self.subdivide()
                self.points.append(point)
                for pnt in self.points:
                    self.northeast.insert(pnt)
                    self.northwest.insert(pnt)
                    self.southeast.insert(pnt)
                    self.southwest.insert(pnt)
                self.points = []
        else:
            self.northeast.insert(point)
            self.northwest.insert(point)
            self.southeast.insert(point)
            self.southwest.insert(point)

    def query(self, range, found=None):
        if found is None:
            found = []
        if not self.boundary.intersect(range):
            return
        else:
            for p in self.points:
                if range.contains(p):
                    found.append(p)
        if self.divided:
            self.northeast.query(range, found)
            self.northwest.query(range, found)
            self.southeast.query(range, found)
            self.southwest.query(range, found)
            return found

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.boundary.x,
                         self.boundary.y, self.boundary.w, self.boundary.h), 1)

        if self.divided:
            self.northeast.draw(screen)
            self.northwest.draw(screen)
            self.southeast.draw(screen)
            self.southwest.draw(screen)

    def draw_points(self, screen):
        if self.divided:
            self.northeast.draw_points(screen)
            self.northwest.draw_points(screen)
            self.southeast.draw_points(screen)
            self.southwest.draw_points(screen)
        else:
            for point in self.points:
                pygame.draw.circle(screen, (255, 0, 0), (point.x, point.y), 3)
