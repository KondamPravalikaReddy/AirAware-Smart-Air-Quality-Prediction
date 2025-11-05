import streamlit as st

# Load dataset (if needed in backend)
import pandas as pd
df = pd.read_csv("AirQuality_cleaned.csv")
st.write("Dataset Loaded:", df.shape)

# Show dashboard.html fullscreen in an iframe
st.components.v1.iframe("http://localhost:8502/dashboard.html", height=1800, width=1500, scrolling=True)
