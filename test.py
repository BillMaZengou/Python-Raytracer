from sightpy import *

# Set Scene 
Sc = Scene(ambient_color=rgb(0., 0., 0.))
Sc.add_Camera(
	screen_width=400, screen_height=400, 
	look_from=vec3(0, 10, 10), look_at=vec3(0, 0, 0), 
	focal_distance=1., field_of_view=90
)
Sc.add_DirectionalLight(Ldir=vec3(-1.0, -0.5, -0.5), color=rgb(15., 15., 15.))
Sc.add_DirectionalLight(Ldir=vec3(1.0, 0.5, -0.5), color=rgb(30., 15., 15.))
white_diffuse = Diffuse(diff_color=rgb(.73, .73, .73))
Sc.add(
    Sphere(material=white_diffuse, center=vec3(0., 0., -5.), radius=3., shadow=False, max_ray_depth=5)
)
# Render 
img = Sc.render(samples_per_pixel=3, progress_bar=False)
img.save("test.png")