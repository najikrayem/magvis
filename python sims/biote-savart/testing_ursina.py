from ursina import *

from panda3d.core import ConfigVariableInt

#ConfigVariableInt('win-size', '800 600')  # Reduce resolution
ConfigVariableInt('framebuffer-multisample', 0)  # Disable anti-aliasing
ConfigVariableInt('multisamples', 0)

app = Ursina(development_mode=True)

# Set the background color to white
window.color = color.white




class CombinedCubes(Entity):
    def __init__(self, mag_field, **kwargs):
        super().__init__()

        self.cubes = []

        space_dim = len(mag_field)
        half_space_dim = space_dim // 2

        # Create a cube for each point in the cube
        for i in range(space_dim):
            for j in range(space_dim):
                for k in range(space_dim):
                    # Calculate the color of the cube based on the magnetic field at that point
                    c = color.rgba(0, 0, 0, mag_field[i][j][k])
                    # Create the particle
                    particle = Entity(model='cube', color=c, scale=1, parent=self, x=i - half_space_dim, y=j - half_space_dim, z=k - half_space_dim)
                    self.cubes.append(particle)


# Create a random 10x10x10 cube of magnetic field values
n = 15
new_cube = [[[random.uniform(0, 0.1) for _ in range(n)] for _ in range(n)] for _ in range(n)]

cube = CombinedCubes(mag_field=new_cube)

# Set up camera to orbit around the center.
camera = EditorCamera(rotation_speed=500, rotate_key='left mouse', zoom_smoothing=1, rotation_smoothing=0)

# Reduce update rate
camera.update_rate = 1/30  # Lower update frequency to 30 FPS
# Reduce clipping planes
camera.fov = 75  # Lower field of view
camera.near_clip = 0.1  # Adjust near clipping
camera.far_clip = 100  # Adjust far clipping for better performance

window.fps_counter.enabled = True
window.vsync = False  # Disable VSync for higher FPS
application.target_fps = 30  # Set a reasonable FPS cap


app.run()
