# import streamlit as st
# import cv2
# import numpy as np
# import time
# from tensorflow.keras.models import load_model
# from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
# import av

# # Load models
# gender_model = load_model('gender_model.h5')  # Input: (128, 128, 3)
# violence_model = load_model('model.h5')  # Input: (None, 1, 99)

# # Haar cascade for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# # Preprocessing for gender
# def preprocess_gender_frame(frame, target_size=(128, 128)):
#     resized = cv2.resize(frame, target_size)
#     norm = resized / 255.0
#     return np.expand_dims(norm, axis=0)

# # Preprocessing for violence
# def preprocess_violence_frame(frame):
#     resized = cv2.resize(frame, (33, 3))  # 33 x 3 = 99
#     gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#     flat = gray.flatten() / 255.0
#     return np.expand_dims(np.expand_dims(flat, axis=0), axis=1)

# # Labels
# gender_labels = ['Male', 'Female']
# violence_labels = ['Non-Violent', 'Violent']
# VIOLENCE_THRESHOLD = 0.0006
# # Custom VideoProcessor for streamlit-webrtc
# class VideoProcessor(VideoProcessorBase):
#     def __init__(self):
#         self.male_count = 0
#         self.female_count = 0
#         self.total_faces = 0
#         self.violence_count = 0
#         self.start_time = time.time()
#         self.summary_placeholder = st.empty()

#     def recv(self, frame):
#         img = frame.to_ndarray(format="bgr24")
#         display = img.copy()

#         # Gender Detection
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

#         for (x, y, w, h) in faces:
#             face = img[y:y+h, x:x+w]
#             gender_input = preprocess_gender_frame(face)
#             pred = gender_model.predict(gender_input, verbose=0)
#             gender_index = np.argmax(pred)
#             label = gender_labels[gender_index]

#             if gender_index == 0:
#                 self.male_count += 1
#             else:
#                 self.female_count += 1
#             self.total_faces += 1

#             cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             cv2.putText(display, f"Gender: {label}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

#         # Violence Detection
#         violence_input = preprocess_violence_frame(img)
#         v_pred = violence_model.predict(violence_input, verbose=0)
#         v_prob = v_pred[0][0]
#         violence_label = violence_labels[1] if v_prob >= VIOLENCE_THRESHOLD else violence_labels[0]

#         if v_prob >= VIOLENCE_THRESHOLD:
#             self.violence_count += 1
#             cv2.rectangle(display, (0, 0), (display.shape[1]-1, display.shape[0]-1), (0, 0, 255), 10)

#         cv2.putText(display, f"Violence: {violence_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#         # Summary every 45 seconds
#         elapsed = time.time() - self.start_time
#         if elapsed >= 45:
#             summary = "--- 45 Second Summary ---\n"
#             if self.total_faces > 0:
#                 male_percent = (self.male_count / self.total_faces) * 100
#                 female_percent = (self.female_count / self.total_faces) * 100
#             else:
#                 male_percent = female_percent = 0.0
#             summary += f"Male %: {male_percent:.1f}%, Female %: {female_percent:.1f}%\n"
#             summary += f"Violence Detections: {self.violence_count}\n"
#             summary += "-------------------------\n"
#             self.summary_placeholder.text(summary)

#             # Reset counters
#             self.start_time = time.time()
#             self.male_count = self.female_count = self.total_faces = self.violence_count = 0

#         return av.VideoFrame.from_ndarray(display, format="bgr24")

# # Streamlit app
# st.title("Gender & Violence Detection")
# st.write("This app detects gender and potential violence in real-time using a webcam feed.")

# # Initialize webrtc streamer
# webrtc_streamer(
#     key="gender-violence-detection",
#     video_processor_factory=VideoProcessor,
#     media_stream_constraints={"video": True, "audio": False},
#     async_processing=True,
# )

# st.write("Press 'Stop' in the video feed to end the session.")


import streamlit as st
import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

# Load models
gender_model = load_model('gender_model.h5')
violence_model = load_model('model.h5')

# Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Preprocessing
def preprocess_gender_frame(frame, target_size=(128, 128)):
    resized = cv2.resize(frame, target_size)
    norm = resized / 255.0
    return np.expand_dims(norm, axis=0)

def preprocess_violence_frame(frame):
    resized = cv2.resize(frame, (33, 3))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    flat = gray.flatten() / 255.0
    return np.expand_dims(np.expand_dims(flat, axis=0), axis=1)

gender_labels = ['Male', 'Female']
violence_labels = ['Non-Violent', 'Violent']
VIOLENCE_THRESHOLD = 0.0006

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.male_count = 0
        self.female_count = 0
        self.total_faces = 0
        self.violence_count = 0
        self.start_time = time.time()
        self.summary_placeholder = st.empty()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        display = img.copy()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = img[y:y+h, x:x+w]
            gender_input = preprocess_gender_frame(face)
            pred = gender_model.predict(gender_input, verbose=0)
            gender_index = np.argmax(pred)
            label = gender_labels[gender_index]

            if gender_index == 0:
                self.male_count += 1
            else:
                self.female_count += 1
            self.total_faces += 1

            cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(display, f"Gender: {label}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        violence_input = preprocess_violence_frame(img)
        v_pred = violence_model.predict(violence_input, verbose=0)
        v_prob = v_pred[0][0]
        violence_label = violence_labels[1] if v_prob >= VIOLENCE_THRESHOLD else violence_labels[0]

        if v_prob >= VIOLENCE_THRESHOLD:
            self.violence_count += 1
            cv2.rectangle(display, (0, 0), (display.shape[1]-1, display.shape[0]-1), (0, 0, 255), 10)

        cv2.putText(display, f"Violence: {violence_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elapsed = time.time() - self.start_time
        if elapsed >= 45:
            summary = "--- 45 Second Summary ---\n"
            if self.total_faces > 0:
                male_percent = (self.male_count / self.total_faces) * 100
                female_percent = (self.female_count / self.total_faces) * 100
            else:
                male_percent = female_percent = 0.0
            summary += f"Male %: {male_percent:.1f}%, Female %: {female_percent:.1f}%\n"
            summary += f"Violence Detections: {self.violence_count}\n"
            summary += "-------------------------\n"
            self.summary_placeholder.text(summary)

            self.start_time = time.time()
            self.male_count = self.female_count = self.total_faces = self.violence_count = 0

        return av.VideoFrame.from_ndarray(display, format="bgr24")

# -------------- UI Code --------------

st.markdown("""
    <style>
        /* Full page background */
        html, body, .main, .block-container {
            background-color: #2D1D63 !important;
        }

        .main-card {
            background-color: rgba(255, 255, 255, 0.06);
            padding: 2rem;
            border-radius: 25px;
            box-shadow: 0px 0px 15px rgba(0,0,0,0.2);
            margin-top: 2rem;
        }

        .header-title {
            text-align: center;
            font-size: 2.2rem;
            font-weight: bold;
            color: #ffffff;
        }

        .subtext {
            text-align: center;
            margin-top: 0.5rem;
            color: #ccc;
        }

        .stat-text {
            font-size: 1.3rem;
            text-align: center;
            margin-top: 1.5rem;
            color: white;
        }

        /* Button styling */
        .stButton>button {
            background-color: #e63946;
            color: white;
            border-radius: 6px;
            padding: 0.5em 1em;
            font-weight: bold;
            border: none;
        }

        .stButton>button:hover {
            background-color: #ff4b5c;
        }

        /* Make Streamlit transparent overlay parts cleaner */
        header, footer {
            background: none;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div style="background: linear-gradient(to right, #6a11cb, #2575fc); padding: 1rem;"><div class="header-title">🎥 Gender & Violence Detection</div></div>', unsafe_allow_html=True)

# Main webcam card
with st.container():
    st.markdown('<div class="main-card" id="webcam-section">', unsafe_allow_html=True)


    webrtc_ctx = webrtc_streamer(
        key="gender-violence-detection",
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if webrtc_ctx.video_processor:
        male_percent = (webrtc_ctx.video_processor.male_count / webrtc_ctx.video_processor.total_faces) * 100 if webrtc_ctx.video_processor.total_faces > 0 else 0
        female_percent = 100 - male_percent if webrtc_ctx.video_processor.total_faces > 0 else 0

        st.markdown(f'<div class="stat-text">🧔 Male: {male_percent:.1f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-text">👩 Female: {female_percent:.1f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-text">⚠️ Violence: <b>Not Checked</b></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.write("Press 'Stop' in the video feed to end the session.")
