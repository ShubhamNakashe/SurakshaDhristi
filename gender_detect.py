import cv2
import numpy as np
from tensorflow.keras.models import load_model

gender_model = load_model("gender_model.h5")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def count_genders(video_path):
    cap = cv2.VideoCapture(video_path)
    male_count = 0
    female_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (128, 128))
            face_input = face_resized / 255.0
            face_input = np.expand_dims(face_input, axis=0)

            pred = gender_model.predict(face_input)[0][0]
            if pred > 0.5:
                male_count += 1
            else:
                female_count += 1

    cap.release()

    total = male_count + female_count
    if total == 0:
        return 0.0, 0.0  # No faces detected

    male_percent = round((male_count / total) * 100, 2)
    female_percent = round((female_count / total) * 100, 2)

    return male_percent, female_percent
