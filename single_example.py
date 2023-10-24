from sightpy import *

# Set Scene 
Sc = Scene(ambient_color=rgb(0., 0., 0.))
Sc.add_Camera(
	screen_width=400, screen_height=600, 
	look_from=vec3(278, 278, 800), look_at=vec3(278, 278, 0), 
	focal_distance=1., field_of_view=35
)
angle = -0
# Sc.add_DirectionalLight(Ldir=vec3(-1.0, -0.5, -0.5), color=rgb(15., 15., 15.))

# define materials to use
gold_metal = Glossy(diff_color=rgb(1., .572, .184), n=vec3(0.15 + 3.58j, 0.4 + 2.37j, 1.54 + 1.91j), roughness=0.0, spec_coeff=0.2, diff_coeff=0.8)
red_diffuse = Diffuse(diff_color=rgb(.65, .05, .05))
white_diffuse = Diffuse(diff_color=rgb(.73, .73, .73))
emissive_white = Emissive(color=rgb(15., 15., 15.))
green_glass = Refractive(n=vec3(1.5 + 4e-8j, 1.5 + 0.j, 1.5 + 4e-8j))
soap_bubble = ThinFilmInterference(thickness=330, noise=60.)

Sc.add( # this is the light
	Plane(
		material=emissive_white, center=vec3(213 + 130. / 2., 554, -227.0 - 105. / 2.), 
  		width=130.0, height=105.0, 
    	u_axis=vec3(1.0, 0, 0), v_axis=vec3(0.0, 0.0, 1.0)
 	), 
	importance_sampled=True
)
Sc.add( # Left
	Plane(
		material=red_diffuse, center=vec3(50.0, 555.0 / 2.0, -555.0 / 2.0), 
  		width=555.0, height=555.0,
    	u_axis=vec3(0.0, 1.0, 0.0), v_axis=vec3(0.0, 0.0, -1.0)
	)
)
# Sc.add( # Right
# 	Plane(
# 		material=red_diffuse, center=vec3(555.0, 555.0 / 2.0, -555.0 / 2.0), 
#   		width=555.0, height=555.0,
#     	u_axis=vec3(0.0, 1.0, 0.0), v_axis=vec3(0.0, 0.0, -1.0)
# 	)
# )
Sc.add( # Top
	Plane(
		material=white_diffuse, center=vec3(555.0 / 2.0, 555.0, -555.0 / 2.0), 
  		width=555.0, height=555.0,
    	u_axis=vec3(1.0, 0.0, 0.0), v_axis=vec3(0.0, 0.0, -1.0)
	)
)
Sc.add( # Bottom
	Plane(
		material=gold_metal, center=vec3(555.0 / 2.0, 0.0, -555.0 / 2.0), 
  		width=555.0, height=555.0,
    	u_axis=vec3(1.0, 0.0, 0.0), v_axis=vec3(0.0, 0.0, -1.0)
	)
)

Sc.add(
	Sphere(
		material=green_glass, center=vec3(370.5, 165. / 2., -65. - 185. / 2.), radius=165. / 2., 
  		shadow=True, max_ray_depth=5
	),
	importance_sampled=True
)

cb = Cuboid(
	material=white_diffuse, center=vec3(182.5, 165.0, -285.0 - 160.0 / 2.0), 
 	width=165.0, height=165. * 2., length=165., shadow=True
)
cb.rotate(theta=15, u=vec3(0, 1, 0))
Sc.add(cb)

Sc.add(
    Sphere(material=soap_bubble, center=vec3(235., 165.0 * 2. / 3., 1.5), radius=165. / 3., shadow=False, max_ray_depth=5)
)

Sc.add_Background("lake.png", light_intensity=5., blur=1.)
# Render 
img = Sc.render(samples_per_pixel=10, progress_bar=True)
# you are going to need more than 10 samples to remove the noise. At least 1000 for a nice image.
img.save("cornell_box.png")
# img.show()