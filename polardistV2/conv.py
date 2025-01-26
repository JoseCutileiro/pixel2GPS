#!/usr/bin/env python3
# conv.py

import cv2
import numpy as np
import math

clicked_point = None

def mouse_callback(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f"Clicked pixel = ({x}, {y})")

def main():
    global clicked_point
    # Load image
    image_path = 'C:\\Users\\35196\OneDrive\Ambiente de Trabalho\\tese\PIC_code\pixel2GPS\polardistV2\\tes.png'
    img = cv2.imread(image_path)
    if img is None:
        print("Error: could not read image.")
        return

    # Read the affine matrix
    try:
        affine_mat = np.loadtxt("map.txt")
    except:
        print("Error reading map.txt.")
        return

    if affine_mat.shape != (2, 3):
        print("Affine matrix in map.txt is not the correct shape (2x3).")
        return

    # Set up display
    cv2.namedWindow("Click a point to convert")
    cv2.setMouseCallback("Click a point to convert", mouse_callback)
    
    print("Instructions: Click anywhere on the image to get (r,theta) in meters/degrees.")

    while True:
        display_img = img.copy()
        cv2.imshow("Click a point to convert", display_img)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC to exit
            break

        # If user clicked
        if clicked_point is not None:
            px, py = clicked_point

            # Convert to real-world (x, y)
            # We'll treat the pixel as (u, v) and multiply by the 2x3 matrix
            # M = affine_mat
            # real_coords = M * [u, v, 1]^T
            u, v = float(px), float(py)
            x = affine_mat[0, 0]*u + affine_mat[0, 1]*v + affine_mat[0, 2]
            y = affine_mat[1, 0]*u + affine_mat[1, 1]*v + affine_mat[1, 2]

            # Convert to polar
            r = math.sqrt(x*x + y*y)
            theta_rad = math.atan2(y, x)  # Radians
            theta_deg = math.degrees(theta_rad)
            # Convert to 0-360 if desired
            if theta_deg < 0:
                theta_deg += 360.0

            print(f"Clicked pixel=({px}, {py}) -> Real (x,y)=({x:.3f}, {y:.3f}) -> (r,theta)=({r:.3f}, {theta_deg:.3f} deg)")

            # Reset the click so we can click multiple times
            clicked_point = None

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
