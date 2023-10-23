from ..utils.constants import *
from ..utils.vector3 import vec3
from functools import reduce as reduce 
from . import Material
from ..textures import *

class Emissive(Material):
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        if isinstance(color, vec3):
            self.texture_color = solid_color(color)
        elif isinstance(color, texture):
            self.texture_color = color

    def get_color(self, scene, ray, hit):
        diff_color = self.texture_color.get_color(hit)
        return diff_color