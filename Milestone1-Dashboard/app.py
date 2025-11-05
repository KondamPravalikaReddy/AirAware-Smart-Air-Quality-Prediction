import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------
# 🎨 PAGE SETUP
# ----------------------------
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# ----------------------------
# 🌗 THEME TOGGLE
# ----------------------------
theme = st.sidebar.radio("🌗 Choose Theme", ["Dark Mode", "Light Mode"])

# Define color palettes for both themes
if theme == "Dark Mode":
    bg_color = "#121212"
    text_color = "#EDEDED"
    subtext_color = "#BBBBBB"
    accent_color = "#FF8C00"
    chart_colors = ["#FFA500", "#FF6347", "#FFD700", "#FF4500"]
    plot_template = "plotly_dark"
else:
    bg_color = "#F5F5F5"
    text_color = "#222222"
    subtext_color = "#555555"
    accent_color = "#0073e6"
    chart_colors = ["#0073e6", "#66b3ff", "#99ccff", "#3399ff"]
    plot_template = "plotly_white"

# ----------------------------
# 💅 CUSTOM STYLING
# ----------------------------
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        [data-testid="stMetricValue"] {{
            color: {accent_color};
            font-size: 30px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}
        .main-title {{
            text-align: center;
            font-size: 40px;
            color: {accent_color};
            font-weight: bold;
        }}
        .sub-header {{
            text-align: center;
            color: {subtext_color};
            font-size: 18px;
        }}
        hr {{
            border: 1px solid {accent_color};
        }}
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 🌿 TITLE
# ----------------------------
st.markdown("<div class='main-title'>🌿 Air Quality Monitoring Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Analyze and visualize air pollutant levels interactively</div>", unsafe_allow_html=True)
st.markdown("---")

# ----------------------------
# 📂 LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("AirQuality_cleaned.csv")

    rename_map = {
        'CO(GT)': 'CO',
        'PT08.S1(CO)': 'Sensor_CO',
        'NMHC(GT)': 'NMHC',
        'C6H6(GT)': 'Benzene',
        'PT08.S2(NMHC)': 'Sensor_NMHC',
        'NOx(GT)': 'NOx',
        'PT08.S3(NOx)': 'Sensor_NOx',
        'NO2(GT)': 'NO2',
        'PT08.S4(NO2)': 'Sensor_NO2',
        'PT08.S5(O3)': 'Sensor_O3',
        'T': 'Temperature_C',
        'RH': 'Relative_Humidity',
        'AH': 'Absolute_Humidity',
        'O3': 'O3',
        'SO2': 'SO2'
    }

    df = df.rename(columns=rename_map)
    df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
    df = df.dropna(subset=['Datetime'])
    df = df.sort_values(by='Datetime')
    return df

df = load_data()

# ----------------------------
# 🧭 SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("🧭 Filters")

pollutants = [
    'CO', 'NO2', 'NOx', 'NMHC', 'Benzene',
    'Temperature_C', 'Relative_Humidity', 'Absolute_Humidity',
    'Sensor_CO', 'Sensor_NO2', 'Sensor_NOx', 'Sensor_NMHC', 'Sensor_O3'
]

selected_pollutants = st.sidebar.multiselect("Select Pollutants", pollutants, default=['CO', 'NO2', 'Temperature_C'])

time_range = st.sidebar.selectbox("Select Time Range", ["Last 7 Days", "Last 30 Days", "All Data"])
if time_range == "Last 7 Days":
    df = df[df['Datetime'] >= df['Datetime'].max() - pd.Timedelta(days=7)]
elif time_range == "Last 30 Days":
    df = df[df['Datetime'] >= df['Datetime'].max() - pd.Timedelta(days=30)]

# ----------------------------
# 📊 KPI METRICS
# ----------------------------
# --- Key Indicators Section ---
st.markdown(f"<h2 style='color:{text_color};'>📊 Key Indicators</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<p style='color:{text_color}; font-size:18px;'>🌡️ Avg Temperature (°C)</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#1E90FF;'>{df['Temperature_C'].mean():.2f}</h3>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<p style='color:{text_color}; font-size:18px;'>💧 Avg Humidity (%)</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#1E90FF;'>{df['Relative_Humidity'].mean():.2f}</h3>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<p style='color:{text_color}; font-size:18px;'>🌿 Avg CO (mg/m³)</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#1E90FF;'>{df['CO'].mean():.2f}</h3>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<p style='color:{text_color}; font-size:18px;'>🚗 Avg NOx (ppb)</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#1E90FF;'>{df['NOx'].mean():.2f}</h3>", unsafe_allow_html=True)


# ----------------------------
# 📈 TRENDS
# ----------------------------
st.markdown("---")
st.markdown(f"<h3 style='color:{text_color};'>📈 Trends Over Time</h3>", unsafe_allow_html=True)

if selected_pollutants:
    for pollutant in selected_pollutants:
        if pollutant in df.columns:
            fig = px.line(
                df, x='Datetime', y=pollutant, 
                title=f"{pollutant} Trend Over Time",
                color_discrete_sequence=chart_colors,
                template=plot_template
            )
            st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please select at least one pollutant to view trends.")

# ----------------------------
# 🧩 COMPARISON
# ----------------------------
if len(selected_pollutants) > 1:
    st.markdown(f"<h3 style='color:{text_color};'>📊 Pollutant Comparison</h3>", unsafe_allow_html=True)
    fig2 = px.line(
        df, x='Datetime', y=selected_pollutants, 
        title="Comparison of Selected Pollutants",
        color_discrete_sequence=chart_colors,
        template=plot_template
    )
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# 🔍 DATA INSIGHTS
# ----------------------------
st.markdown("---")
st.markdown(f"<h3 style='color:{text_color};'>🔍 Data Insights</h3>", unsafe_allow_html=True)

colA, colB = st.columns(2)
with colA:
    st.write("#### Average Values per Pollutant")
    avg_data = df[selected_pollutants].mean().reset_index()
    avg_data.columns = ['Pollutant', 'Average Value']
    fig3 = px.bar(
        avg_data, x='Pollutant', y='Average Value', color='Pollutant',
        color_discrete_sequence=chart_colors,
        template=plot_template
    )
    st.plotly_chart(fig3, use_container_width=True)

with colB:
    st.write("#### Correlation Heatmap")
    corr = df[selected_pollutants].corr()
    fig4 = px.imshow(
        corr, text_auto=True, aspect="auto",
        color_continuous_scale='Oranges' if theme=="Dark Mode" else 'Blues',
        template=plot_template
    )
    st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# 🧾 FOOTER
# ----------------------------
st.markdown("---")
st.markdown(
    f"<center style='color:{subtext_color};'>© 2025 Air Quality Dashboard | Powered by Streamlit</center>",
    unsafe_allow_html=True
)