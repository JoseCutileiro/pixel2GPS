import cv2
import os
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("models/yolo11n.pt")

# Directory containing images
input_directory = "imgTest/imgs"
output_file = "out.txt"

# Ensure the output file is empty
open(output_file, 'w').close()

# Iterate through all image files in the directory
for filename in os.listdir(input_directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Construct the full file path
        file_path = os.path.join(input_directory, filename)

        # Read the image
        image = cv2.imread(file_path)
        if image is None:
            print(f"Could not read {file_path}. Skipping.")
            continue

        # Run the YOLO model on the image
        results = model(image)

        # Open the output file in append mode
        with open(output_file, "a") as f:
            for result in results:
                for box in result.boxes:
                    if int(box.cls) == 0:  # Class 0 typically represents 'person'
                        # Get bounding box coordinates (x_min, y_min, x_max, y_max)
                        x_min, y_min, x_max, y_max = box.xyxy[0].cpu().numpy()

                        # Calculate the midpoint of the bounding box
                        x_mid = (x_min + x_max) / 2
                        y_mid = (y_min + y_max) / 2

                        # Write to the file
                        f.write(f"{filename} - {int(x_mid)} {int(y_mid)}\n")

                        # Draw the bounding box on the image
                        cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
                        cv2.putText(image, "Person", (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the image with bounding boxes
        output_image_path = os.path.join(input_directory, f"out_{filename}")
        cv2.imwrite(output_image_path, image)

print(f"Processing complete. Output saved to {output_file}.")
