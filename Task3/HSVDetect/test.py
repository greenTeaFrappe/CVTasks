import cv2

# Load the image
image_path = "hand4.png"  # Replace this with the correct path to your image
image = cv2.imread(image_path)

# Check if the image was loaded correctly
if image is None:
    print("Error: Could not load the image. Check the file path.")
else:
    # Resize the image for easier display (optional)
    image = cv2.resize(image, (600, 800))

    # Convert the image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Function to get HSV value on mouse click
    def get_hsv_value(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # Left-click to get HSV value
            hsv_value = hsv_image[y, x]
            print("HSV Value at ({}, {}): {}".format(x, y, hsv_value))

    # Display the image and set up a mouse callback
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", get_hsv_value)

    print("Click on the image to get HSV values. Press 'q' to quit.")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
