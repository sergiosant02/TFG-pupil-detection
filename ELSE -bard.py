import numpy as np
import cv2

def draw_ellipse(image, ellipse_params):
    """
    Draw an ellipse on the given image.

    Parameters:
    - image: The input image.
    - ellipse_params: A tuple containing parameters of the ellipse (center, axes, angle).
      Example: ((cx, cy), (major_axis, minor_axis), angle)

    Returns:
    - None (modifies the input image in-place).
    """
    center, axes, angle = ellipse_params

    # Convert the angles from degrees to radians
    angle_rad = np.radians(angle)

    # Draw the ellipse on the image
    cv2.ellipse(image, center, axes, angle, 0, 360, (0, 255, 0), 2)


def preprocess_image(name ,image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize the image
    normalized_image = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    # Apply Canny edge detection
    edges = cv2.Canny(normalized_image, 50, 100)
    kernel = np.ones((5, 5), np.uint8)

    # Perform dilation to connect nearby edge pixels
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)
    edges = filter_edges(gray,edges)
    stacked_images = np.hstack((normalized_image, edges, dilated_edges))
    cv2.imshow(name + " Normalized | Edges, dilated", stacked_images)
    

    return edges

def filter_edges_neightbords(edges):
    # Sum up the direct neighborhood of each edge pixel
    neighborhood_sum = cv2.filter2D(edges.astype(np.float32), -1, np.ones((3, 3)))

    # Keep only the edges with exactly two neighbors
    filtered_edges = edges.copy()
    filtered_edges[(neighborhood_sum  > 2) & (neighborhood_sum > 0)] = 0

    return filtered_edges

def filter_edges(image, edges):
    kernel = np.ones((3, 3), np.uint8)

    # Perform dilation to connect nearby edge pixels
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    # Find the contours of the dilated edges
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an image to visualize the filtered edges
    filtered_edges_image = np.zeros_like(image)

    # Loop through each contour (edge) and filter edges with more than 2 neighbors
    for contour in contours:
        for point in contour:
            x, y = point[0]
            # Extract the neighborhood of the current pixel
            neighborhood = dilated_edges[y-1:y+2, x-1:x+2]
            # Subtract the central pixel to count neighbors
            neighbors_count = np.sum(neighborhood) - dilated_edges[y, x]
            # If the pixel has 2 or fewer neighbors, set the pixel in the result image
            if neighbors_count <= 20:
                filtered_edges_image[y, x] = 255

    return filtered_edges_image

def collect_and_evaluate_edges(edges):
    # Implement connected edge collection and evaluation (Step 2.2)
    # Evaluate based on straightness, inner intensity, elliptic properties, etc.

    # If a valid ellipse is found, return it
    # Otherwise, return None

    return ellipse_parameters  # Replace with actual ellipse parameters

def second_analysis(image):
    # Downsampling (Step 2.3.1)
    downsampled_image = cv2.resize(image, (new_width, new_height))

    # Surface difference and mean filter (Step 2.3.2)
    # Implement surface difference and mean filter

    # Select the best position (Step 2.3.3)
    best_position = select_best_position(filtered_image)

    # Optimize the position on the full-scale image (Step 2.4)
    optimized_position = optimize_position(full_scale_image, best_position)

    return optimized_position

def main():
    # Load the image
    image = cv2.imread("images/picture1.jpg")
    edges = preprocess_image('picture1', image)
    image = cv2.imread("images/picture2.jpg")
    edges = preprocess_image('picture2', image)
    image = cv2.imread("images/picture3.jpg")
    edges = preprocess_image('picture3', image)
    image = cv2.imread("images/picture4.jpg")
    edges = preprocess_image('picture4', image)

    # Preprocess the image
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""
    # Remove edge connections
    edges = filter_edges(edges)

    # Collect and evaluate connected edges
    ellipse_params = collect_and_evaluate_edges(edges)

    if ellipse_params:
        # If a valid ellipse is found, draw it on the image
        draw_ellipse(image, ellipse_params)
    else:
        # If no ellipse is found, perform the second analysis
        optimized_position = second_analysis(image)
        # Draw the result of the second analysis on the image

    # Display the final result
    cv2.imshow("Result", image)
    """
    

if __name__ == "__main__":
    main()