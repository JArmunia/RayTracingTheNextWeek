from random import random

import material
import numpy as np
from hitable import Hitable, hitable_list, xy_rect
from sphere import Sphere, moving_sphere
from texture import constant_texture, checker_texture, noise_texture


def random_scene():
    lista = list()
    lista.append(Sphere(np.array((0, -1000, 0)), 1000, material.lambertian(checker_texture(constant_texture(
        np.array((0.2, 0.3, 1))), constant_texture(np.array((0.9, 0.9, 0.9)))))))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center: np.ndarray = np.array((a + 0.9 * random(), 0.2, b + 0.9 * random()))
            if np.linalg.norm(center - np.array((4.0, 0.2, 0.0))) > 0.9:
                if choose_mat < 0.8:  # diffuse
                    lista.append(Sphere(center, 0.2, material.lambertian(constant_texture(
                        np.array((random() * random(), random() * random(), random() * random()))))))
                elif choose_mat < 0.95:  # metal
                    lista.append(Sphere(center, 0.2, material.metal(
                        np.array((0.5 * (1 + random()), 0.5 * (1 + random()), 0.5 * (1 + random()))), 0.5 * random())))

                else:
                    lista.append(Sphere(center, 0.2, material.dielectric(1.5)))

    lista.append(Sphere(np.array((0, 1, 0)), 1, material.dielectric(1.5)))
    lista.append(Sphere(np.array((-4, 1, 0)), 1, material.lambertian(constant_texture(np.array((0.4, 0.2, 0.1))))))
    lista.append(Sphere(np.array((4, 1, 0)), 1, material.metal(np.array((0.7, 0.6, 0.5)), 0.0)))

    return hitable_list(lista)


def two_spheres() -> Hitable:
    checker = checker_texture(constant_texture(np.array((0.2, 0.3, 0.1), float)),
                              constant_texture(np.array((0.9, 0.9, 0.9), float)))

    h_list = list()
    h_list.append(Sphere(np.array((0, -10, 0)), 10, material.lambertian(checker)))
    h_list.append(Sphere(np.array((0, 10, 0)), 10, material.lambertian(checker)))

    return hitable_list(h_list)


def two_perlin_spheres() -> Hitable:
    pertext = noise_texture(0.1)
    h_list = list()
    h_list.append(Sphere(np.array((0, -1000, 0)), 1000, material.lambertian(pertext)))
    h_list.append(Sphere(np.array((0, 2, 0)), 2, material.lambertian(pertext)))

    return hitable_list(h_list)


def simple_light():
    pertext = noise_texture(4)
    h_list = list()
    checker = checker_texture(constant_texture(np.array((0.2, 0.3, 0.1), float)),
                              constant_texture(np.array((0.9, 0.9, 0.9), float)))
    h_list.append(Sphere(np.array((0, -1000, 0)), 1000, material.lambertian(checker)))
    h_list.append(Sphere(np.array((0, 2, 0)), 2, material.lambertian(pertext)))
    h_list.append(Sphere(np.array((2, 2, -2)), 2, material.dielectric(1)))
    h_list.append(moving_sphere(np.array((-2, 2, 2)),np.array((-2, 2, 2)),0,1, 2, material.lambertian(pertext)))
    h_list.append(Sphere(np.array((0, 7, 0)), 2, material.diffuse_light(constant_texture(np.array((4, 4, 4))))))

    h_list.append(xy_rect(0, 50, 0, 30, -2, material.diffuse_light(constant_texture(np.array((4, 4, 4))))))

    return hitable_list(h_list)
