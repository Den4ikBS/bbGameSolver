from . import *

from pprint import pprint

g = Game(
    np.array([[1, 0, 1], [2, 1, 0], [1, 2, 3]])
)

log = g.solve(10000)

print(log[0], log[1])