from PIL import Image, ImageFilter
import numpy as np


from config import SCALE, SET, OFFSET, ASSUMED_MAX_DISPARITY
from utils import getImgArr, get_slice


# Product sums and normalizes two windows, returns a correlation between 0 and 1.
def get_correlation(arr1, arr2):
    mArr1 = arr1 - np.average(arr1)
    mArr2 = arr2 - np.average(arr2)

    numerator = np.sum(np.multiply(mArr1, mArr2))
    denominator = (np.sum(mArr1**2) * np.sum(mArr2**2))**0.5

    return numerator / denominator

# Process a given left/right stereo image pair with a particular window size.
def get_disparity_map(left_img_arr, right_img_arr, edge_offset):
    # Create a new array to hold disparities.
    disparities = np.zeros((len(left_img_arr) - 2 * edge_offset, len(left_img_arr[0]) - 2 * edge_offset))
    
    # Calculate the number of usable rows/cols, accounting for minimum offset due to window size.
    num_valid_rows = len(left_img_arr) - 1 - edge_offset
    num_valid_cols = len(left_img_arr[0]) - 1 - edge_offset

    for row in range(edge_offset, num_valid_rows):
        # Instead of iterating through every column linearly, we have a queue of columns to iterate.
        columns = []
        # Stores columns from the RIGHT that have been matched, alongside with info about quality.
        matches = {}
        # Initially, fill with all columns.
        columns += list(range(edge_offset, num_valid_cols))

        # Iterating through all columns that need a pair. 
        while(len(columns) > 0):
            current_column = columns.pop()

            # Extract a window around the target pixel. We'll be reusing it, so we only pull it once.
            left_window = get_slice(row, current_column, edge_offset, left_img_arr)

            # Info about the best match.
            max_correlation = 0
            max_correlation_col = None

            # With a fixed left pixel, iterate through every potential match in the right
            for potential_matching_col in range(current_column - 1, max(current_column - ASSUMED_MAX_DISPARITY, edge_offset - 1) , -1):
                rightChunk = get_slice(row, potential_matching_col, edge_offset, right_img_arr)
                correlation = get_correlation(left_window, rightChunk)

                if max_correlation_col is None or correlation > max_correlation:
                    # Now, enforce uniqueness constraint.
                    # If we've found a match better than an existing one, remove existing match.
                    if (not potential_matching_col in matches) or correlation > matches[potential_matching_col]['correlation']:
                        if potential_matching_col in matches:
                            columns.append(matches[potential_matching_col]['left_col'])
                        if max_correlation_col is not None: #
                            matches.pop(max_correlation_col) #
                        max_correlation_col = potential_matching_col
                        max_correlation = correlation
                        matches[max_correlation_col] = {
                            'left_col': current_column,
                            'correlation': max_correlation
                        }
            
            # Assign the disparity of this pixel.
            distance = current_column - max_correlation_col if max_correlation_col is not None else 0
            disparities[row - edge_offset, current_column - edge_offset] = distance
    return disparities
            


