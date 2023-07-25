import cv2
import numpy as np
from flask_cors import CORS
from flask import Flask,jsonify,abort,request,render_template
import math
from image_analyzer import predict_image,load_model
app = Flask(__name__)

CORS(app)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze-image',methods=['POST'])
def analyze_image():
    try:
        return jsonify(predict_image(request.get_json()['path'],load_model('trained_model.joblib')))
    except Exception as e:
        print(e)
        abort(500)
        
@app.route('/analyze',methods=['POST'])
def analyze_video():
    intensities = []
    url = request.get_json()['path']
        # Read the video
    video = cv2.VideoCapture(url)

    # Check if the video is opened successfully
    if not video.isOpened():
        abort(500)

    # Calculate the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize variables for flash count and time
    flash_count = 0
    total_time = 0.0
    flash_rate = 0.0
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
        intensities.append(average_intensity)
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
        return jsonify({"success":False,"trigger":None,"flash_rate":None})

    # Calculate the flash rate in Hz
    flash_rate = flash_count / total_time

    # Check if the flash rate falls within the specified range
    if flash_rate >= 3.0 and flash_rate <= 50.0:
        return jsonify({"success":True,"trigger":True,"flash_rate":flash_rate})
    else:
        return jsonify({"success":True,"trigger":False,"flash_rate":flash_rate})



@app.errorhandler(500)
def bad_request(code):
    return jsonify({"success":False,"error":500,"message":"File not properly opened. check path","trigger":None,"flash_rate":None}), 500


if __name__ == "__main__":
    app.run(debug=True)