import random
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pygame
from numpy import random


def dist(pointA, pointB):
    return np.sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)


def near_points(point):
    count = random.randint(2, 5)
    points = []
    for i in range(count):
        x = random.randint(-20, 20)
        y = random.randint(-20, 20)
        points.append((point[0] + x, point[1] + y))
    return points


def draw_yellow_points(p, n, alone_points):
    if n not in alone_points:
        pygame.draw.circle(screen, color='yellow', center=p, radius=5)
        return
    pygame.draw.circle(screen, color='red', center=p, radius=5)



def iterate_for_neighbours(p, neighbours, alone_points):
    for n in neighbours:
        draw_yellow_points(p, n, alone_points)


def draw_red_points(p, neighbours, alone_points):
    if len(neighbours) == 0:
        pygame.draw.circle(screen, color='red', center=p, radius=5)
    else:
        iterate_for_neighbours(p, neighbours, alone_points)


def dbscan(points, distance, count_of_points, screen):
    alone = 0
    pointer = 0

    visited_points = set()
    clustered_points = set()
    clusters = {alone: []}

    def find_neighbours(p):
        return [q for q in points if dist(p, q) < distance]

    def add_cluster(p, neighbours):
        if pointer not in clusters:
            clusters[pointer] = []
        clusters[pointer].append(p)
        clustered_points.add(p)
        while neighbours:
            q = neighbours.pop()
            if q not in visited_points:
                visited_points.add(q)
                # plt.scatter(q[0], height - q[1], c='g')
                pygame.draw.circle(screen, color='green', center=q, radius=5)
                neighbours2 = find_neighbours(q)
                if len(neighbours2) > count_of_points:
                    neighbours.extend(neighbours2)
            if q not in clustered_points:
                clustered_points.add(q)
                clusters[pointer].append(q)
                if q in clusters[alone]:
                    clusters[alone].remove(q)

    for p in points:
        if p in visited_points:
            continue
        visited_points.add(p)
        neighbours = find_neighbours(p)
        if len(neighbours) < count_of_points:
            clusters[alone].append(p)
        else:
            pointer += 1
            add_cluster(p, neighbours)
            # plt.scatter(p[0], height - p[1], c='g')
            pygame.draw.circle(screen, color='green', center=p, radius=5)

    for p in clusters[alone]:
        neighbours = find_neighbours(p)
        draw_red_points(p, neighbours, clusters[alone])

    return clusters


if __name__ == '__main__':
    HEIGHT = 400
    pygame.init()
    screen = pygame.display.set_mode((600, HEIGHT))
    screen.fill(color="#FFFFFF")
    pygame.display.update()
    is_active = True
    is_pressed = False
    points = []
    while (is_active):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_pressed = True
                if event.button == 1:
                    is_pressed = True
                    coord = event.pos
                    points.append(coord)
                    pygame.draw.circle(screen, color='black', center=coord, radius=5)
            if event.type == pygame.MOUSEBUTTONUP:
                is_pressed = False
            if event.type == pygame.MOUSEMOTION:
                if is_pressed:
                    # if random.choice((0,10))==0:
                    # coord = event.pos
                    # pygame.draw.circle(screen, color='black', center=coord, radius=10)
                    if (dist(event.pos, points[-1]) > 20):
                        coord = event.pos
                        pygame.draw.circle(screen, color='black', center=coord, radius=5)
                        for nearP in near_points(coord):
                            pygame.draw.circle(screen, color='black', center=nearP, radius=5)
                            points.append(nearP)
                        points.append(coord)
            if event.type == pygame.KEYUP:
                if event.key == 13:
                    screen.fill(color="#FFFFFF")
                    clusters = dbscan(points, 50, 4, screen)
                    # for points in clusters.values():
                    # for point in points:
                    # pygame.draw.circle(screen, color='green', center=point, radius=5)
        pygame.display.update()

    # clusters = dbscan(points, 50, 4, HEIGHT)
    # for c, points in zip(cycle('bgrcmyk'), clusters.values()):
    #   X = [p[0] for p in points]
    #    Y = [HEIGHT - p[1] for p in points]
    #    plt.scatter(X, Y, c=c)
    # plt.show()
