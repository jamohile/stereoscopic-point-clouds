# How much each side of the source image will be downscaled by.
SCALE = 8
# Which image set to use.
SET = "adirondack"
# Half-width of windows used to region match.
OFFSET = int(3/(SCALE / 8))


###################
# REGION MATCHING
###################

# The maximum disparity to consider.
ASSUMED_MAX_DISPARITY = int(30 / (SCALE/8))


###################
# POST PROCESSING
###################

# Occasionally, we get huge outlier distance values. This filters those out.
THRESHOLD_DISTANCE_OUTLIER = 10 ** 4

# If two pixels are within this z-distance, considered z-related.
THRESHOLD_Z_RELATION = 5

# Color difference threshold to consider two points similar.
THRESHOLD_COLOR_REGION_RELATION = 5



###################
# CAMERA PARAMS
###################

PRINCIPLE_X_A=1445.577
PRINCIPLE_X_B=1654.636
PRINCIPLE_Y = 984.686
FOCAL_PX=4161.221
BASELINE=176.252 # DOFFS but in mm
DOFFS = PRINCIPLE_X_B - PRINCIPLE_X_A