import numpy as np


from config import SCALE, OFFSET, THRESHOLD_Z_RELATION

# Will smooth (dequantize) distances in the given array.
def get_smoothed(distance_map, region_map, clip_threshold):
    # Create a copy for output.
    smoothed_distances = np.copy(distance_map)
    # Iterate each pixel.
    for row in range(OFFSET, distance_map.shape[0]):
        for col in range(OFFSET, distance_map.shape[1]):
            # Keep track of a sum of surrounding pixel distances, and # of pixels included in average.
            num = 0
            s = 0

            # Z of the pixel being smoothed.
            Z = distance_map[row, col, 2]
            
            # Iterate through window of potential related pixels.
            for i in range(-1, 2):
                for j in range(-4, 5):
                    # Ignore current target pixel, it will be considered at end.
                    if i == 0 and j == 0:
                        continue
                    surrounding_pixel_row = row + i
                    surrounding_pixel_col = col + j
                    if 0 <= surrounding_pixel_row < distance_map.shape[0]:
                        if 0 <= surrounding_pixel_col < distance_map.shape[1]:
                            thisZ = distance_map[surrounding_pixel_row, surrounding_pixel_col][2]
                            # Ignore pixels in the 'garbage zone'
                            if thisZ > clip_threshold:
                                continue

                            # Evaluate relationship between pixels.
                            is_distance_related = abs(thisZ - Z) < THRESHOLD_Z_RELATION*SCALE
                            is_region_related = region_map[row, col] == region_map[surrounding_pixel_row, surrounding_pixel_col]

                            if (is_distance_related and is_region_related) or Z > clip_threshold :
                                num += 1
                                s += thisZ
                                
            # Compute average distance.
            # If original is decently close to this, include it in the average.
            avgZ = s/num if num != 0 else Z
            if abs(Z - avgZ)/avgZ < 0.1:
                avgZ = (num * avgZ + Z) / (num + 1)
            
            # Assign new value without mutating original array.
            smoothed_distances[row, col, 2] = [avgZ]
    return smoothed_distances

# Get rid of noisy outlier points that don't contribute to overall structure.
def get_denoised(distance_map):
    denoised_distances = np.copy(distance_map)
    for row in range(OFFSET, distance_map.shape[0] - OFFSET):
        for col in range(OFFSET, distance_map.shape[1] - OFFSET):
            Z = distance_map[row, col, 2]
            s = 0
            n = 0
            # Iterate window of surrounding pixels, compute average of Z-distances from current target.
            for i in range(-1, 1):
                for j in range(-1, 1):
                    if i == 0 and j == 0:
                        continue
                    n += 1
                    s += abs(Z - distance_map[row + i, col + j, 2])

            # If pixel has some threshold average distance, considered an outlier.
            avg = s/n
            if avg > 10:
                # This marks a pixel as 'deleted'. 
                denoised_distances[row, col, 2] = None
    return denoised_distances


def get_processed(distance_map, region_map, iterations):
    # We know that the edges are not processed, so there will be some garbage results there.
    # Filter them out.
    invalid_distance = distance_map[0, 0, 2]
    clip_threshold = 0.99 * invalid_distance

    result = None
    for i in range(0, iterations):
        target = result if not result is None else distance_map
        result = get_denoised(get_smoothed(target, region_map, clip_threshold=clip_threshold))
    return result