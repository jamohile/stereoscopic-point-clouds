from utils import get_image_arr

from pre_process import get_region_map
from disparities import get_disparity_map
from triangulation import get_distance_map
from cloud_generation import get_points
from post_process import get_processed

from config import SCALE, SET, OFFSET



def main(file_out = "./generated-cloud.txt"):
    left_image_arr = get_image_arr("im0", greyscale=True)
    right_image_arr = get_image_arr("im1", greyscale=True)

    left_image_arr_color = get_image_arr("im0", greyscale=False)

    disparity_map = get_disparity_map(left_image_arr, right_image_arr, OFFSET)
    distance_map = get_distance_map(disparity_map)
    processed_distance_map = get_processed(distance_map, left_image_arr_color, iterations=3)
    points = get_points(processed_distance_map, left_image_arr_color)
    
    np.savetxt(file_out, points)    

main()