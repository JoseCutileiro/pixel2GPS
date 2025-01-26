#!/usr/bin/env python3
# createCoordMap.py

import cv2
import numpy as np

# Global list to hold the points the user clicks
clicked_points = []

def mouse_callback(event, x, y, flags, param):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print(f"Clicked pixel = ({x}, {y})")

def main():
    # --- 1. Load your image ---
    image_path = 'C:\\Users\\35196\OneDrive\Ambiente de Trabalho\\tese\PIC_code\pixel2GPS\polardistV2\\tes.png'
    img = cv2.imread(image_path)
    if img is None:
        print("Error: could not read image.")
        return

    # We'll make a copy for display
    display_img = img.copy()

    # --- 2. Set up the mouse callback ---
    cv2.namedWindow("Click 13 points in order")
    cv2.setMouseCallback("Click 13 points in order", mouse_callback)

    instructions = """
    Instructions:
    1) Click the center.
    2) Click points at 2,4,6m for 0° direction.
    3) Click points at 2,4,6m for 90° direction.
    4) Click points at 2,4,6m for 180° direction.
    5) Click points at 2,4,6m for 270° direction.
    """
    print(instructions)

    # We'll keep showing the image until we have 13 points
    while True:
        cv2.imshow("Click 13 points in order", display_img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key to exit
            break
        if len(clicked_points) == 13:
            break

    cv2.destroyAllWindows()

    if len(clicked_points) != 13:
        print("You did not click exactly 13 points. Exiting.")
        return

    # Real world coordinates for the 13 points, in the order we expect the user to click.
    # The center is (0,0)
    # 0° direction -> (2,0), (4,0), (6,0)
    # 90° direction -> (0,2), (0,4), (0,6)
    # 180° -> (-2,0), (-4,0), (-6,0)
    # 270° -> (0,-2), (0,-4), (0,-6)

    real_points = np.array([
        [ 0,  0],   # Center
        [ 2,  0],   # 0°, 2m
        [ 4,  0],   # 0°, 4m
        [ 6,  0],   # 0°, 6m
        [ 0,  2],   # 90°, 2m
        [ 0,  4],   # 90°, 4m
        [ 0,  6],   # 90°, 6m
        [-2,  0],   # 180°, 2m
        [-4,  0],   # 180°, 4m
        [-6,  0],   # 180°, 6m
        [ 0, -2],   # 270°, 2m
        [ 0, -4],   # 270°, 4m
        [ 0, -6],   # 270°, 6m
    ], dtype=np.float32)

    pixel_points = np.array(clicked_points, dtype=np.float32)

    # --- 3. Compute affine transform ---
    #   An affine transform in 2D can be determined from 3 pairs exactly, but we
    #   have 13. We can do a least-squares fit with cv2.estimateAffine2D:
    affine_mat, inliers = cv2.estimateAffine2D(pixel_points, real_points)

    # affine_mat is 2x3:
    # [
    #   [a11, a12, b1],
    #   [a21, a22, b2]
    # ]

    if affine_mat is None:
        print("Error: could not compute an affine transform.")
        return

    # --- 4. Save the transform to file (map.txt) ---
    # We'll store the matrix in a simple text format:
    np.savetxt("map.txt", affine_mat)
    print("Affine matrix saved to map.txt.")
    print("Affine matrix:\n", affine_mat)

if __name__ == "__main__":
    main()
