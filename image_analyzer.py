import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

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

def save_model(model, model_filename):
    # Save the trained model to a file
    joblib.dump(model, model_filename)
    print(f"Model saved to '{model_filename}'.")

def load_model(model_filename):
    # Load the saved model from a file
    model = joblib.load(model_filename)
    print(f"Model loaded from '{model_filename}'.")
    return model

def main_func(with_patterns, no_pattern):
    clf = SVC(kernel='linear')  # Create a new instance of the classifier for each pair of images

    # Load images
    image_with_patterns = cv2.imread(with_patterns)
    image_without_patterns = cv2.imread(no_pattern)

    X = []
    y = []

    # Number of samples for each class
    num_samples_with_patterns = 5
    num_samples_without_patterns = 5

    # Image with patterns (label 1)
    for _ in range(num_samples_with_patterns):
        features_with_patterns = extract_features(image_with_patterns)
        X.append([features_with_patterns])
        y.append(1)

    # Image without patterns (label 0)
    for _ in range(num_samples_without_patterns):
        features_without_patterns = extract_features(image_without_patterns)
        X.append([features_without_patterns])
        y.append(0)

    X = np.array(X)
    y = np.array(y)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Check if there are at least two unique classes in the training set
    unique_classes = np.unique(y_train)
    if len(unique_classes) < 2:
        raise ValueError("Insufficient classes in the training set. Add more samples from both classes.")

    # Create and train the SVM classifier
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    return clf  # Return the trained classifier

def predict_image(image_path, model):
    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)

        # Extract features from the image
        features = extract_features(image)
        print(features)
        # Make a prediction using the pre-trained model
        prediction = model.predict([[features]])[0]

        # Define a dictionary to map the prediction label to a meaningful message
        result = {
            0: "No repeated patterns detected.",
            1: "Repeated patterns detected."
        }

        # Prepare the response
        response = {
            "prediction": int(prediction),  # Convert numpy.int32 to Python int
            "message": result[prediction]
        }

        return response

    except Exception as e:
        return {"error": str(e)}

def create_model():
    # directory of images with patterns
    pattern_dir = './static/img/pattern'
    # directory of images with no patterns
    no_pattern_dir = './static/img/no pattern'

    items = os.listdir(pattern_dir)
    for pattern, no_pattern in zip(items, os.listdir(no_pattern_dir)):
        pattern_path = os.path.join(pattern_dir, pattern)
        no_pattern_path = os.path.join(no_pattern_dir, no_pattern)
        main_func(pattern_path, no_pattern_path)

    # Save the last trained model to a file
    clf = main_func(f"./static/img/pattern/{pattern}", f"./static/img/no pattern/{no_pattern}")
    save_model(clf, 'trained_model.joblib')


