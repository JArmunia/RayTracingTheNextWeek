import sys
from random import random, seed
from time import time_ns

import numpy as np

from aabb import surrounding_box, aabb
from ray import Ray


class hit_record:
    def __init__(self, t: float, p: np.ndarray, normal: np.ndarray, material, u:float = 0, v:float = 0):
        self.t = t
        self.p = p
        self.normal = normal
        self.material = material
        self.u = u
        self.v = v

    def __str__(self):
        return "t: {} p: {} normal: {} material{}".format(self.t, self.p, self.normal, self.material)


class Hitable:
    def hit(self, r: Ray, t_min: float, t_max: float):
        pass

    def bounding_box(self, t0: float, t1: float):
        pass

    def box_x_compare(self):
        has_bound, box = self.bounding_box(0, 0)

        return box.min()[0]

    def box_y_compare(self):
        has_bound, box = self.bounding_box(0, 0)

        return box.min()[2]

    def box_z_compare(self):
        has_bound, box = self.bounding_box(0, 0)

        return box.min()[2]


class hitable_list(Hitable):
    def __init__(self, l: list):
        self.l = l

    def hit(self, r: Ray, t_min: float, t_max: float):
        hit_anything = False
        rec = None
        closest_so_far = t_max
        for element in self.l:
            has_hit, temp_rec = element.hit(r, t_min, closest_so_far)
            if has_hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything, rec

    def bounding_box(self, t0: float, t1: float):
        if len(self.l) > 1:
            return False, None
        first_true, temp_box = self.l[0].bounding_box(t0, t1)

        if not first_true:
            return False, None
        else:
            box = temp_box

        for i in range(1, len(self.l)):
            has_bound, temp_box = list[i].bounding_box(t0, t1)
            if has_bound:
                box = surrounding_box(box, temp_box)
            else:
                return False, None

        return True, box


class bvh_node(Hitable):

    def __init__(self, l: hitable_list, time0: float, time1: float):
        self.box: aabb = None
        self.left: Hitable = None
        self.right: Hitable = None

        seed(time_ns)
        axis = int(3 * random())

        if axis == 0:
            sorted(l.l, key=lambda hitable: hitable.box_x_compare())

        elif axis == 1:
            sorted(l.l, key=lambda hitable: hitable.box_y_compare())

        else:
            sorted(l.l, key=lambda hitable: hitable.box_z_compare())

        if len(l.l) == 1:
            self.left = l.l[0]
            self.right = l.l[0]
        elif len(l.l) == 2:
            self.left = l.l[0]
            self.right = l.l[1]

        else:
            self.left = bvh_node(hitable_list(l.l[0:int(len(l.l) / 2)]), time0, time1)
            self.right = bvh_node(hitable_list(l.l[int(len(l.l) / 2):len(l.l)]), time0, time1)

        has_bound_left, box_left = self.left.bounding_box(time0, time1)
        has_bound_right, box_right = self.right.bounding_box(time0, time1)

        if not has_bound_left or not has_bound_right:
            sys.stderr.write("No bounding box in bvh_node constructor\n")
        self.box = surrounding_box(box_left, box_right)

    def hit(self, r: Ray, t_min: float, t_max: float):
        if self.box.hit(r, t_min, t_max):
            hit_left, left_rec = self.left.hit(r, t_min, t_max)
            hit_right, right_rec = self.right.hit(r, t_min, t_max)
            if hit_left and hit_right:
                if left_rec.t < right_rec.t:
                    rec = left_rec
                else:
                    rec = right_rec

                return True, rec

            elif hit_left:
                rec = left_rec
                return True, rec

            elif hit_right:
                rec = right_rec
                return True, rec

            else:
                return False, None
        else:
            return False, None

    def bounding_box(self, t0: float, t1: float):
        return True, self.box
