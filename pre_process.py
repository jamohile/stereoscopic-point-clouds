from PIL import Image, ImageFilter
import numpy as np

from config import THRESHOLD_COLOR_REGION_RELATION

# Breaks a picture into contiguous regions.
def get_region_map(image):
    # Output array where each element has a region. 0 indicates no region (yet)
    regions = np.zeros(image.shape)

    num_regions = 0

    # Check similarity between a given pixel and the pixel to the i_row, i_col direction of it. (e.g 1, 1)
    def check_direction(row, col, i_row, i_col, regionCounter):
        if abs(image[row, col] - image[row+i_row, col+i_col]) < THRESHOLD_COLOR_REGION_RELATION:
            # Region of target pixel.
            centerRegion = regions[row, col]
            # Region of other pixel.
            checkedRegion = regions[row+i_row, col+i_col]

            # If one of these has a region, and the other doesn't, assign that region.
            # If neither has a region, create a region and assign it to both.
            # Otherwise ignore, doesn't really matter.

            if centerRegion == 0:
                if checkedRegion == 0:
                    regions[row, col] = regionCounter + 1
                    regions[row+i_row, col+i_col] = regionCounter + 1
                    return regionCounter + 1
                else:
                    regions[row, col] = checkedRegion
            else:
                if checkedRegion == 0:
                    regions[row+i_row, col+i_col] = centerRegion
        # have to do it this way cause Python scopes are messed.
        return regionCounter
                    

    # Go through and DFT every pixel. (Not DFT but has the same effect.)
    for row in range(1, image.shape[0] - 1):
        for col in range(1, image.shape[1] -1):
            for row_i in range(-1, 2):
                for col_i in range(-1, 2):
                    num_regions = check_direction(row, col, row_i, col_i, num_regions)
    return regions


            


