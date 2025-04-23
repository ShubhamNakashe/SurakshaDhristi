import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
from utils.db_connection import save_crime_data,db 
from utils.db_connection import fetch_crime_data 

# def crime_dashboard():
#     st.title("Crime Data Dashboard")

#     data = {
#         'date': ['2020', '2021', '2022', '2023'],
#         'type': ['Assault', 'Harassment', 'Theft', 'Assault'],
#         'count': [120, 150, 100, 130],
#         'location': ['South Mumbai', 'Andheri', 'Bandra', 'Dadar']
#     }
#     df = pd.DataFrame(data)
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("Crime Trend Over Years")
#         st.plotly_chart(px.line(df, x='date', y='count'))

#     with col2:
#         st.subheader("Crime Type Distribution")
#         st.plotly_chart(px.pie(df, names='type', values='count'))

#     comparison_data = {
#         'location': ['South Mumbai', 'Andheri', 'Bandra', 'Dadar'],
#         '2020': [20, 35, 15, 25],
#         '2021': [25, 30, 20, 15],
#         '2022': [30, 20, 35, 20],
#         '2023': [40, 25, 30, 25]
#     }

#     df_comp = pd.DataFrame(comparison_data)
#     fig = go.Figure()
#     for year in ['2020', '2021', '2022', '2023']:
#         fig.add_trace(go.Bar(x=df_comp['location'], y=df_comp[year], name=year))
#     fig.update_layout(barmode='group', title='Crime Comparison Across Years')

#     st.plotly_chart(fig)

st.header("🚨 Add Crime Report")

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
        # def save_crime_data(crime_data):
            # try:
            #     ref = db.reference("crime_reports")
            #     ref.push(data)
            #     print("✅ Data saved to Firebase!")
            # except Exception as e:
            #     print("❌ Error saving to Firebase:", e)
        st.success("✅ Crime report submitted!")
        st.write("📄 Submitted Crime Data:", crime_data)
        save_crime_data(crime_data)
        

    # You can now pass `crime_data` to Firebase

def crime_dashboard():
    st.title("Crime Data Dashboard")
    st.write("Crime analysis over the past year, categorized by type and location")

 
# 1. Fetch data from Firebase
def fetch_crime_data():
    ref = db.reference("crime_reports")
    data = ref.get()
    if data:
        # Convert dict to list of dicts
        return list(data.values())
    else:
        return []

# 2. Load into DataFrame
crime_data = fetch_crime_data()
# if crime_data:
#     df = pd.DataFrame(crime_data)

#     st.subheader("📊 Crime Type Distribution")
#     fig1 = px.pie(df, names='type', title='Crime Types Reported')
#     st.plotly_chart(fig1)

#     st.subheader("📍 Crimes by Location")
#     fig2 = px.bar(df, x='location', color='type', title='Crimes per Location')
#     st.plotly_chart(fig2)

#     st.subheader("📅 Crimes Over Time")
#     fig3 = px.histogram(df, x='date', nbins=10, title='Crimes by Date')
#     st.plotly_chart(fig3)
# else:
#     st.warning("No crime reports found in database.")


# Dummy crime_data simulation (replace with your actual data)
# df = pd.DataFrame(crime_data)
# Ensure date column is in datetime format
# df['date'] = pd.to_datetime(df['date'])

# Replace this with your actual crime_data


st.markdown("""
    <style>
        /* Main container with dark background */
        .main-container {
            background-color: #2e2e2e;  /* Dark grey background */
            padding: 20px;
            border-radius: 15px;
            color: white;
        }

        /* Header styling with deep black background and smaller strip */
        .header {
            background-color: #212121;  /* Very dark grey background */
            padding: 10px 20px;  /* Smaller height */
            border-radius: 5px;
            color: white;
            margin-bottom: 20px;
            text-align: left;
            font-size: 1.5rem;  /* Smaller font size */
            font-weight: 600;
            letter-spacing: 0.5px;
            width: 100%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }

        /* Optional: Adjust other elements like buttons */
        .stButton>button {
            background-color: #2980b9;
            color: white;
            border-radius: 8px;
            font-weight: 600;
        }

        .stButton>button:hover {
            background-color: #3498db;
        }
    </style>
""", unsafe_allow_html=True)

# Header with simple deep black background and smaller font size
st.markdown("<div class='header'><h2>Crime Data Analysis Dashboard</h2></div>", unsafe_allow_html=True)


# Dummy crime_data check
if crime_data:
    df = pd.DataFrame(crime_data)
    df['date'] = pd.to_datetime(df['date'])

    # Start main container
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # Top-level Filters
    st.markdown("<h3 style='color:white;'>🔍 Filter Crime Data</h3>", unsafe_allow_html=True)

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

    # KPIs
    st.markdown("<h4 style='color:white;'>🔢 Key Performance Indicators</h4>", unsafe_allow_html=True)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Crimes", len(filtered_df))
    kpi2.metric("Unique Locations", filtered_df['location'].nunique())
    kpi3.metric("Crime Types", filtered_df['type'].nunique())
    kpi4.metric("Date Range", f"{filtered_df['date'].min().date()} → {filtered_df['date'].max().date()}")

    # Section: Quick Insights
    st.markdown("<div class='card'><h4 style='color: white;'>📊 Quick Insights</h4></div>", unsafe_allow_html=True)
    
    # Layout for Quick Insights
    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        fig1 = px.pie(filtered_df, names='type', hole=0.4, title="Crime Type Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    with row1_col2:
        fig2 = px.bar(filtered_df, x='location', color='type', title='Crimes per Location')
        st.plotly_chart(fig2, use_container_width=True)

    with row1_col3:
        timeline = filtered_df.groupby('date').size().reset_index(name='count')
        fig3 = px.line(timeline, x='date', y='count', markers=True, title="Crimes Over Time")
        st.plotly_chart(fig3, use_container_width=True)

    # Section: Additional Views
    st.markdown("<div class='card'><h4 style='color: #1e1e1e;'>📈 Additional Visuals</h4></div>", unsafe_allow_html=True)
    
    r2c1, r2c2 = st.columns(2)

    with r2c1:
        fig4 = px.area(timeline, x='date', y='count', title='Cumulative Crime Trend')
        st.plotly_chart(fig4, use_container_width=True)

    with r2c2:
        fig5 = px.pie(filtered_df, names='type', hole=0.5, title="Donut: Crime Types")
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ No crime reports found in database.")

crime_dashboard()
