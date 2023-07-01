import cv2
import numpy as np
import math

def analyze_flash_rate(video_path):
    # Read the video
    video = cv2.VideoCapture(video_path)

    # Check if the video is opened successfully
    if not video.isOpened():
        print("Error opening video file:", video_path)
        return

    # Calculate the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize variables for flash count and time
    flash_count = 0
    total_time = 0.0

    # Iterate through each frame of the video
    for frame_number in range(total_frames):
        # Read the frame
        ret, frame = video.read()

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the average intensity of the frame
        average_intensity = np.mean(gray_frame)

        # Check if the frame is a flash by comparing the intensity with a threshold
        threshold = 100  # Adjust this threshold as needed
        if average_intensity > threshold:
            flash_count += 1

        # Calculate the time elapsed based on the frame rate
        frame_rate = video.get(cv2.CAP_PROP_FPS)
        frame_time = 1.0 / frame_rate
        total_time += frame_time
    # Release the video object
    video.release()
    # Check if the total time is zero
    if total_time == 0:
        print("Error: Unable to calculate flash rate. Total time is zero.")
        return

    # Calculate the flash rate in Hz
    flash_rate = flash_count / total_time

    # Check if the flash rate falls within the specified range
    if 3 <= flash_rate <= 30:
        print("Is a trigger with a flash rate of ",flash_rate)
    else:
        print("Not a trigger: ",flash_rate)
    


# Specify the path to your video file
video_path = "data/videos/Epilepsy Test_Trim.mp4"

# Call the function to analyze the flash rate
analyze_flash_rate(video_path)
