import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
from utils.db_connection import save_crime_data, db
from utils.db_connection import fetch_crime_data

# Set page configuration
st.set_page_config(page_title="Crime Dashboard - Suraksha Drishti", layout="wide")

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
    h2, h3, h4 {
        color: white;
        text-align: center;
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
    /* Card styling for sections */
    .card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
    }
    /* Chart cards */
    .chart-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .chart-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #d3d3d3;
        text-align: center;
    }
    /* KPI cards */
    .kpi-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        color: white;
        margin: 5px;
    }
    .kpi-label {
        font-size: 14px;
        color: #d3d3d3;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #ff4d94;
    }
    /* Filter section */
    .filter-section {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
    }
    /* Adjust Plotly chart background */
    .plotly-graph-div {
        background-color: transparent !important;
    }
    /* Adjust Streamlit elements */
    .stSelectbox, .stMultiSelect, .stDateInput {
        background-color: rgba(255, 255, 255, 0.1);
        color: #000000; /* Black text for dropdowns */
        border-radius: 8px;
    }
    .stSelectbox div, .stMultiSelect div, .stDateInput div {
        color: #000000; /* Black text for dropdown options */
    }
    .stButton>button {
        background-color: #ff4d94;
        color: #000000; /* Changed text color to black */
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #ff6ba8;
        color: #000000; /* Black text on hover */
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
            <a class="nav-item" href="http://localhost:8501/app.py">Home</a>
            <a class="nav-item" href="http://localhost:8501/pages/Crime_Dashboard.py">Dashboard</a>
            <a class="nav-item" href="http://localhost:8501/app.py">CCTV</a>
            <a class="nav-item" href="http://localhost:8501/app.py">Live</a>
            <a class="nav-item" href="http://localhost:8501/app.py">Violence</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main Title
st.markdown("<h1>Crime Data Dashboard</h1>", unsafe_allow_html=True)

# Fetch data from Firebase
crime_data = fetch_crime_data()

# Display dashboard if data exists
if crime_data:
    df = pd.DataFrame(crime_data)
    df['date'] = pd.to_datetime(df['date'])

    # Filter Section
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    st.markdown("<h3>🔍 Filter Crime Data</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 3, 4])
    with col1:
        crime_types = st.multiselect("Select Crime Types", df['type'].unique(), default=df['type'].unique())
    with col2:
        locations = st.multiselect("Select Locations", df['location'].unique(), default=df['location'].unique())
    with col3:
        date_range = st.date_input("Select Date Range", [df['date'].min(), df['date'].max()])

    # Filter the data
    filtered_df = df[
        (df['type'].isin(crime_types)) &
        (df['location'].isin(locations)) &
        (df['date'] >= pd.to_datetime(date_range[0])) &
        (df['date'] <= pd.to_datetime(date_range[1]))
    ]
    st.markdown("</div>", unsafe_allow_html=True)

    # KPIs Section
    st.markdown("<h4>🔢 Key Performance Indicators</h4>", unsafe_allow_html=True)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Crimes</div>
                <div class="kpi-value">{len(filtered_df)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with kpi2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Unique Locations</div>
                <div class="kpi-value">{filtered_df['location'].nunique()}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with kpi3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Crime Types</div>
                <div class="kpi-value">{filtered_df['type'].nunique()}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with kpi4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Date Range</div>
                <div class="kpi-value">{filtered_df['date'].min().date()} → {filtered_df['date'].max().date()}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Main Charts (to match the screenshot)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='chart-title'>Crime Trend Over Years</h2>", unsafe_allow_html=True)
        timeline = filtered_df.groupby(filtered_df['date'].dt.year).size().reset_index(name='count')
        fig1 = px.line(timeline, x='date', y='count', markers=True, labels={'count': 'Crime Count'})
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="white"
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='chart-title'>Crime Type Distribution</h2>", unsafe_allow_html=True)
        type_counts = filtered_df['type'].value_counts().reset_index()
        type_counts.columns = ['type', 'count']
        fig2 = px.pie(type_counts, names='type', values='count',
                      color_discrete_sequence=['#ff6384', '#36a2eb', '#ffcd56'])
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="white"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Quick Insights Section
    st.markdown("<div class='card'><h4>📊 Quick Insights</h4></div>", unsafe_allow_html=True)
    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        type_counts_insight = filtered_df.groupby('type').size().reset_index(name='count')
        fig3 = px.pie(type_counts_insight, names='type', values='count', hole=0.4,
                      title="Crime Type Distribution")
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="white"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with row1_col2:
        fig4 = px.bar(filtered_df, x='location', color='type', title='Crimes per Location')
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="white"
        )
        st.plotly_chart(fig4, use_container_width=True)

    with row1_col3:
        timeline = filtered_df.groupby('date').size().reset_index(name='count')
        fig5 = px.line(timeline, x='date', y='count', markers=True, title="Crimes Over Time")
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="white"
        )
        st.plotly_chart(fig5, use_container_width=True)

    # Additional Visuals Section
    st.markdown("<div class='card'><h4>📈 Additional Visuals</h4></div>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)

    with r2c1:
        fig6 = px.area(timeline, x='date', y='count', title='Cumulative Crime Trend')
        fig6.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="white"
        )
        st.plotly_chart(fig6, use_container_width=True)

    with r2c2:
        type_counts_additional = filtered_df.groupby('type').size().reset_index(name='count')
        fig7 = px.pie(type_counts_additional, names='type', values='count', hole=0.5,
                      title="Donut: Crime Types")
        fig7.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="white"
        )
        st.plotly_chart(fig7, use_container_width=True)

else:
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <h4 style="color: #ff4d94;">⚠️ No Crime Reports Found</h4>
            <p style="color: #ff4d94;">Please submit crime reports to view the dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Crime Report Form
st.markdown("<div class='card'><h3>🚨 Add Crime Report</h3></div>", unsafe_allow_html=True)
with st.form("crime_form"):
    crime_date = st.date_input("Date of Crime")
    crime_type = st.selectbox("Type of Crime", ["Theft", "Assault", "Robbery", "Fraud", "Harassment", "Other"])
    crime_location = st.text_input("Location")
    crime_description = st.text_area("Description")

    submitted = st.form_submit_button("Submit")

    if submitted:
        crime_data = {
            "date": str(crime_date),
            "type": crime_type,
            "location": crime_location,
            "description": crime_description
        }
        st.success("✅ Crime report submitted!")
        st.write("📄 Submitted Crime Data:", crime_data)
        save_crime_data(crime_data)