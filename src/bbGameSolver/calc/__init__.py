import numpy as np
import pandas as pd

class DGame:
    """Решатель дискретных антагонистичеких игр"""
    log: np.ndarray
    mtx: np.ndarray
    def __init__(self, game_mtx):
        """Создание решателя, задание матрицы игры"""
        self.mtx = game_mtx
        self.log = None
    
    def solve(self, n=1000):
        """Генерация решения
        
        n: int:   число итераций.
        Возвращает пару стратегий
        """
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
        for i in range(A_moves):
            strat_a[i] = (self.log[:, 0].astype(int) == i).sum() / n
        for i in range(B_moves):
            strat_b[i] = (self.log[:, 1].astype(int) == i).sum() / n
        return strat_a, strat_b
    
    @classmethod
    def from_tsv(cls, csv_path):
        """Загрузка матрицы из файла"""
        return cls(pd.read_csv(csv_path, header=None, sep='\t').to_numpy())
    
    def to_tsv(self, csv_path):
        """Выгрузка матрицы в файл"""
        return pd.DataFrame(self.mtx).to_csv(csv_path, index=False, header=False, sep='\t')

    @classmethod
    def from_func(cls, func, N, M):
        """Генерация матрицы по платёжной функции"""
        mtx = np.fromiter((func(i, j) for i in range(N) for j in range(M)), float).reshape((N, M))
        return cls(mtx)
    
