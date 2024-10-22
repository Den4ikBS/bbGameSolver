from . import *

from pprint import pprint

# TODO: gui for interacting with games
# TODO: file format to store matrices/logs/tables/strategies/program state/`Game` objects
# TODO: game creator gui
# TODO: game visualizer gui (show mtx and strats in a single info graphic)
# TODO: game simulation (human/human computer/computer computer aided gaming/something)

# next phase
# TODO: figure out a way to handle contiguous games

def duel(n):
    def f(i, j):
        if i == j:
            return 0.0
        elif i < j:
            return (i + 1) / n - (1 - (i + 1) / n) * (j + 1) / n
        else:
            return (1 - (j + 1) / n) * (i + 1) / n - (j + 1) / n
    return f

n = 6
g = DGame.from_func(duel(n), n, n)
print(g.mtx * n ** 2)
log = g.solve(10000)
print(log[0].round(2), log[1].round(2))

