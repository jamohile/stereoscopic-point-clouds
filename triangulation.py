from config import SCALE, BASELINE, FOCAL_PX, DOFFS , PRINCIPLE_Y, PRINCIPLE_X_A
import numpy as np


def get_distance_map(disparity_map):
    # Create empty array for distances.
    distances = np.zeros((*disparity_map.shape, 3))

    for row in range(disparity_map.shape[0]):
        for col in range(disparity_map.shape[1]):
            disparity_Px = disparity_map[row, col]

            # Calculate x and y centerline offset.
            YOffset_PX = ((disparity_map.shape[0] - row) * SCALE) - PRINCIPLE_Y
            XOffset_PX = ((disparity_map.shape[1] - col) * SCALE) - PRINCIPLE_X_A

            # Calculate world coordinates using pre-derived formulas (similar triangles)
            Z = (BASELINE * FOCAL_PX) / (disparity_Px + DOFFS)
            Y = (Z/FOCAL_PX) * YOffset_PX
            X = (Z/FOCAL_PX) * XOffset_PX

            distances[row, col] = [X, Y, Z]
    return distances
        



