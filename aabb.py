import numpy as np

from ray import Ray


def ffmin(a: float, b: float) -> float:
    return a if a < b else b


def ffmax(a: float, b: float) -> float:
    return a if a > b else b


class aabb:
    def __init__(self, a: np.ndarray, b: np.ndarray):
        self._min = a
        self._max = b

    def min(self):
        return self._min

    def max(self):
        return self._max

    def hit(self, r: Ray, tmin: float, tmax: float):
        for a in range(3):
            invD = 1.0 / r.direction()[a]

            t0 = (self._min[a] - r.origin()[a]) * invD

            t1 = (self._max[a] - r.origin()[a]) * invD

            if invD < 0.0:
                aux = t1
                t1 = t0
                t0 = aux

            tmin = t0 if t0 > tmin else tmin
            tmax = t1 if t1 < tmax else tmax

            if tmax <= tmin:
                return False

        return True


def surrounding_box(box0: aabb, box1: aabb) -> aabb:
    small: np.ndarray = np.array((min(box0.min()[0], box1.min()[0]),
                                  min(box0.min()[1], box1.min()[1]),
                                  min(box0.min()[2], box1.min()[2])))
    big: np.ndarray = np.array((max(box0.max()[0], box1.max()[0]),
                                max(box0.max()[1], box1.max()[1]),
                                max(box0.max()[2], box1.max()[2])))

    return aabb(small, big)
