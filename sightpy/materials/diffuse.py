from ..utils.constants import *
from ..utils.vector3 import vec3, rgb, extract
from ..utils.random import spherical_caps_pdf, cosine_pdf, mixed_pdf
from functools import reduce as reduce 
from ..ray import Ray, get_raycolor
from .. import lights
import numpy as np
from . import Material
from ..textures import *

class Diffuse(Material):
    def __init__(self, diff_color, diffuse_rays=20, ambient_weight=0.5, **kwargs):
        super().__init__(**kwargs)
        if isinstance(diff_color, vec3):
            self.diff_texture = solid_color(diff_color)
        elif isinstance(diff_color, texture):
            self.diff_texture = diff_color
        self.diffuse_rays = diffuse_rays
        self.max_diffuse_reflections = 2
        self.ambient_weight = ambient_weight

    def get_color(self, scene, ray, hit):
        hit.point = (ray.origin + ray.dir * hit.distance) # intersection point
        # N = hit.material.get_Normal(hit)                  # normal 
        # print(N)
        N = self.get_Normal(hit)                  # normal 
        # print(N)
        diff_color = self.diff_texture.get_color(hit)
        color = rgb(0., 0., 0.)

        if ray.diffuse_reflections < 1:
            nudged = hit.point + N * .000001
            N_repeated = N.repeat(self.diffuse_rays)
            n_repeated = ray.n if ray.n.shape() == 1 else ray.n.repeat(self.diffuse_rays)
            nudged_repeated = nudged.repeat(self.diffuse_rays)
            # hit_repeated = hit.point.repeat(self.diffuse_rays)

            size = N.shape()[0] * self.diffuse_rays
            pdf1 = cosine_pdf(size, N_repeated)
            pdf2 = spherical_caps_pdf(size, nudged_repeated, scene.importance_sampled_list)
            s_pdf = pdf1 if len(scene.importance_sampled_list) < 1 else mixed_pdf(size, pdf1, pdf2, self.ambient_weight)

            ray_dir = s_pdf.generate()
            PDF_val = s_pdf.value(ray_dir)
            NdotL = np.clip(ray_dir.dot(N_repeated), 0., 1.)
            # TODO: light color?
            # color += diff_color / np.pi
            color_temp = get_raycolor(Ray(nudged_repeated, ray_dir, ray.depth + 1, n_repeated, ray.reflections + 1, ray.transmissions, ray.diffuse_reflections + 1), scene)
            color_temp = color_temp * NdotL / PDF_val / np.pi #  diff_color/np.pi = Lambertian BRDF
            color += diff_color * color_temp.reshape(N.shape()[0], self.diffuse_rays).mean(axis=1)
            # color += diff_color / np.pi
            # print(color)
        elif ray.diffuse_reflections < self.max_diffuse_reflections:
            """
            when ray.diffuse_reflections > 1 we just call one diffuse ray to solve rendering equation (otherwise is too slow)
            """
            nudged = hit.point + N * .000001
            size = N.shape()[0] 

            pdf1 = cosine_pdf(size, N)
            pdf2 = spherical_caps_pdf(size, nudged, scene.importance_sampled_list)
            s_pdf = cosine_pdf(size, N) if len(scene.importance_sampled_list) < 1 else mixed_pdf(size, pdf1, pdf2, self.ambient_weight)

            ray_dir = s_pdf.generate()
            PDF_val = s_pdf.value(ray_dir)

            NdotL = np.clip(N.dot(ray_dir), 0., 1.)
            color_temp = diff_color * get_raycolor(Ray(nudged, ray_dir, ray.depth + 1, ray.n, ray.reflections + 1, ray.transmissions, ray.diffuse_reflections + 1), scene)
            color = color_temp * NdotL  / PDF_val / np.pi
        return color
