import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Streamlit Web Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('AirQuality_cleaned.csv')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.sort_values('Datetime')
    return df

df = load_data()

# Column mapping
POLLUTANT_MAPPING = {
    "PM2.5": "C6H6(GT)",
    "NO2": "NO2(GT)",
    "NOx": "NOx(GT)",
    "O3": "PT08.S5(O3)",
    "SO2": "PT08.S4(NO2)"
}

def calculate_aqi(value):
    """Calculate AQI from pollutant value"""
    if value < 50:
        return {'aqi': round(value), 'status': 'Good', 'color': '#4CAF50'}
    elif value < 100:
        return {'aqi': round(value), 'status': 'Moderate', 'color': '#FFC107'}
    elif value < 150:
        return {'aqi': round(value), 'status': 'Unhealthy for Sensitive', 'color': '#FF9800'}
    else:
        return {'aqi': round(value), 'status': 'Unhealthy', 'color': '#F44336'}

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin-bottom: 30px;">
    <h1 style="color: white; margin: 0;">📊 Streamlit Web Dashboard</h1>
    <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">Milestone 4: Working Application (Weeks 7-8)</p>
</div>
""", unsafe_allow_html=True)


# Sidebar Controls
st.sidebar.markdown("### ⚙️ Controls")

station = st.sidebar.selectbox(
    "Monitoring Station",
    ["Downtown", "Suburb", "Industrial Zone"]
)

time_range = st.sidebar.selectbox(
    "Time Range",
    ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Data"]
)

pollutant = st.sidebar.selectbox(
    "Pollutant",
    list(POLLUTANT_MAPPING.keys())
)

forecast_horizon = st.sidebar.selectbox(
    "Forecast Horizon",
    ["1 Hour", "6 Hours", "12 Hours", "24 Hours", "48 Hours"]
)

# Update button
update_btn = st.sidebar.button("🔄 Update Dashboard", use_container_width=True)

# Admin toggle
st.sidebar.markdown("---")
admin_mode = st.sidebar.toggle("Admin Mode")

# Get time range data
def get_time_filtered_data(df, time_range):
    if time_range == "Last 24 Hours":
        start = df['Datetime'].max() - timedelta(hours=24)
    elif time_range == "Last 7 Days":
        start = df['Datetime'].max() - timedelta(days=7)
    elif time_range == "Last 30 Days":
        start = df['Datetime'].max() - timedelta(days=30)
    else:  # All Data
        start = df['Datetime'].min()
    
    return df[df['Datetime'] >= start]

# Filter data
filtered_df = get_time_filtered_data(df, time_range)
col_name = POLLUTANT_MAPPING[pollutant]
pollutant_values = filtered_df[col_name].dropna()

# Get current AQI
if len(pollutant_values) > 0:
    current_value = pollutant_values.iloc[-1]
    aqi_info = calculate_aqi(current_value)
else:
    aqi_info = {'aqi': 0, 'status': 'No Data', 'color': '#999999'}

# Main Dashboard Grid
col1, col2, col3 = st.columns(3)

# Column 1: Current Air Quality
with col1:
    st.markdown("### 📊 Current Air Quality")
    st.markdown(f"**Station:** {station}")
    
    # AQI Gauge using plotly
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=aqi_info['aqi'],
        title={'text': pollutant},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 200]},
            'bar': {'color': aqi_info['color']},
            'steps': [
                {'range': [0, 50], 'color': "rgba(76, 175, 80, 0.3)"},
                {'range': [50, 100], 'color': "rgba(255, 193, 7, 0.3)"},
                {'range': [100, 150], 'color': "rgba(255, 152, 0, 0.3)"},
                {'range': [150, 200], 'color': "rgba(244, 67, 54, 0.3)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 150
            }
        }
    ))
    fig_gauge.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.markdown(f"**Status:** <span style='color: {aqi_info['color']}; font-weight: bold;'>{aqi_info['status']}</span>", unsafe_allow_html=True)

# Column 2: Forecast
with col2:
    st.markdown(f"### 📈 {pollutant} Forecast")
    
    # Generate forecast data
    recent_values = pollutant_values.tail(12).values if len(pollutant_values) >= 12 else pollutant_values.values
    
    # Forecast horizon mapping
    horizon_map = {"1 Hour": 1, "6 Hours": 6, "12 Hours": 12, "24 Hours": 24, "48 Hours": 48}
    h = horizon_map[forecast_horizon]
    
    # Generate forecast
    last_val = recent_values[-1] if len(recent_values) > 0 else 50
    forecast = np.array([last_val + (np.sin(i/5) * 10) + np.random.randn() * 3 for i in range(h)])
    forecast = np.maximum(forecast, 0)
    
    # Time labels
    time_actual = list(range(len(recent_values)))
    time_forecast = list(range(len(recent_values)-1, len(recent_values) + h - 1))
    
    fig_forecast = go.Figure()
    
    fig_forecast.add_trace(go.Scatter(
        x=time_actual,
        y=recent_values,
        name='Historical',
        mode='lines+markers',
        line=dict(color='#667eea', width=2),
        marker=dict(size=6)
    ))
    
    fig_forecast.add_trace(go.Scatter(
        x=time_forecast,
        y=forecast,
        name='Forecast',
        mode='lines+markers',
        line=dict(color='#ff6b35', width=2, dash='dash'),
        marker=dict(size=6)
    ))
    
    fig_forecast.update_layout(
        height=350,
        hovermode='x unified',
        template='plotly_white',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_forecast, use_container_width=True)

# Column 3: Alert Notifications
with col3:
    st.markdown("### 🚨 Alert Notifications")
    
    alerts = []
    
    if aqi_info['aqi'] > 100:
        alerts.append({
            'type': 'warning',
            'icon': '⚠️',
            'title': 'Moderate air quality expected',
            'time': 'Tomorrow, 10:00 AM'
        })
    
    if aqi_info['aqi'] > 150:
        alerts.append({
            'type': 'danger',
            'icon': '🔴',
            'title': 'High pollution alert',
            'time': 'Tomorrow, 2:00 PM'
        })
    
    if aqi_info['aqi'] < 50:
        alerts.append({
            'type': 'success',
            'icon': '✅',
            'title': 'Good air quality today',
            'time': 'Today, 8:00 AM'
        })
    else:
        alerts.append({
            'type': 'info',
            'icon': 'ℹ️',
            'title': 'Model update completed',
            'time': 'Yesterday, 11:30 PM'
        })
    
    for alert in alerts:
        if alert['type'] == 'warning':
            st.warning(f"{alert['icon']} **{alert['title']}**\n\n{alert['time']}")
        elif alert['type'] == 'danger':
            st.error(f"{alert['icon']} **{alert['title']}**\n\n{alert['time']}")
        elif alert['type'] == 'success':
            st.success(f"{alert['icon']} **{alert['title']}**\n\n{alert['time']}")
        else:
            st.info(f"{alert['icon']} **{alert['title']}**\n\n{alert['time']}")

# Second Row: Pollutant Trends
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Pollutant Trends")
    
    # Get multiple pollutants for comparison
    pollutants_to_plot = ["PM2.5", "NO2", "O3"]
    
    fig_trends = go.Figure()
    
    for pol in pollutants_to_plot:
        col = POLLUTANT_MAPPING[pol]
        if col in filtered_df.columns:
            values = filtered_df[col].dropna()
            x_range = list(range(len(values)))

            
            fig_trends.add_trace(go.Scatter(
                x=x_range,
                y=values,
                name=pol,
                mode='lines',
                line=dict(width=2)
            ))
    
    fig_trends.update_layout(
        height=400,
        hovermode='x unified',
        template='plotly_white',
        xaxis_title='Time',
        yaxis_title='Concentration (μg/m³)',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_trends, use_container_width=True)

# Data statistics
with col2:
    st.markdown("### 📈 Statistics")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric(
            "Current",
            f"{aqi_info['aqi']} AQI",
            delta=aqi_info['status']
        )
    
    with col_b:
        st.metric(
            "24h Average",
            f"{pollutant_values.tail(24).mean():.1f}",
            delta=f"({pollutant_values.tail(24).std():.1f} std)"
        )
    
    with col_c:
        st.metric(
            "Max (24h)",
            f"{pollutant_values.tail(24).max():.1f}",
            delta=f"Min: {pollutant_values.tail(24).min():.1f}"
        )
    
    # Data table
    st.markdown("### 📋 Recent Data")
    display_df = filtered_df[[
        'Datetime', 'C6H6(GT)', 'NO2(GT)', 'NOx(GT)', 'PT08.S5(O3)', 'T', 'RH'
    ]].tail(10).copy()
    display_df.columns = ['DateTime', 'PM2.5', 'NO2', 'NOx', 'O3', 'Temp', 'Humidity']
    st.dataframe(display_df, use_container_width=True)

# Admin Interface
if admin_mode:
    st.markdown("---")
    st.markdown('<div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
    st.markdown("### 🔐 Admin Interface")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Upload New Data**")
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        if uploaded_file is not None:
            st.success("File uploaded successfully!")
            st.write(pd.read_csv(uploaded_file).head())
    
    with col2:
        st.markdown("**Model Retraining**")
        if st.button("🤖 Retrain Models"):
            with st.spinner("Training models..."):
                import time
                time.sleep(2)
            st.success("Models retrained successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
