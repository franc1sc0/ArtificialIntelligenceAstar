import heapq
import math
import random

def solve(start, finish, heuristic):
    """Find the shortest path from START to FINISH."""
    heap = []

    link = {} # parent node link
    h = {} # heuristic function cache
    g = {} # shortest path to a node

    g[start] = 0    #shortest path
    h[start] = 0    #estimated_distance
    link[start] = None


    heapq.heappush(heap, (0, 0, start))
    # keep a count of the  number of steps, and avoid an infinite loop.
    for kk in xrange(1000000):
        current = heapq.heappop(heap)
        if current == finish:
            print("distance:", g[current], "steps:", kk)
            return g[current], kk, build_path(start, finish, link)

        moves = current.get_moves()
        distance = g[current]
        for mv in moves:
            if mv not in g or g[mv] > distance + 1:
                g[mv] = distance + 1 #g[mv] holds the length of the shortest known path to mv
                if mv not in h:
                    h[mv] = heuristic(mv)   #h[mv] holds the estimated distance from mv...finish
                link[mv] = current
                # g[mv] + h[mv] current best estimate of the distance from start...finish
                heapq.heappush(heap, (g[mv] + h[mv], -kk, mv))
    else:
        raise Exception("did not find a solution")


 