import matplotlib.pyplot as plt
import random
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def random_points(n=100):
    points = []
    for i in range(n):
        points.append(Point(random.randint(0, 100), random.randint(0, 100)))
        # plt.scatter(points[i].x, points[i].y, color='b')
        plt.scatter(points[i].x, points[i].y)
    return points


def dist(pointA, pointB):
    return np.sqrt((pointA.x - pointB.x) ** 2 + (pointA.y - pointB.y) ** 2)


def make_first_centroids(points, n=5):
    pointCntr = Point(0, 0)  # center of the circle
    for i in range(len(points)):
        pointCntr.x += points[i].x
        pointCntr.y += points[i].y
    pointCntr.x /= len(points)
    pointCntr.y /= len(points)
    R = 0  # radius of the circle
    for i in range(len(points)):
        d = dist(points[i], pointCntr)
        if (d > R):
            R = d
    centroids = []
    for i in range(n):
        centroids.append(Point(R * np.cos(2 * np.pi * i / n) + pointCntr.x,
                               R * np.sin(2 * np.pi * i / n) + pointCntr.y))
        # plt.scatter(centroids[i].x, centroids[i].y, color = 'r')
        plt.scatter(centroids[i].x, centroids[i].y)
    return centroids


if __name__ == '__main__':
    points = random_points(200)
    make_first_centroids(points)
    plt.show()
