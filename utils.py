from PIL import Image, ImageFilter
from config import SCALE, SET
import numpy as np

def get_image_arr(name = "im0", greyscale=False):
    img = Image.open(f"../images/{SET}/{name}.png")
    width, height = img.size
    img = img.resize((int(width/SCALE), int(height/SCALE)))
    if greyscale:
        img = img.convert(mode="L")
    return np.asarray(img)


# Helper function to calculate indexing bounds about a point.
def get_slice_bounds(row, col, offset):
    return [
        row - offset,
        row + offset + 1, 
        col - offset,
        col + offset + 1
    ]

# Helper function to extract a window around a point.
def get_slice(row, col, offset, arr):
    [rowBottom, rowTop, colBottom, colTop] = get_slice_bounds(row, col, offset)
    return arr[rowBottom:rowTop, colBottom:colTop]