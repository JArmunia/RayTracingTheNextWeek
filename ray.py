import numpy as np


class Ray:

    def __init__(self, A: np.ndarray, B: np.ndarray, ti: float):
        self.A: np.ndarray = A
        self.B: np.ndarray = B
        self.t: float = ti

    def __str__(self):
        return "A = {} B = {}".format(self.A, self.B)

    def origin(self):
        return self.A

    def direction(self):
        return self.B

    def point_at_parameter(self, t: float):
        return self.A + (t * self.B)

    def time(self):
        return self.t
