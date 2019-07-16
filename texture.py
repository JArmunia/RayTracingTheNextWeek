import numpy as np
from math import floor


class texture:
    def value(self, u: float, v: float, p: np.ndarray) -> np.ndarray:
        pass


class constant_texture(texture):
    def __init__(self, c: np.ndarray):
        self.color: np.ndarray = c

    def value(self, u: float, v: float, p: np.ndarray) -> np.ndarray:

        return self.color


class checker_texture(texture):
    def __init__(self, t0: texture, t1: texture):
        self.even = t0
        self.odd = t1

    def value(self, u: float, v: float, p: np.ndarray) -> np.ndarray:
        sines = np.sin(10 * p[0]) * np.sin(10 * p[1]) * np.sin(10 * p[2])

        if sines < 0:
            return self.odd.value(u, v, p)
        else:
            return self.even.value(u, v, p)


def perlin_generate_perm():
    return np.random.permutation(256)


def perlin_generate():
    vec = np.array((-1, -1, -1)) + (2 * np.random.random([256, 3]))
    norm = np.linalg.norm(vec, axis=1)

    ret = vec / norm[:, None]

    return ret


def trilinear_interp(c: np.ndarray, u: float, v: float, w: float):
    accum: float = 0.0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                accum += (i * u + (1 - i) * (1 - u)) * \
                         (j * v + (1 - j) * (1 - v)) * \
                         (k * w + (1 - k) * (1 - w)) * c[i, j, k]

    return accum


def perlin_interp(c: np.ndarray, u: float, v: float, w: float):
    uu = u * u * (3 - 2 * u)
    vv = v * v * (3 - 2 * v)
    ww = w * w * (3 - 2 * w)

    accum = 0

    for i in range(2):
        for j in range(2):
            for k in range(2):
                weight_v = np.array((u - i, v - j, w - k), float)
                accum += (i * uu + (1 - i) * (1 - uu)) * \
                         (j * vv + (1 - j) * (1 - vv)) * \
                         (k * ww + (1 - k) * (1 - ww)) * np.dot(c[:, i, j, k], weight_v)

    return accum


class perlin:
    def __init__(self):
        self.ranfloat = perlin_generate()
        self.perm_x = perlin_generate_perm()
        self.perm_y = perlin_generate_perm()
        self.perm_z = perlin_generate_perm()

    def noise(self, p: np.ndarray):
        u = p[0] - floor(p[0])
        v = p[1] - floor(p[1])
        w = p[2] - floor(p[2])
        i = floor(p[0])
        j = floor(p[1])
        k = floor(p[2])
        c: np.ndarray = np.zeros([3, 2, 2, 2], float)
        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    x = self.perm_x[(i + di) & 255] ^ \
                        self.perm_y[(j + dj) & 255] ^ \
                        self.perm_z[(k + dk) & 255]

                    c[:, di, dj, dk] = self.ranfloat[x]

        return perlin_interp(c, u, v, w)

    def turb(self, p: np.ndarray, depth: int = 7):
        accum: float = 0
        temp_p: np.ndarray = p
        weight: float = 1.0
        for i in range(depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p *= 2
        return np.abs(accum)


class noise_texture(texture):
    def __init__(self, scale: float = 1):
        self.noise = perlin()
        self.scale = scale

    def value(self, u: float, v: float, p: np.ndarray) -> np.ndarray:
        # return np.array((1, 1, 1), float) * self.noise.noise(p * self.scale)
        #print("u: {} v: {} p {}".format(u, v, p))
        ret = np.array((1, 1, 1)) * 0.5 * (1 + np.sin(self.scale * p[2] + 10 * self.noise.turb(p)))
        #print("noise: " + str(ret))
        return ret
