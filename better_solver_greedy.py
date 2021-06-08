#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def cross_check(pt1, pt2, pt3, pt4):
    x1,y1 = pt1
    x2,y2 = pt2
    x3,y3 = pt3
    x4,y4 = pt4

    ta = (x3 - x4) * (y1 - y3) + (y3 - y4) * (x3 - x1)
    tb = (x3 - x4) * (y2 - y3) + (y3 - y4) * (x3 - x2)
    tc = (x1 - x2) * (y3 - y1) + (y1 - y2) * (x1 - x3)
    td = (x1 - x2) * (y4 - y1) + (y1 - y2) * (x1 - x4)
    # Trueが交差、Falseが交差してない
    return (tc * td < 0) & (ta * tb < 0)

def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        if  len(tour)>1:
            for i in range(len(tour)-1):
                if cross_check(cities[tour[i]],cities[tour[i+1]],cities[tour[-1]],cities[next_city]):
                    tour_before = tour[:i]
                    tour_after = tour[i:]
                    for i in range(len(tour_after)):
                        tour_before.append(tour_after[-1-i])
                    tour = tour_before
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    next_city = tour[0]
    for i in range(len(tour)-1):
        if cross_check(cities[tour[i]],cities[tour[i+1]],cities[tour[-1]],cities[next_city]):
            tour_before = tour[:i]
            tour_after = tour[i:]
            for i in range(len(tour_after)):
                tour_before.append(tour_after[-1-i])
            tour = tour_before
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    with open('output_'+sys.argv[1].split('.')[-1][-1]+'.csv', mode='a') as f:
        f.write('index\n')
        for t in tour:
            f.write(str(t)+'\n')
