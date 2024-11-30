import cv2


def list_camera_indexes():
    index = 0
    while True:
        # Try to open the camera with the current index
        cap = cv2.VideoCapture(index)

        # Check if the camera was opened successfully
        if not cap.read()[0]:
            break

        # Release the camera
        cap.release()

        # Print the index
        print(f"Camera index {index} is available")

        # Move to the next index
        index += 1


# Call the function to list camera indexes
list_camera_indexes()