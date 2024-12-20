import base64
import io

import cv2
import numpy as np
from imageio import imread
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

classifier = load_model("models/emotion_classifier.h5")
classes = ["Angry", "Happy", "Calm", "Sad", "Surprise"]
expression = "None"


# converts a base64 encoded image string to a numpy array
def uri_to_cv2_img(uri):
    _, encoded = uri.split(",", 1)
    img = imread(io.BytesIO(base64.b64decode(encoded)))
    return img


# determines the person's mood based on the image of the face
def getExpression(uri):
    img = uri_to_cv2_img(uri)
    frame = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected = haar_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    expression = ""

    for x, y, w, h in detected:
        # Draws blue rectangle around face
        cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)

        # Stores only face from the image
        roi_gray = gray[y : y + h, x : x + w]

        # Resize to 48x48 using interpolation to calculate pixel values for new image
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        # If a face is detected in the ROI by the classifier
        if np.sum([roi_gray]) != 0:
            # Normalized, converted to array to be used by model
            roi = roi_gray.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            predict = classifier.predict(roi)[0]
            label = classes[predict.argmax()]
            label_position = (x, y)
            expression = label.lower()

            # Puts prediction as text above the ROI, in green
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(
                frame, "No Face Detected", (20, 20), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3
            )

    # Convert to jpeg to pass to website feed
    _, jpeg = cv2.imencode(".jpg", frame)

    if expression == "":
        expression = "Calm"
    return expression, jpeg.tobytes()
