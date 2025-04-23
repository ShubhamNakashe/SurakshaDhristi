# import streamlit as st

# st.set_page_config(page_title="Suraksha Drishti", layout="wide")
# st.title("Suraksha Drishti")
# st.write("Welcome! Use the sidebar to navigate between pages.")

import streamlit as st

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
        padding: 10px 20px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .nav-item {
        margin: 0 15px;
        font-size: 16px;
        color: white;
        text-decoration: none;
    }
    .nav-item:hover {
        color: #ff4d94;
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
    st.image("https://via.placeholder.com/150x50?text=Suraksha+Drishti", width=150)  # Replace with your logo URL
with col2:
    st.markdown(
        """
        <div class="nav-bar">
            <a class="nav-item" href="#">Home</a>
            <a class="nav-item" href="#">Dashboard</a>
            <a class="nav-item" href="#">CCTV</a>
            <a class="nav-item" href="#">Live</a>
            <a class="nav-item" href="#webcam-section">Violence</a>
        </div>
        """,
        unsafe_allow_html=True
    )

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
            <div class="feature-title">YOLO Monitoring</div>
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