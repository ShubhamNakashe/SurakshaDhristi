import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from keras import backend as K
from tensorflow.keras.models import load_model
import os

# Load the model once
model_path = "model.h5"
loaded_model = load_model(model_path)

# Create output directory for processed frames
output_dir = './output_frames'
os.makedirs(output_dir, exist_ok=True)

def detect_violence(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    pose_data = []
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb_frame)

        if result.pose_landmarks:
            landmarks = [[lm.x, lm.y, lm.z] for lm in result.pose_landmarks.landmark]
            pose_data.append(landmarks)

    cap.release()

    # Process pose data
    if not pose_data:
        return "No pose data detected."

    pose_data = np.array(pose_data)
    pose_data = pose_data / np.max(pose_data)  # Normalize

    num_frames = pose_data.shape[0]
    num_landmarks = pose_data.shape[1] if num_frames > 0 else 0
    features = num_landmarks * 3

    pose_data_avg = np.mean(pose_data, axis=0).reshape((1, 1, features))
    
    K.clear_session()

    # Predict violence
    prediction = loaded_model.predict(pose_data_avg)
    prediction_threshold = 0.0012

    return "🚨 Violence Detected!" if prediction[0][0] > prediction_threshold else "✅ No Violence Detected."
