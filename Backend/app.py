from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np, math

# Flask app
app = Flask(__name__)
CORS(app)

# Initialize webcam, detector, and classifier once
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300
labels = ["Okay", "Please", "No", "Hello", "Thankyou", "Yes"]

# Store current prediction
current_prediction = {"label": "", "confidence": 0}

def generate_frames():
    global current_prediction
    while True:
        success, img = cap.read()
        if not success:
            continue  # skip if frame not read

        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

            if imgCrop.size != 0:
                aspectRatio = h / w
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                label = labels[index]
                conf = round(float(max(prediction)) * 100, 2)
                current_prediction = {"label": label, "confidence": conf}

                cv2.putText(imgOutput, f"{label} ({conf}%)", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', imgOutput)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Home route
@app.route("/")
def home():
    return "Sign Language Detection Backend is running!"

# Video streaming route
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Prediction route
@app.route('/prediction')
def prediction():
    return jsonify(current_prediction)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
