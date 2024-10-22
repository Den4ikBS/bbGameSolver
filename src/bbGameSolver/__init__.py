import numpy as np
import pandas as pd

class Game:
    log: np.ndarray
    mtx: np.ndarray
    def __init__(self, game_mtx):
        self.mtx = game_mtx
        self.log = None
    
    def solve(self, n=1000):
        # should return a pair of strats and optionally a calculation log
        self.log = np.zeros((n, sum(self.mtx.shape) + 2), float)
        B_moves = self.mtx.shape[0]
        A_moves = self.mtx.shape[1]
        self.log[0, :2] = 0
        self.log[0, 2:2+B_moves] = self.mtx[:, 0]
        self.log[0, 2+B_moves:] = - self.mtx[0]
        for i in range(1, n):
            score_a = self.log[i-1, 2:2+B_moves]
            score_b = self.log[i-1, 2+B_moves:]
            strat_a = score_a.argmax()
            strat_b = score_b.argmax()
            new_score_a = score_a + self.mtx[:, strat_b]
            new_score_b = score_b - self.mtx[strat_a]
            self.log[i, :2] = [strat_a, strat_b]
            self.log[i, 2:2+B_moves] = new_score_a
            self.log[i, 2+B_moves:] = new_score_b
        strat_a = np.zeros(A_moves)
        strat_b = np.zeros(B_moves)
        print(A_moves, B_moves)
        for i in range(A_moves):
            strat_a[i] = (self.log[:, 0].astype(int) == i).sum() / n
        for i in range(B_moves):
            strat_b[i] = (self.log[:, 1].astype(int) == i).sum() / n
        return strat_a, strat_b
    
    @classmethod
    def from_csv(cls, csv_path):
        pass

    @classmethod
    def from_func(cls, func):
        pass