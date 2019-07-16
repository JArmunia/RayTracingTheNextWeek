import material
import numpy as np
from aabb import aabb, surrounding_box
from hitable import hit_record, Hitable
from math import sqrt
from ray import Ray


def get_shpere_uv(p: np.ndarray):
    phi: float = np.arctan2(p[2], p[0])

    theta: float = np.arcsin(p[1])

    u = 1 - (phi + np.pi) / (2 * np.pi)
    v = (theta + np.pi / 2) / np.pi
    return u, v


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
                u, v = get_shpere_uv((p - self.center) / self.radius)
                rec = hit_record(t, p, normal, self.material, u, v)
                return True, rec

            temp = float((-b + sqrt(b * b - a * c)) / a)
            if (temp < t_max) and (temp > t_min):
                t = temp
                p = r.point_at_parameter(t)
                normal = (p - self.center) / self.radius
                u, v = get_shpere_uv((p - self.center) / self.radius)
                rec = hit_record(t, p, normal, self.material, u, v)
                return True, rec

        return False, None

    def bounding_box(self, t0: float, t1: float):
        box = aabb(self.center - np.array((self.radius, self.radius, self.radius)),
                   self.center + np.array((self.radius, self.radius, self.radius)))

        return True, box


class moving_sphere(Hitable):
    def __init__(self, cen0: np.ndarray, cen1: np.ndarray, t0: float, t1: float, r: float, m: material.material):
        self.center0: np.ndarray = cen0
        self.center1: np.ndarray = cen1
        self.time0: float = t0
        self.time1: float = t1
        self.radius: float = r
        self.material: material.material = m

    def center(self, time: float) -> np.ndarray:
        return self.center0 + ((time - self.time0) / (self.time1 - self.time0)) * (self.center1 - self.center0)

    def hit(self, r: Ray, t_min: float, t_max: float):
        oc = r.origin() - self.center(r.time())
        a = np.dot(r.direction(), r.direction())
        b = np.dot(oc, r.direction())
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - a * c

        if discriminant > 0:
            temp = (-b - sqrt(b * b - a * c)) / a
            if (temp < t_max) and (temp > t_min):
                t = float(temp)
                p = r.point_at_parameter(t)
                normal = (p - self.center(r.time())) / self.radius
                u, v = get_shpere_uv((p - self.center(r.time())) / self.radius)
                rec = hit_record(t, p, normal, self.material, u,v)
                return True, rec

            temp = (-b + sqrt(b * b - a * c)) / a
            if (temp < t_max) and (temp > t_min):
                t = float(temp)
                p = r.point_at_parameter(t)
                normal = (p - self.center(r.time())) / self.radius
                u, v = get_shpere_uv((p - self.center(r.time())) / self.radius)
                rec = hit_record(t, p, normal, self.material, u,v)
                return True, rec

        return False, None

    def bounding_box(self, t0: float, t1: float):
        box0 = aabb(self.center(self.time0) - np.array((self.radius, self.radius, self.radius)),
                    self.center(self.time0) + np.array((self.radius, self.radius, self.radius)))

        box1 = aabb(self.center(self.time1) - np.array((self.radius, self.radius, self.radius)),
                    self.center(self.time1) + np.array((self.radius, self.radius, self.radius)))

        total_box = surrounding_box(box0, box1)

        return True, total_box
