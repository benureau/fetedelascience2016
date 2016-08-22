"""Transformation Matrix Library"""

class Transformation:

    def __init__(self):
        self.matrix = [[1, 0, 0],
                       [0, 1, 0],
                       [0, 0, 1]]

    @classmethod
    def dot(cls, A, B):
        """Matrix multiplication"""
        return [[sum(a * b for a, b in zip(A_row, B_col))
                 for B_col in zip(*B)] for A_row in A]

    def rotate(self, angle):
        """Add a rotation"""
        R = [[ cos(angle), sin(angle), 0],
             [-sin(angle), cos(angle), 0],
             [          0,          0, 1]]
        self.matrix = self.dot(self.matrix, R)
        return self

    def translate(self, tx, ty):
        """Add a translation"""
        T = [[1, 0, tx],
             [0, 1, ty],
             [0, 0,  1]]
        self.matrix = self.dot(self.matrix, T)
        return self

    def apply(self, x, y):
        c = self.dot(self.matrix, [[x], [y], [1]])
        return c[0][0], c[1][0]
