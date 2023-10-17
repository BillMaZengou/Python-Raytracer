from ..utils.constants import *
from ..utils.vector3 import vec3
import numpy as np

class Primitive:    
    def __init__(self, center, material, max_ray_depth=1, shadow=True):
        self.center = center
        self.material = material
        self.material.assigned_primitive = self
        self.shadow = shadow
        self.collider_list = [] 
        self.max_ray_depth = max_ray_depth
        
    def rotate(self, theta, u):
        u = u.normalize()
        theta = np.deg2rad(theta)
        cos_val = np.cos(theta)
        sin_val = np.sqrt(1 - cos_val**2) * np.sign(theta)
        
        #rotation matrix along u axis
        M = np.array([
            [cos_val + u.x * u.x * (1 - cos_val),           u.x * u.y * (1 - cos_val) - u.z * sin_val,  u.x * u.z * (1 - cos_val) + u.y * sin_val],
            [u.y * u.x * (1 - cos_val) + u.z * sin_val,     cos_val + u.y * u.y * (1 - cos_val),        u.y * u.z * (1 - cos_val) - u.x * sin_val],
            [u.z * u.x * (1 - cos_val) - u.y * sin_val,     u.z * u.y * (1 - cos_val) + u.x * sin_val,  cos_val + u.z * u.z * (1 - cos_val)]
        ])
        
        for c in self.collider_list:
            c.rotate(M, self.center)
            
