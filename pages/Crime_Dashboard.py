import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def crime_dashboard():
    st.title("Crime Data Dashboard")

    data = {
        'date': ['2020', '2021', '2022', '2023'],
        'type': ['Assault', 'Harassment', 'Theft', 'Assault'],
        'count': [120, 150, 100, 130],
        'location': ['South Mumbai', 'Andheri', 'Bandra', 'Dadar']
    }
    df = pd.DataFrame(data)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Crime Trend Over Years")
        st.plotly_chart(px.line(df, x='date', y='count'))

    with col2:
        st.subheader("Crime Type Distribution")
        st.plotly_chart(px.pie(df, names='type', values='count'))

    comparison_data = {
        'location': ['South Mumbai', 'Andheri', 'Bandra', 'Dadar'],
        '2020': [20, 35, 15, 25],
        '2021': [25, 30, 20, 15],
        '2022': [30, 20, 35, 20],
        '2023': [40, 25, 30, 25]
    }

    df_comp = pd.DataFrame(comparison_data)
    fig = go.Figure()
    for year in ['2020', '2021', '2022', '2023']:
        fig.add_trace(go.Bar(x=df_comp['location'], y=df_comp[year], name=year))
    fig.update_layout(barmode='group', title='Crime Comparison Across Years')

    st.plotly_chart(fig)

crime_dashboard()
