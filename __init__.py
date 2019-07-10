import numpy as np
from ray import Ray
from math import pow
from hitable import Hitable, hit_record
from sphere import Sphere
from hitable_list import hitable_list
from camera import Camera
from random import random, seed
from time import time_ns
import material
import sys
from multiprocessing import Pool, cpu_count


def color(r: Ray, world: Hitable):
    has_hit, rec = world.hit(r, 0.001, np.inf)
    depth = 0
    scattered = r
    accumulate_attenuation = 1.
    while has_hit:

        has_scattered, attenuation, scattered = rec.material.scatter(r, rec)

        if (depth < 50) and has_scattered:
            has_hit, rec = world.hit(scattered, 0.001, np.inf)
            r = scattered
            depth += 1
            accumulate_attenuation *= attenuation
        else:

            return np.array((0, 0, 0))

    unit_direction = scattered.direction() / np.linalg.norm(scattered.direction())
    t = 0.5 * (unit_direction[1] + 1)
    return accumulate_attenuation * ((1.0 - t) * np.array((1., 1., 1.)) + t * np.array((.5, .7, 1.)))


# def color(r: Ray, world: Hitable):
#     has_hit, rec = world.hit(r, 0.001, np.inf)
#     depth = 0
#     attenuation = 1
#     while has_hit:
#
#         has_scattered, attenuation, scattered = rec.material.scatter(r, rec)
#         if (depth < 50) and has_scattered:
#             has_hit, rec = world.hit(scattered, 0.001, np.inf)
#             r = scattered
#         else:
#             return np.array((0, 0, 0))
#
#         depth += 1
#
#     direction = r.direction()
#     unit_direction = direction / np.linalg.norm(direction)
#     t = 0.5 * (unit_direction[1] + 1)
#     return np.power(attenuation, depth) * ((1 - t) * np.array((1, 1, 1), float) + t * np.array((0.5, 0.7, 1), float))
#
#
# def color(r: Ray, world: Hitable, depth: int):
#     has_hit, rec = world.hit(r, 0.001, np.inf)
#     if has_hit:
#         has_scattered, attenuation, scattered = rec.material.scatter(r, rec)
#         if (depth < 50) and has_scattered:
#             return attenuation * color(scattered, world, depth + 1)
#         else:
#             return np.array((0, 0, 0), float)
#
#     else:
#         direction = r.direction()
#         unit_direction = direction / np.linalg.norm(direction)
#         t = 0.5 * (unit_direction[1] + 1)
#         return (1 - t) * np.array((1, 1, 1), float) + t * np.array((0.5, 0.7, 1.0))


def random_scene():
    lista = list()
    lista.append(Sphere(np.array((0, -1000, 0)), 1000, material.lambertian(
        np.array((0.5, 0.5, 0.5)))))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random()
            center: np.ndarray = np.array((a + 0.9 * random(), 0.2, b + 0.9 * random()))
            if np.linalg.norm(center - np.array((4.0, 0.2, 0.0))) > 0.9:
                if choose_mat > 0.8:  # diffuse
                    lista.append(Sphere(center, 0.2, material.lambertian(
                        np.array((random() * random(), random() * random(), random() * random())))))
                elif choose_mat < 0.95:  # metal
                    lista.append(Sphere(center, 0.2, material.metal(
                        np.array((0.5 * (1 + random()), 0.5 * (1 + random()), 0.5 * (1 + random()))), 0.5 * random())))

                else:
                    lista.append(Sphere(center, 0.2, material.dielectric(1.5)))

    lista.append(Sphere(np.array((0, 1, 0)), 1, material.dielectric(1.5)))
    lista.append(Sphere(np.array((0, 1, 0)), 1, material.lambertian(np.array((0.4, 0.2, 0.1)))))
    lista.append(Sphere(np.array((0, 1, 0)), 1, material.metal(np.array((0.7, 0.6, 0.5)), 0.0)))

    return lista


def render(ny: float, nx: float, start: int, end: int, world, cam, img: dict):
    for j in range(start, end, -1):
        for i in range(0, nx):
            col = np.array((0, 0, 0), float)
            for s in range(0, ns):
                u = (i + random()) / nx
                v = (j + random()) / ny
                r = cam.get_ray(u, v)
                p = r.point_at_parameter(2)
                col += color(r, world)

            col = np.sqrt(col / ns) * 255.99
            ir = int(col[0])
            ig = int(col[1])
            ib = int(col[2])

            f.write("\n{} {} {}".format(ir, ig, ib))


if __name__ == '__main__':

    pool = Pool(cpu_count())
    args = sys.argv
    f = open(args[1], "w+")
    nx: int = int(args[2])
    ny: int = int(args[3])
    ns: int = int(args[4])

    f.write("P3\n{} {}\n255".format(nx, ny))

    lookfrom: np.ndarray = np.array((3, 3, 2))
    lookat: np.ndarray = np.array((0, 0, -1))
    dist_to_focus = np.linalg.norm(lookfrom - lookat)
    aperture = 2.0
    # cam = Camera(np.array((0, 0, 0)), np.array((0, 0, -1)), np.array((0, 1, 0)), 90, nx / ny)
    cam = Camera(lookfrom, lookat, np.array((0, 1, 0)), 20, float(nx) / float(ny), aperture, dist_to_focus)
    R = np.cos(np.pi / 4)

    h_list = list()
    # h_list.append(Sphere(np.array((-R, 0, -1)), R, material.lambertian(np.array((0., 0., 1.)))))
    # h_list.append(Sphere(np.array((R, 0, -1)), R, material.lambertian(np.array((1., 0., 0.)))))
    h_list.append(Sphere(np.array((0, 0, -1)), 0.5, material.lambertian(np.array((0.1, 0.2, 0.5)))))
    h_list.append(Sphere(np.array((0, -100.5, -1)), 100, material.lambertian(np.array((0.8, 0.8, 0)))))
    h_list.append(Sphere(np.array((1, 0, -1)), 0.5, material.metal(np.array((0.8, 0.6, 0.2)), 0.3)))
    h_list.append(Sphere(np.array((-1, 0, -1)), 0.5, material.dielectric(1.5)))
    # h_list.append(Sphere(np.array((-1, 0, -1)), -0.45, material.dielectric(1.5)))
    h_list.append(Sphere(np.array((-5, 2.5, -5)), 2, material.lambertian(np.array((0.1, 0.2, 0.5)))))
    world: Hitable = hitable_list(h_list)
    img = dict()
    seed(time_ns())
    t_init = time_ns()
    for j in range(ny, 0, -1):
        for i in range(0, nx):
            col = np.array((0, 0, 0), float)
            for s in range(0, ns):
                u = (i + random()) / nx
                v = (j + random()) / ny
                r = cam.get_ray(u, v)
                p = r.point_at_parameter(2)
                col += color(r, world)

            col = np.sqrt(col / ns) * 255.99
            ir = int(col[0])
            ig = int(col[1])
            ib = int(col[2])

            f.write("\n{} {} {}".format(ir, ig, ib))
        print("{}% ({}/{})".format(100 * (ny - j) / ny, ny - j, ny))

    t_end = time_ns()
    total = t_end - t_init
    print("Tiempo total: {}s".format(total * 10 ** -9))
