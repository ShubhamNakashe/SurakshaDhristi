# import streamlit as st

# st.set_page_config(page_title="Suraksha Drishti", layout="wide")
# st.title("Suraksha Drishti")
# st.write("Welcome! Use the sidebar to navigate between pages.")

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page configuration
st.set_page_config(page_title="Suraksha Drishti", layout="wide")

# Custom CSS for styling to match the screenshot
st.markdown(
    """
    <style>
    /* Background and text styling */
    .stApp {
        background: linear-gradient(135deg, #1e1b4b 0%, #3b2a77 100%);
        color: white;
        font-family: 'Arial', sans-serif;
    }
    h1 {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-top: 50px;
        color: white;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #d3d3d3;
        margin-bottom: 40px;
    }
    /* Navigation bar styling */
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
    /* Feature cards styling */
    .feature-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px;
        color: white;
        transition: transform 0.3s;
        min-height: 150px;
    }
    .feature-card:hover {
        transform: scale(1.05);
        background-color: rgba(255, 255, 255, 0.2);
    }
    .feature-icon {
        font-size: 40px;
        color: #ff4d94;
        margin-bottom: 10px;
    }
    .feature-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .feature-desc {
        font-size: 14px;
        color: #d3d3d3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo and Navigation Bar
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

# Main Title and Subtitle
st.markdown("<h1>Real-Time Women Safety Surveillance</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">A comprehensive surveillance system offering live CCTV feeds, crime dashboards, threat detection, and gender-based violence monitoring.</p>',
    unsafe_allow_html=True
)

# First Row of Feature Cards
cols1 = st.columns(3)

# Feature 1: Threat Detection
with cols1[0]:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Threat Detection</div>
            <div class="feature-desc">Detects violence or distress gestures instantly.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Feature 2: YOLO Monitoring
with cols1[1]:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">👁️</div>
            <div class="feature-title">Monitoring</div>
            <div class="feature-desc">Object and person detection via camera feeds.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Feature 3: AI Behavior Analysis
with cols1[2]:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI Behavior Analysis</div>
            <div class="feature-desc">Uses deep models for movement tracking.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Second Row of Feature Cards
cols2 = st.columns(3)

# Feature 4: Instant Alerts
with cols2[0]:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔔</div>
            <div class="feature-title">Instant Alerts</div>
            <div class="feature-desc">Live notification on unusual activity.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Feature 5: Live Feed
with cols2[1]:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📹</div>
            <div class="feature-title">Live Feed</div>
            <div class="feature-desc">Stream and analyze video in real-time.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Feature 6: Camera Integration
with cols2[2]:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📷</div>
            <div class="feature-title">Camera Integration</div>
            <div class="feature-desc">Plug in multiple CCTV sources.</div>
        </div>
        """,
        unsafe_allow_html=True
    )