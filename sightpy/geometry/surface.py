from ..utils.constants import *
from ..utils.vector3 import vec3
import numpy as np

class Surface:    
    def __init__(self, center, material, shadow=True):
        self.center = center
        self.material = material
        self.material.assigned_surface = self
        self.shadow = shadow
        self.collider_list = [] 
        
    def rotate(self, theta, u):
        u = u.normalize()
        theta = np.deg2rad(theta)
        costheta = np.cos(theta)
        sintheta = np.sqrt(1 - costheta**2) * np.sign(theta)
        
        #rotation matrix along u axis
        M = np.array([
            [costheta + u.x*u.x * (1-costheta),     u.x*u.y*(1-costheta) - u.z*sintheta,    u.x*u.z*(1-costheta) +u.y*sintheta],
            [u.y*u.x*(1-costheta) + u.z*sintheta,   costheta + u.y**2 * (1-costheta),       u.y*u.z*(1-costheta) -u.x*sintheta],
            [u.z*u.x*(1-costheta) -u.y*sintheta,    u.z*u.y*(1-costheta) + u.x*sintheta,    costheta + u.z*u.z*(1-costheta)]
        ])
        for c in self.collider_list:
            c.rotate(M, self.center)
            
