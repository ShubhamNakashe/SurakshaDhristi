import streamlit as st
import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
from streamlit_extras.switch_page_button import switch_page


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
           .nav-bar {
    display: flex;
    justify-content: flex-end;
    padding: 12px 20px;
    background: transparent;
    margin-bottom: 25px;
}

.nav-item {
    margin: 0 20px;
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
    text-decoration: none;
    transition: color 0.3s ease-in-out;
}

.nav-item:hover {
    color: #f9a8d4;
    text-decoration: underline;
}
.stButton>button {
    margin: 6px;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 900;  /* Bold text */
    font-size: 22px;   /* Larger font size */
    border: none;
    background-color: rgba(255, 255, 255, 0.1); /* Subtle hover effect */
    color: #f9a8d4;
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    text-decoration: underline;
    background-color: rgba(255, 255, 255, 0.1); /* Subtle hover effect */
    color: #f9a8d4;
}

        /* Make Streamlit transparent overlay parts cleaner */
        header, footer {
            background: none;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    st.image("Videos/logo3.png", width=150)

with col2:
    col2_1, col2_2, col2_3, col2_4, col2_5 = st.columns(5)
    with col2_1:
        if st.button("Home"):
            switch_page("app")  # if app.py is your main file
    with col2_2:
        if st.button("Locate on Map"):
            switch_page("ip locator")
    with col2_3:
        if st.button("CCTV Footage"):
            switch_page("live surveillance")
    with col2_4:
        if st.button("Live Cameras"):
            switch_page("WebCam")
    with col2_5:
        if st.button("Dashboard"):
            switch_page("crime dashboard")

# Load models
gender_model = load_model('gender_model.h5')  # Input: (128, 128, 3)
violence_model = load_model('model.h5')       # Input: (None, 1, 99)

# Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Preprocessing for gender detection
def preprocess_gender_frame(frame, target_size=(128, 128)):
    resized = cv2.resize(frame, target_size)
    norm = resized / 255.0
    return np.expand_dims(norm, axis=0)

# Preprocessing for violence detection
def preprocess_violence_frame(frame):
    resized = cv2.resize(frame, (33, 3))  # 33 x 3 = 99
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    flat = gray.flatten() / 255.0
    return np.expand_dims(np.expand_dims(flat, axis=0), axis=1)

# Labels
gender_labels = ['Male', 'Female']
violence_labels = ['Non-Violent', 'Violent']
VIOLENCE_THRESHOLD = 0.0009# def draw_gender_percentage_overlay(display, male_count, female_count, total_faces):


# Custom VideoProcessor class
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.male_count = 0
        self.female_count = 0
        self.total_faces = 0
        self.violence_count = 0
        self.start_time = time.time()
        self.summary_placeholder = st.empty()
        # self.last_gender_update_time = time.time()
        # self.gender_overlay_text = ""


    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        display = img.copy()

        # Gender Detection
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



        # Violence Detection
        violence_input = preprocess_violence_frame(img)
        v_pred = violence_model.predict(violence_input, verbose=0)
        v_prob = v_pred[0][0]
        violence_label = violence_labels[1] if v_prob >= VIOLENCE_THRESHOLD else violence_labels[0]

        if v_prob >= VIOLENCE_THRESHOLD:
            self.violence_count += 1
            cv2.rectangle(display, (0, 0), (display.shape[1]-1, display.shape[0]-1), (0, 0, 255), 10)

        cv2.putText(display, f"Violence: {violence_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return av.VideoFrame.from_ndarray(display, format="bgr24")

# Streamlit app
st.title("Live Webcam")
st.write("This app uses machine learning to detect gender and potential violence in real-time using your webcam.")

# Start webcam stream
webrtc_streamer(
    key="gender-violence-detection",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

st.write("👉 Press **Stop** to end the stream.")


