from random import seed, random
from time import time_ns

import numpy as np

from ray import Ray


def random_in_unit_disk():
    seed(time_ns)
    p = 2.0 * np.array((random(), random(), 0), float) - np.array((1, 1, 0), float)

    while np.dot(p, p) >= 1:
        p = 2.0 * np.array((random(), random(), 0), float) - np.array((1, 1, 0), float)

    return p


class Camera:
    def __init__(self, lookfrom: np.ndarray, lookat: np.ndarray, vup: np.ndarray, vfov: float, aspect: float,
                 aperture: float, focus_dist: float):
        theta = vfov * np.pi / 180
        half_height = np.tan(theta / 2)
        half_width = aspect * half_height

        self.lens_radius = aperture / 2
        self.origin = lookfrom
        w = (lookfrom - lookat) / np.linalg.norm(lookfrom - lookat)
        u = np.cross(vup, w) / np.linalg.norm(np.cross(vup, w))
        v = np.cross(w, u)
        self.lower_left_corner = self.origin - half_width * focus_dist * u - half_height * focus_dist * v - focus_dist * w
        self.horizontal = 2 * half_width * focus_dist * u
        self.vertical = 2 * half_height * focus_dist * v

    def get_ray(self, u: float, v: float) -> Ray:
        rd = self.lens_radius * random_in_unit_disk();
        offset = u * rd[0] + v * rd[1]
        return Ray(self.origin + offset,
                   self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin - offset)
