import cv2
import numpy as np
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

def extract_features(image):
    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(grayscale_image, threshold1=100, threshold2=200)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=100)

    # Calculate line count as a feature
    line_count = len(lines) if lines is not None else 0

    return line_count

def load_model(model_filename):
    # Your existing code to load the saved model
    model = joblib.load(model_filename)
    return model

# Load the pre-trained SVM model
model_filename = "trained_model.joblib"
loaded_model = load_model(model_filename)

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        # Get the uploaded image from the request
        file = request.files['image']

        # Read the image using OpenCV
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Extract features from the image
        features = extract_features(image)

        # Make a prediction using the pre-trained model
        prediction = loaded_model.predict([[features]])[0]
        print(loaded_model.predict([[features]]))

        # Define a dictionary to map the prediction label to a meaningful message
        result = {
            0: "No repeated patterns detected.",
            1: "Repeated patterns detected."
        }

        # Prepare the response
        response = {
            "prediction": int(prediction),
            "message": result[prediction]
        }

        return jsonify(response)
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error occured"})

if __name__ == "__main__":
    app.run(debug=True)
