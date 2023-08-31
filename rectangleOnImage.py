import cv2
import numpy as np

# Load the image
image = cv2.imread('test.png')  # Replace with your image's path

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and improve detection
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect edges using Canny edge detector
edges = cv2.Canny(blurred, threshold1=30, threshold2=150)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

largest_area = 0
largest_contour = None

# Iterate through the contours to find the largest rectangle
for contour in contours:
    # Approximate the contour to a polygon
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    
    # Check if the polygon has 4 vertices (rectangle) and a reasonable area
    if len(approx) == 4 and cv2.contourArea(approx) > largest_area:
        largest_area = cv2.contourArea(approx)
        largest_contour = approx

# Draw the largest rectangle
if largest_contour is not None:
    # cv2.drawContours(image, [largest_contour], 0, (0, 0, 0), -1)  # Fill with black to remove the green box

    # Define the multiline text to be added
    multiline_text = "No 160,\nRathpaha,\nKahagolla,\nDiyatalawa."
    
    # Split the multiline text into individual lines
    lines = multiline_text.split('\n')
    
    # Calculate the position for centered text
    rect_coords = largest_contour.reshape(-1, 2)
    top_left = rect_coords.min(axis=0)
    bottom_right = rect_coords.max(axis=0)
    
    text_x = (top_left[0] + bottom_right[0]) // 2
    text_y = (top_left[1] + bottom_right[1]) // 2

    # Calculate vertical spacing between lines
    line_height = 30
    
    # Add each line of text centered below the previous line
    for line in lines:
        cv2.putText(image, line, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        text_y += line_height
    
    # Save the modified image
    output_path = 'output_image.jpg' 
    cv2.imwrite(output_path, image)

    print(f"Modified image saved to {output_path}")

else:
    print("No valid rectangle found in the image.")
