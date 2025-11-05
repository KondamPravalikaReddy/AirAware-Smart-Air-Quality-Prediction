import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="Air Quality Alert System",
    page_icon="⚠️",
    layout="wide"
)

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv('AirQuality_cleaned.csv')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    return df

df = load_data()

# Show dataset info
st.write("✅ **Dataset Loaded:**", df.shape)

# Embed the HTML dashboard
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=2000, scrolling=True)