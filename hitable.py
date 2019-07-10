import numpy as np

from ray import Ray


class hit_record:
    def __init__(self, t: float, p: np.ndarray, normal: np.ndarray, material):
        self.t = t
        self.p = p
        self.normal = normal
        self.material = material

    def __str__(self):
        return "t: {} p: {} normal: {} material{}".format(self.t, self.p, self.normal, self.material)


class Hitable:
    def hit(self, r: Ray, t_min: float, t_max: float):
        pass
