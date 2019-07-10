import hitable
from ray import Ray


class hitable_list(hitable.Hitable):
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
