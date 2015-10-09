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

class BlockPuzzle(object):
    def __init__(self, n, xs=None):
        """Create an nn block puzzle

        Use XS to initialize to a specific state.
        """
        self.n = n
        self.n2 = n * n
        if xs is None:
            self.xs = [(x + 1) % self.n2 for x in xrange(self.n2)]
        else:
            self.xs = list(xs)
        self.hsh = None
        self.last_move = []

    def __hash__(self):
        if self.hsh is None:
            self.hsh = hash(tuple(self.xs))
        return self.hsh

    def __repr__(self):
        return "BlockPuzzle(%d, %s)" % (self.n, self.xs)

    def show(self):
        ys = ["%2d" % x for x in self.xs]
        xs = [" ".join(ys[kk:kk+self.n]) for kk in xrange(0,self.n2, self.n)]
        return "\n".join(xs)

    def __eq__(self, other):
        return self.xs == other.xs

    def copy(self):
        return BlockPuzzle(self.n, self.xs)

    def get_moves(self):
        # Find the 0 tile, and then generate any moves we
        # can by sliding another block into its place.
        tile0 = self.xs.index(0)
        def swap(i):
            j = tile0
            tmp = list(self.xs)
            last_move = tmp[i]
            tmp[i], tmp[j] = tmp[j], tmp[i]
            result = BlockPuzzle(self.n, tmp)
            result.last_move = last_move
            return result

        if tile0 - self.n >= 0:
            yield swap(tile0-self.n)
        if tile0 +self.n < self.n2:
            yield swap(tile0+self.n)
        if tile0 % self.n > 0:
            yield swap(tile0-1)
        if tile0 % self.n < self.n-1:
            yield swap(tile0+1)

def shuffle(position, n):
    for kk in xrange(n):
        xs = list(position.get_moves())
        position = random.choice(xs)
    return position

def build_path(start, finish, parent):
    """
    Reconstruct the path from start to finish given
    a dict of parent links.

    """
    x = finish
    xs = [x]
    while x != start:
        x = parent[x]
        xs.append(x)
    xs.reverse()
    return xs

def misplaced_h(position):
    """Returns the number of tiles out of place."""
    n2 = position.n2
    c = 0
    for kk in xrange(n2):
        if position.xs[kk] != kk+1:
            c += 1
    return c


def test_block_8_misplaced(num_tests):
    for kk in xrange(num_tests):
        p = shuffle(BlockPuzzle(3), 200)
        print (p.show())
        solve(p, BlockPuzzle(3), misplaced_h)

#test_block_8_misplaced(1)

 