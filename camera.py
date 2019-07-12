from random import random

import numpy as np

from ray import Ray


def random_in_unit_disk():
    p = 2.0 * np.array((random(), random(), 0), float) - np.array((1, 1, 0), float)

    while np.dot(p, p) >= 1:
        p = 2.0 * np.array((random(), random(), 0), float) - np.array((1, 1, 0), float)

    return p


class Camera:
    def __init__(self, lookfrom: np.ndarray, lookat: np.ndarray, vup: np.ndarray, vfov: float, aspect: float,
                 aperture: float, focus_dist: float, t0: float, t1: float):
        self.time0 = t0
        self.time1 = t1
        self.lens_radius = aperture / 2
        theta = vfov * np.pi / 180
        half_height = np.tan(theta / 2)
        half_width = aspect * half_height
        self.origin = lookfrom

        lf_la = lookfrom - lookat
        self.w = lf_la / np.linalg.norm(lf_la)

        cr_vu_w = np.cross(vup, self.w)
        self.u = cr_vu_w / np.linalg.norm(cr_vu_w)

        self.v = np.cross(self.w, self.u)

        self.lower_left_corner = self.origin - \
                                 half_width * focus_dist * self.u - \
                                 half_height * focus_dist * self.v - \
                                 focus_dist * self.w

        self.horizontal = 2 * half_width * focus_dist * self.u
        self.vertical = 2 * half_height * focus_dist * self.v

    def get_ray(self, s: float, t: float):
        rd: np.ndarray = self.lens_radius * random_in_unit_disk()
        offset: np.ndarray = self.u * rd[0] + self.v * rd[1]
        time = self.time0 + random() * (self.time1 - self.time0)
        return Ray(self.origin + offset,
                   self.lower_left_corner +
                   s * self.horizontal +
                   t * self.vertical
                   - self.origin - offset, time)
