#%%

import numpy as np
import logging
import tqdm
#import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants------------------------------------------------------------

# Permeability of free space in Tesla*meters/ampere
MU_0 = 4 * np.longdouble(np.pi) * 10 ** -7
MU_0_OVER_4PI = np.longdouble(10) ** -7

# log
logging.info(f"Permeability of free space: {MU_0}")
logging.debug(f"Type of mu_0: {type(MU_0)}")

# Data ----------------------------------------------------------------

# Array that stores the 3D points of wire. Current moves from
# the first point to the second, then to the third, and so on.
# Units are in millimeters.
#wire = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0], [5, 0, 0], [6, 0, 0], [7, 0, 0], [8, 0, 0], [9, 0, 0], [10, 0, 0]], dtype=np.longdouble)
wire = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]], dtype=np.longdouble)

# # create a straight wire that goes from (0, 0, 0) to (1000, 0, 0). must have 1000 individual 3D points.
# wire = np.zeros((1000, 3), dtype=np.longdouble)
# for i in range(1000):
#     wire[i, 0] = i
#     wire[i, 1] = 0
#     wire[i, 2] = 0

# Point in 3D space where we want to calculate the magnetic field. Units are in millimeters.
#r_obs = np.array([1, 1, 0], dtype=np.longdouble)

# Logic ---------------------------------------------------------------

# translate the wire such that all points are positive
min_x = np.min(wire[:, 0])
min_y = np.min(wire[:, 1])
min_z = np.min(wire[:, 2])
wire[:, 0] = wire[:, 0] - min_x
wire[:, 1] = wire[:, 1] - min_y
wire[:, 2] = wire[:, 2] - min_z

logging.debug(f"Wire location after translation: {wire}")

# %%

# Change the units of the wire shape from millimeters to meters.
wire = wire / 1000
#r_obs = r_obs / 1000

# Array that stores the 3D points of the magnetic field. 
# To determine the size of the 3D space, we calulate the
# width, height, and length of the wire shape and then
# we double the manimum which will be used as the
# dimensions of the cube.
# Units are in millimeters.
wire_width = np.max(wire[:, 0]) - np.min(wire[:, 0]) + 1/1000
wire_height = np.max(wire[:, 1]) - np.min(wire[:, 1]) + 1/1000
wire_length = np.max(wire[:, 2]) - np.min(wire[:, 2]) + 1/1000
max_wire_dim = np.max([wire_width, wire_height, wire_length])
cube_dim = int(2 * max_wire_dim * 1000)
if max_wire_dim % 2 != 0:
    cube_dim += 1

# Finally create the cube. Each point in the cube is a
# 3D vector that stores the magnetic field at that point.
cube = np.zeros((int(cube_dim), int(cube_dim), int(cube_dim), 3), dtype=np.longdouble)

#log
logging.info(f"Wire width: {wire_width}")
logging.info(f"Wire height: {wire_height}")
logging.info(f"Wire length: {wire_length}")
logging.info(f"Cube dimensions: {cube_dim}")
logging.debug(f"Cube: {cube}")

# Translate the wire shape to the center of the cube
wire = wire + (max_wire_dim / 2)


# Find the derivative of the wire shape, which is equivalent to
# the direction of the current at each point. We assume that the
# current flows in the direction of the wire shape, from the first
# point to the second, then to the third, and so on.
wire_diff = np.diff(wire, axis=0)

#log
logging.debug(f"Wire current elements: {wire_diff}")


def discrete_biot_savart(amp: np.longdouble, dl: np.ndarray, r_obs: np.ndarray, r_src: np.ndarray) -> np.ndarray:
    """
    Calculate the magnetic field at a point r_obs due to a current element dl at r_src.
    :param amp: The ampere value of the current element.
    :param dl: 3D vector that stores the current element. Unit is in meters.
    :param r_obs: 3D vector that stores the observation point, relative to the origin of the space. Unit is in meters.
    :param r_src: 3D vector that stores the source point, relative to the origin of the space. Unit is in meters.
    :return: 3D vector that stores the magnetic field at the observation point. Unit is in Tesla.
    """
    logging.debug(f"Calculating magnetic field at {r_obs} due to current {amp} element {dl} at {r_src}")

    # Change types to long double
    amp = np.longdouble(amp)
    dl = dl.astype(np.longdouble)
    r_obs = r_obs.astype(np.longdouble)
    r_src = r_src.astype(np.longdouble)

    # Vector from the source to the observation point
    r = r_obs - r_src

    logging.debug(f"Vector r: {r}")
    logging.debug(f"Vector r type: {r.dtype}")

    # Calculte the euclidean distance between the observation point and the source point. And its square.
    r_mag = np.linalg.norm(r)
    r_mag_sq = r_mag ** 2

    logging.debug(f"Distance r_mag: {r_mag}")
    logging.debug(f"Distance r_mag^2: {r_mag_sq}")

    # calculate the unit vector in the direction of r
    r_hat = r / r_mag

    logging.debug(f"Unit vector r_hat: {r_hat}")

    # Calculate the cross product dl x r_hat
    cross = np.cross(dl, r_hat)

    logging.debug(f"Cross product dl x r_hat: {cross}")

    # Calculate numerator
    # TODO factor out mu_0 for better performance and precision
    numerator = MU_0_OVER_4PI * amp * cross

    logging.debug(f"Numerator: {numerator}")

    # Calculate denominator
    denominator = r_mag_sq

    logging.debug(f"Denominator: {denominator}")

    # Calculate the magnetic field
    b = numerator / denominator

    logging.debug(f"Magnetic field: {b}")

    return b


# Main Script ---------------------------------------------------------

# Calculate the magnetic field at each point in the cube.
# The magnetic field is calculated by summing the magnetic
# fields of each current element in the wire shape.

I = 1  # Amperes

# Iterate over each point in the cube
for i in tqdm.tqdm(range(cube_dim)):
    for j in range(cube_dim):
        for k in range(cube_dim):
            # Calculate the magnetic field at the point (i, j, k)
            for n in range(len(wire) - 1):
                # Calculate the magnetic field at the point (i, j, k) due to the current element n
                b = discrete_biot_savart(I, wire_diff[n], np.array([i, j, k]), wire[n])
                cube[i, j, k] += b

logging.debug(f"Cube: {cube}")

# normalize values and convert to grey scale
new_cube = np.zeros((cube_dim, cube_dim, cube_dim), dtype=np.float32)
for i in range(cube_dim):
    for j in range(cube_dim):
        for k in range(cube_dim):
            new_cube[i, j, k] = np.linalg.norm(cube[i, j, k])

print(f"New Cube: {new_cube}")

# Replace all nans with 0
new_cube = np.nan_to_num(new_cube)

new_cube = new_cube / np.max(new_cube)

print(f"Cube: {new_cube}")

print(f"Cube max: {np.max(new_cube)}")

new_cube = new_cube / (cube_dim * cube_dim * cube_dim)

print(f"new Cube: {new_cube}")

# add black cubes where the wire is
for i in range(len(wire)):
    x = int(wire[i, 0] * 1000)
    y = int(wire[i, 1] * 1000)
    z = int(wire[i, 2] * 1000)
    new_cube[x, y, z] = 1
    print(f"Wire point: {x}, {y}, {z}")

print(f"new Cube: {new_cube}")

# # plot the z=0 plane of the cube
# plt.imshow(cube[:, :, 0], cmap='gray')
# plt.show()

                