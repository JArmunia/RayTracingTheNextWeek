from distutils.core import setup
from distutils.extension import Extension

from Cython.Distutils import build_ext

ext_modules = [
    Extension("init", ["__init__.py"]),
    Extension("aabb", ["aabb.py"]),
    Extension("hitable", ["hitable.py"]),
    Extension("material", ["material.py"]),
    Extension("camera", ["camera.py"]),
    Extension("ray", ["ray.py"]),
    Extension("scenes", ["scenes.py"]),
    Extension("sphere", ["sphere.py"]),
    Extension("texture", ["texture.py"]),
    #   ... all your modules that need be compiled ...
]
setup(
    name='Render',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
