import numpy as np
import pandas as pd

class Game:
    def __init__(self, game_mtx):
        self.mtx = game_mtx
    
    def solve(self):
        # should return a pair of strats and optionally calculation log
        pass
    
    @classmethod
    def from_csv(cls, csv_path):
        pass

    @classmethod
    def from_func(cls, func):
        pass