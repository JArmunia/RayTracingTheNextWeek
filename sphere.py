import numpy as np
from math import sqrt

import material
from hitable import hit_record, Hitable
from ray import Ray


class Sphere(Hitable):
    def __init__(self, center: np.ndarray, radius: float, m: material.material):
        self.center = center
        self.radius = radius
        self.material = m

    def hit(self, r: Ray, t_min: float, t_max: float):
        oc = r.origin() - self.center
        a = np.dot(r.direction(), r.direction())
        b = np.dot(oc, r.direction())
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - a * c

        if discriminant > 0:
            temp = (-b - sqrt(b * b - a * c)) / a
            if (temp < t_max) and (temp > t_min):
                t = temp
                p = r.point_at_parameter(t)
                normal = (p - self.center) / self.radius
                rec = hit_record(t, p, normal, self.material)
                return True, rec

            temp = (-b + sqrt(b * b - a * c)) / a
            if (temp < t_max) and (temp > t_min):
                t = temp
                p = r.point_at_parameter(t)
                normal = (p - self.center) / self.radius
                rec = hit_record(t, p, normal, self.material)
                return True, rec

        return False, None
