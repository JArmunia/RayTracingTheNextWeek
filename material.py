from random import random, seed
from time import time_ns

import numpy as np
from math import sqrt, pow

from hitable import hit_record
from ray import Ray


def random_in_unit_sphere():
    norm = 2
    seed(time_ns())
    while (norm * norm) >= 1:
        p = 2.0 * np.array((random(), random(), random())) - np.array((1, 1, 1))
        norm = np.linalg.norm(p)
    return p


class material:
    def scatter(self, r_in: Ray, rec: hit_record):
        pass


class lambertian(material):
    def __init__(self, a: np.ndarray):
        self.albedo = a

    def scatter(self, r_in: Ray, rec: hit_record):
        target: np.ndarray = rec.p + rec.normal + random_in_unit_sphere()
        scattered = Ray(rec.p, target - rec.p)
        attenuation = self.albedo

        return True, attenuation, scattered


def reflect(v: np.ndarray, n: np.ndarray):
    return v - 2 * np.dot(v, n) * n


class metal(material):
    def __init__(self, a: np.ndarray, fuzz: float):
        self.albedo = a
        self.fuzz = fuzz

    def scatter(self, r_in: Ray, rec: hit_record):
        unit_direction = r_in.direction() / np.linalg.norm(r_in.direction())

        reflected: np.ndarray = reflect(unit_direction, rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())
        attenuation = self.albedo
        return (np.dot(scattered.direction(), rec.normal) > 0), attenuation, scattered


def refract(v: np.ndarray, n: np.ndarray, ni_over_nt: float):
    uv: np.ndarray = v / np.linalg.norm(v)
    dt = np.dot(uv, n)
    discriminant: float = 1.0 - ni_over_nt * ni_over_nt * (1 - dt * dt)
    if discriminant > 0:
        refracted = ni_over_nt * (uv - n * dt) - n * sqrt(discriminant)
        return True, refracted
    else:
        return False, None


def schlick(cosine: float, ref_idx: float):
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0) * pow((1 - cosine), 5)


class dielectric(material):
    def __init__(self, ri: float):
        self.ref_idx = ri

    def scatter(self, r_in: Ray, rec: hit_record):
        reflected: np.ndarray = reflect(r_in.direction(), rec.normal)
        attenuation = np.array((1, 1, 1), float)
        if np.dot(r_in.direction(), rec.normal) > 0:
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * np.dot(r_in.direction(), rec.normal) / np.linalg.norm(r_in.direction())

        else:
            outward_normal = rec.normal
            ni_over_nt = 1.0 / self.ref_idx
            cosine = -np.dot(r_in.direction(), rec.normal) / np.linalg.norm(r_in.direction())

        has_refracted, refracted = refract(r_in.direction(), outward_normal, ni_over_nt)
        if has_refracted:
            reflect_prob = schlick(cosine, self.ref_idx)

        else:
            reflect_prob = 1

        if random() < reflect_prob:
            scattered = Ray(rec.p, reflected)

        else:
            scattered = Ray(rec.p, refracted)

        return True, attenuation, scattered
