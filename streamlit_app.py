import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import json

# ========================================
# PAGE CONFIGURATION & THEME
# ========================================
st.set_page_config(
    page_title="🌟 Elite Weather Analytics Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# ADVANCED CSS STYLING WITH ANIMATIONS
# ========================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-gradient: linear-gradient(135deg, #232526 0%, #414345 100%);
        --aurora: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5, #ffbe0b, #fb5607);
    }
    
    /* Main App Background: animated starfield with gradient overlay */
    .stApp {
        --bg-overlay: radial-gradient(1200px 600px at 10% 10%, rgba(102, 126, 234, 0.12), transparent 60%),
                      radial-gradient(900px 600px at 90% 30%, rgba(245, 87, 108, 0.10), transparent 60%),
                      radial-gradient(1000px 700px at 30% 80%, rgba(79, 172, 254, 0.10), transparent 60%);
        background: #0b1020;
        background-image:
            radial-gradient(1px 1px at 20% 30%, rgba(255,255,255,0.35), rgba(255,255,255,0.08) 2px, transparent 3px),
            radial-gradient(1px 1px at 80% 20%, rgba(255,255,255,0.35), rgba(255,255,255,0.08) 2px, transparent 3px),
            radial-gradient(1px 1px at 60% 70%, rgba(255,255,255,0.35), rgba(255,255,255,0.08) 2px, transparent 3px),
            radial-gradient(1px 1px at 30% 60%, rgba(255,255,255,0.35), rgba(255,255,255,0.08) 2px, transparent 3px),
            radial-gradient(1px 1px at 50% 40%, rgba(255,255,255,0.35), rgba(255,255,255,0.08) 2px, transparent 3px),
            linear-gradient(135deg, #0b1020, #121b3a, #0f1533),
            var(--bg-overlay);
        background-size: auto, auto, auto, auto, auto, 400% 400%, cover;
        animation: gradientShift 24s ease infinite, twinkle 6s ease-in-out infinite;
        font-family: 'Poppins', sans-serif;
        color: #ffffff;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%, 0% 0%; }
        50% { background-position: 100% 50%, 100% 100%; }
        100% { background-position: 0% 50%, 0% 0%; }
    }

    @keyframes twinkle {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.15); }
    }
    
    /* Glowing Cards */
    .glow-card {
        background: rgba(255, 255, 255, 0.02);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 25px;
        backdrop-filter: blur(20px);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glow-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: var(--aurora);
        border-radius: 24px;
        opacity: 0;
        z-index: -1;
        transition: opacity 0.3s ease;
        animation: rotate 8s linear infinite;
    }
    
    .glow-card:hover::before {
        opacity: 0.7;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .glow-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.6),
            0 0 80px rgba(102, 126, 234, 0.3);
    }
    
    /* Hero Title */
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        background: var(--aurora);
        background-size: 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: auroraText 8s ease infinite;
        text-align: center;
        margin-bottom: 0;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }
    
    @keyframes auroraText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #a8b2d1;
        margin-top: 0;
        font-weight: 300;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        text-shadow: 0 2px 10px rgba(255, 255, 255, 0.3);
        font-family: 'Orbitron', monospace !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a8b2d1 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #00ff88 !important;
        font-weight: 600 !important;
    }
    
    /* Floating Animation */
    .floating {
        animation: floating 6s ease-in-out infinite;
    }
    
    @keyframes floating {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Pulse Animation */
    .pulse {
        animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Weather Icons */
    .weather-icon {
        font-size: 4rem;
        text-shadow: 0 0 20px currentColor;
        animation: iconGlow 4s ease-in-out infinite;
    }
    
    @keyframes iconGlow {
        0%, 100% { text-shadow: 0 0 20px currentColor; }
        50% { text-shadow: 0 0 40px currentColor, 0 0 60px currentColor; }
    }
    
    /* Selectbox Styling - force dark in all OS themes */
    .stSelectbox * { color-scheme: dark; }
    .stSelectbox > div > div > div,
    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: #e9eefc !important;
        min-height: 48px !important;
    }
    .stSelectbox div[data-baseweb="select"] input {
        color: #e9eefc !important;
        background: transparent !important;
        caret-color: #e9eefc !important;
    }
    .stSelectbox div[role="listbox"], 
    .stSelectbox ul[role="listbox"] {
        background: rgba(7, 11, 26, 0.98) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
    }
    .stSelectbox [role="option"] {
        color: #e9eefc !important;
    }
    .stSelectbox [role="option"][aria-selected="true"] {
        background: rgba(102, 126, 234, 0.25) !important;
    }
    .stSelectbox [role="option"]:hover {
        background: rgba(79, 172, 254, 0.25) !important;
    }
    @media (prefers-color-scheme: light) {
        .stSelectbox div[data-baseweb="select"] > div,
        .stSelectbox div[role="listbox"],
        .stSelectbox ul[role="listbox"] {
            background: rgba(7, 11, 26, 0.98) !important;
            color: #e9eefc !important;
        }
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
html, body { background:#070B1A; }
.stApp { background: transparent !important; }
.block-container { position: relative; z-index: 1; }
#bg3d { position: fixed; inset: 0; z-index: 0; pointer-events: none; }
</style>
""", unsafe_allow_html=True)

st.html("""
<canvas id=\"bg3d\"></canvas>
<script>
(function(){
  const canvas = document.getElementById('bg3d');
  const ctx = canvas.getContext('2d');
  let width = 0, height = 0, cx = 0, cy = 0, DPR = window.devicePixelRatio || 1;
  const STAR_COUNT = 900;
  const STAR_DEPTH = 900; // larger = farther
  const FOCAL = 320; // perspective strength
  let stars = [];

  function rand(min, max){ return Math.random() * (max - min) + min; }

  function resize(){
    width = window.innerWidth; height = window.innerHeight; cx = width/2; cy = height/2;
    canvas.width = Math.floor(width * DPR);
    canvas.height = Math.floor(height * DPR);
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  }

  function init(){
    stars = new Array(STAR_COUNT).fill(0).map(()=>({
      x: rand(-cx, cx), y: rand(-cy, cy), z: rand(1, STAR_DEPTH), v: rand(1.1, 3.0)
    }));
  }

  function recycle(s){ s.x = rand(-cx, cx); s.y = rand(-cy, cy); s.z = STAR_DEPTH; s.v = rand(1.1, 3.0); }

  function step(){
    ctx.clearRect(0, 0, width, height);
    // soft vignette backdrop
    const grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(cx, cy));
    grd.addColorStop(0, 'rgba(18, 26, 58, 0.35)');
    grd.addColorStop(1, 'rgba(5, 8, 20, 0.9)');
    ctx.fillStyle = grd; ctx.fillRect(0, 0, width, height);

    for (let i=0; i<stars.length; i++){
      const s = stars[i];
      s.z -= s.v; // move towards camera
      if (s.z <= 1) recycle(s);

      // gentle swirl
      const angle = 0.0008 * (STAR_DEPTH - s.z);
      const cosA = Math.cos(angle), sinA = Math.sin(angle);
      const rx = s.x * cosA - s.y * sinA;
      const ry = s.x * sinA + s.y * cosA;

      const k = FOCAL / s.z;
      const sx = rx * k + cx;
      const sy = ry * k + cy;
      if (sx < -50 || sx > width + 50 || sy < -50 || sy > height + 50){ recycle(s); continue; }

      const size = Math.max(0.6, 1.6 - (s.z / STAR_DEPTH));
      ctx.beginPath();
      ctx.fillStyle = 'rgba(160, 200, 255,' + (1 - s.z / STAR_DEPTH) + ')';
      ctx.arc(sx, sy, size, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(step);
  }

  window.addEventListener('resize', resize);
  resize(); init(); step();
})();
</script>
""")

# ========================================
# WORLD CITIES DATABASE
# ========================================
WORLD_CITIES = {
    "🏙️ New York, USA": (40.7128, -74.0060),
    "🌉 London, UK": (51.5074, -0.1278),
    "🗼 Paris, France": (48.8566, 2.3522),
    "🏯 Tokyo, Japan": (35.6895, 139.6917),
    "🌊 Sydney, Australia": (-33.8688, 151.2093),
    "🏗️ Dubai, UAE": (25.2048, 55.2708),
    "🌆 Mumbai, India": (19.0760, 72.8777),
    "🌴 Singapore": (1.3521, 103.8198),
    "🌁 San Francisco, USA": (37.7749, -122.4194),
    "🏙️ São Paulo, Brazil": (-23.5505, -46.6333),
    "⛰️ Cape Town, South Africa": (-33.9249, 18.4241),
    "🏔️ Moscow, Russia": (55.7558, 37.6173),
    "🏛️ Rome, Italy": (41.9028, 12.4964),
    "🏖️ Barcelona, Spain": (41.3851, 2.1734),
    "🌸 Seoul, South Korea": (37.5665, 126.9780),
}

# ========================================
# WEATHER CONDITION MAPPING
# ========================================
WEATHER_CONDITIONS = {
    0: ("☀️", "Clear Sky", "#FFD700"),
    1: ("🌤️", "Mainly Clear", "#FFA500"),
    2: ("⛅", "Partly Cloudy", "#87CEEB"),
    3: ("☁️", "Overcast", "#708090"),
    45: ("🌫️", "Fog", "#A9A9A9"),
    48: ("🌫️", "Rime Fog", "#A9A9A9"),
    51: ("🌦️", "Light Drizzle", "#4682B4"),
    53: ("🌦️", "Moderate Drizzle", "#4169E1"),
    55: ("🌧️", "Dense Drizzle", "#0000FF"),
    61: ("🌧️", "Slight Rain", "#1E90FF"),
    63: ("🌧️", "Moderate Rain", "#0000CD"),
    65: ("⛈️", "Heavy Rain", "#00008B"),
    71: ("❄️", "Slight Snow", "#B0E0E6"),
    73: ("🌨️", "Moderate Snow", "#87CEEB"),
    75: ("❄️", "Heavy Snow", "#4682B4"),
    95: ("⛈️", "Thunderstorm", "#8A2BE2"),
    96: ("⛈️", "Thunderstorm with Hail", "#9400D3"),
}

# ========================================
# DATA FETCHING FUNCTIONS
# ========================================
@st.cache_data(ttl=600, show_spinner=False)
def fetch_weather_data(lat, lon):
    """Fetch comprehensive weather data from Open-Meteo API"""
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "weather_code", "surface_pressure", "wind_speed_10m",
            "wind_direction_10m", "wind_gusts_10m"
        ],
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "precipitation_probability",
            "precipitation", "wind_speed_10m", "wind_direction_10m",
            "visibility", "uv_index", "weather_code"
        ],
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "precipitation_sum", "precipitation_hours", "precipitation_probability_max",
            "wind_speed_10m_max", "wind_gusts_10m_max", "uv_index_max"
        ],
        "timezone": "auto",
        "past_days": 3,
        "forecast_days": 14
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# ========================================
# VISUALIZATION FUNCTIONS
# ========================================
def create_temperature_gauge(current_temp, feels_like):
    """Create an animated temperature gauge"""
    fig = go.Figure()
    
    # Create gauge
    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = current_temp,
        delta = {'reference': feels_like, 'suffix': "°C feels like"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        # title removed; header is rendered above within the card
        gauge = {
            'axis': {'range': [-20, 50], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "cyan", 'thickness': 0.8},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 3,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': [
                {'range': [-20, 0], 'color': "rgba(135, 206, 250, 0.3)"},
                {'range': [0, 20], 'color': "rgba(0, 255, 127, 0.3)"},
                {'range': [20, 35], 'color': "rgba(255, 165, 0, 0.3)"},
                {'range': [35, 50], 'color': "rgba(255, 69, 0, 0.3)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': feels_like
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Orbitron"},
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_wind_compass(wind_speed, wind_direction):
    """Create an animated wind direction compass"""
    fig = go.Figure()
    
    # Create compass background
    theta = np.linspace(0, 2*np.pi, 100)
    r = np.ones(100)
    
    fig.add_trace(go.Scatterpolar(
        r=r,
        theta=np.degrees(theta),
        mode='lines',
        line=dict(color='rgba(255,255,255,0.3)', width=2),
        showlegend=False
    ))
    
    # Add wind direction arrow
    wind_rad = np.radians(wind_direction)
    arrow_r = [0, 0.8]
    arrow_theta = [wind_direction, wind_direction]
    
    fig.add_trace(go.Scatterpolar(
        r=arrow_r,
        theta=arrow_theta,
        mode='lines+markers',
        line=dict(color='#00ff88', width=8),
        marker=dict(size=[0, 20], color='#00ff88', symbol='arrow-up'),
        name=f'Wind: {wind_speed:.1f} km/h',
        showlegend=False
    ))
    
    # Add cardinal directions
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    
    for direction, angle in zip(directions, angles):
        fig.add_trace(go.Scatterpolar(
            r=[1.1],
            theta=[angle],
            mode='text',
            text=[direction],
            textfont=dict(size=16, color='white'),
            showlegend=False
        ))
    
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=False,
                range=[0, 1.3]
            ),
            angularaxis=dict(
                visible=False,
                direction="clockwise",
                rotation=90
            )
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def create_hourly_forecast_heatmap(hourly_data):
    """Create an animated hourly forecast heatmap"""
    hours = pd.to_datetime(hourly_data['time'])
    temps = hourly_data['temperature_2m']
    humidity = hourly_data['relative_humidity_2m']
    precip_prob = hourly_data['precipitation_probability']
    
    # Take next 48 hours
    df = pd.DataFrame({
        'hour': hours[:48],
        'temperature': temps[:48],
        'humidity': humidity[:48],
        'precipitation': precip_prob[:48]
    })
    
    # Create heatmap data
    df['day'] = df['hour'].dt.strftime('%a %m/%d')
    df['hour_only'] = df['hour'].dt.hour
    
    # Pivot for heatmap
    heatmap_data = df.pivot_table(
        values='temperature', 
        index='day', 
        columns='hour_only', 
        fill_value=np.nan
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=[f"{h:02d}:00" for h in heatmap_data.columns],
        y=heatmap_data.index,
        colorscale=[
            [0, '#440154'],
            [0.2, '#3b528b'],
            [0.4, '#21908d'],
            [0.6, '#5dc863'],
            [0.8, '#fde725'],
            [1, '#ff6b6b']
        ],
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>Hour: %{x}<br>Temperature: %{z:.1f}°C<extra></extra>",
        colorbar=dict(
            title="Temperature (°C)",
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            len=0.7
        )
    ))
    
    fig.update_layout(
        xaxis=dict(
            title="Hour of Day",
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        yaxis=dict(
            title="Date",
            tickfont=dict(color='white'),
            titlefont=dict(color='white')
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        margin=dict(l=50, r=50, t=60, b=50)
    )
    
    return fig

def create_precipitation_radar(daily_data):
    """Create precipitation probability radar chart"""
    days = pd.to_datetime(daily_data['time'])[:7]
    precip_prob = daily_data['precipitation_probability_max'][:7]
    precip_sum = daily_data['precipitation_sum'][:7]
    
    day_names = [day.strftime('%A') for day in days]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=precip_prob,
        theta=day_names,
        fill='toself',
        fillcolor='rgba(0, 255, 136, 0.2)',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8, color='#00ff88'),
        name='Precipitation Probability (%)',
        hovertemplate="<b>%{theta}</b><br>Probability: %{r}%<extra></extra>"
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='white'),
                gridcolor='rgba(255,255,255,0.3)'
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=12),
                gridcolor='rgba(255,255,255,0.3)'
            )
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=400,
        margin=dict(l=50, r=50, t=60, b=50)
    )
    
    return fig

def create_multi_metric_timeline(hourly_data):
    """Create multi-metric animated timeline"""
    hours = pd.to_datetime(hourly_data['time'])[:72]  # Next 3 days
    temps = hourly_data['temperature_2m'][:72]
    humidity = hourly_data['relative_humidity_2m'][:72]
    wind_speed = hourly_data['wind_speed_10m'][:72]
    uv_index = hourly_data['uv_index'][:72]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '🌡️ Temperature Trend', '💨 Wind Speed Pattern',
            '💧 Humidity Levels', '☀️ UV Index Forecast'
        ),
        vertical_spacing=0.18,
        horizontal_spacing=0.12
    )
    
    # Temperature
    fig.add_trace(
        go.Scatter(
            x=hours, y=temps,
            mode='lines+markers',
            line=dict(color='#ff6b6b', width=3, shape='spline'),
            fill='tonexty',
            fillcolor='rgba(255, 107, 107, 0.2)',
            marker=dict(size=4),
            name='Temperature',
            hovertemplate="<b>%{x}</b><br>Temperature: %{y:.1f}°C<extra></extra>"
        ),
        row=1, col=1
    )
    
    # Wind Speed
    fig.add_trace(
        go.Scatter(
            x=hours, y=wind_speed,
            mode='lines+markers',
            line=dict(color='#4ecdc4', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(78, 205, 196, 0.2)',
            marker=dict(size=4),
            name='Wind Speed',
            hovertemplate="<b>%{x}</b><br>Wind: %{y:.1f} km/h<extra></extra>"
        ),
        row=1, col=2
    )
    
    # Humidity
    fig.add_trace(
        go.Scatter(
            x=hours, y=humidity,
            mode='lines+markers',
            line=dict(color='#45b7d1', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(69, 183, 209, 0.2)',
            marker=dict(size=4),
            name='Humidity',
            hovertemplate="<b>%{x}</b><br>Humidity: %{y:.1f}%<extra></extra>"
        ),
        row=2, col=1
    )
    
    # UV Index
    fig.add_trace(
        go.Scatter(
            x=hours, y=uv_index,
            mode='lines+markers',
            line=dict(color='#f7b733', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(247, 183, 51, 0.2)',
            marker=dict(size=4),
            name='UV Index',
            hovertemplate="<b>%{x}</b><br>UV Index: %{y:.1f}<extra></extra>"
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=620,
        margin=dict(l=60, r=60, t=40, b=60)
    )
    
    # Update all axes
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='white'),
                row=i, col=j
            )
            fig.update_yaxes(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='white'),
                row=i, col=j
            )
    
    return fig

def create_weather_mood_indicator(weather_code, temp, humidity):
    """Create a fun weather mood indicator"""
    icon, condition, color = WEATHER_CONDITIONS.get(weather_code, ("❓", "Unknown", "#888888"))
    
    # Calculate mood score
    mood_score = 50
    if 15 <= temp <= 25:
        mood_score += 20
    elif temp < 5 or temp > 35:
        mood_score -= 20
    
    if humidity < 60:
        mood_score += 15
    elif humidity > 80:
        mood_score -= 15
    
    if weather_code in [0, 1]:
        mood_score += 25
    elif weather_code in [61, 63, 65, 95, 96]:
        mood_score -= 20
    
    mood_score = max(0, min(100, mood_score))
    
    # Mood categories
    if mood_score >= 80:
        mood = "FANTASTIC! 🎉"
        mood_color = "#00ff88"
    elif mood_score >= 60:
        mood = "Pretty Good 😊"
        mood_color = "#4ecdc4"
    elif mood_score >= 40:
        mood = "Okay 😐"
        mood_color = "#f7b733"
    else:
        mood = "Could Be Better 😔"
        mood_color = "#ff6b6b"
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = mood_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"☁️ WEATHER MOOD<br><span style='font-size:16px;color:{mood_color};'>{mood}</span>", 
                'font': {'size': 20, 'color': 'white'}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': mood_color, 'thickness': 0.8},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 3,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': [
                {'range': [0, 25], 'color': "rgba(255, 107, 107, 0.3)"},
                {'range': [25, 50], 'color': "rgba(247, 183, 51, 0.3)"},
                {'range': [50, 75], 'color': "rgba(78, 205, 196, 0.3)"},
                {'range': [75, 100], 'color': "rgba(0, 255, 136, 0.3)"}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Orbitron"},
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

# ========================================
# MAIN APP
# ========================================
def main():
    # Hero Section
    st.markdown('<h1 class="hero-title">ELITE WEATHER HUB</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">⚡ Advanced Real-Time Weather Analytics & Forecasting Platform ⚡</p>', unsafe_allow_html=True)
    
    # City Selection
    st.markdown("""
    <style>
    .hero-select-card { margin: 1.25rem auto 0 auto; padding: 20px 22px; border-radius: 20px; }
    .hero-select-card .stSelectbox * { color-scheme: dark; }
    .hero-select-card .stSelectbox > div > div,
    .hero-select-card .stSelectbox div[data-baseweb="select"] > div { background: rgba(255,255,255,0.08) !important; border: 2px solid rgba(255,255,255,0.18) !important; border-radius: 14px !important; box-shadow: 0 8px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.15) !important; }
    .hero-select-card .stSelectbox div[role="combobox"] { padding: 14px 16px !important; color: #e9eefc !important; font-weight: 500; }
    .hero-select-card .stSelectbox div[data-baseweb="select"] input { color: #e9eefc !important; background: transparent !important; caret-color: #e9eefc !important; }
    .hero-select-card .stSelectbox svg { color: #a0b3ff !important; }
    .hero-select-card .stSelectbox > div > div:hover { border-color: rgba(102,126,234,0.65) !important; }
    .hero-select-card .stSelectbox > div > div:focus-within { box-shadow: 0 0 0 3px rgba(79,172,254,0.25), 0 12px 32px rgba(79,172,254,0.25) !important; border-color: rgba(79,172,254,0.8) !important; }
    .hero-select-card .stSelectbox div[role="listbox"],
    .hero-select-card .stSelectbox ul[role="listbox"] { background: rgba(7, 11, 26, 0.98) !important; border: 1px solid rgba(255,255,255,0.18) !important; }
    .hero-select-card .stSelectbox [role="option"] { color: #e9eefc !important; }
    .hero-select-card .stSelectbox [role="option"][aria-selected="true"] { background: rgba(102, 126, 234, 0.25) !important; }
    .hero-select-card .stSelectbox [role="option"]:hover { background: rgba(79, 172, 254, 0.25) !important; }
    @media (prefers-color-scheme: light) {
        .hero-select-card .stSelectbox div[data-baseweb="select"] > div,
        .hero-select-card .stSelectbox div[role="listbox"],
        .hero-select-card .stSelectbox ul[role="listbox"] { background: rgba(7, 11, 26, 0.98) !important; color: #e9eefc !important; }
    }
    </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="glow-card floating hero-select-card">\n  <h3 style="margin:0 0 8px 0;">🌍 SELECT YOUR DESTINATION</h3>', unsafe_allow_html=True)
        selected_city = st.selectbox(
            " ",
            options=list(WORLD_CITIES.keys()),
            index=0,
            key="city_selector",
            placeholder="Search or pick a city...",
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Get coordinates
    lat, lon = WORLD_CITIES[selected_city]
    
    # Loading animation
    weather_data = None
    with st.spinner('🚀 Fetching elite weather data from satellites...'):
        try:
            weather_data = fetch_weather_data(lat, lon)
        except Exception as e:
            st.error(f"⚠️ Unable to fetch weather data: {str(e)}")
            st.stop()
    
    if weather_data is None:
        st.stop()
        return
    
    # Extract current weather
    current = weather_data['current']
    hourly = weather_data['hourly']
    daily = weather_data['daily']
    
    # Current weather metrics
    current_temp = current['temperature_2m']
    feels_like = current['apparent_temperature']
    humidity = current['relative_humidity_2m']
    pressure = current['surface_pressure']
    wind_speed = current['wind_speed_10m']
    wind_direction = current['wind_direction_10m']
    wind_gusts = current['wind_gusts_10m']
    weather_code = current['weather_code']
    
    # Get weather condition
    icon, condition, color = WEATHER_CONDITIONS.get(weather_code, ("❓", "Unknown", "#888888"))
    
    st.markdown("---")
    
    # Current Weather Hero Section
    st.markdown(f"""
    <div class="glow-card" style="text-align: center; margin: 2rem 0;">
        <div class="weather-icon" style="color: {color}; margin-bottom: 1rem;">{icon}</div>
        <h2 style="color: white; margin-bottom: 0.5rem; font-family: 'Orbitron';">{selected_city.replace('🏙️ ', '').replace('🌉 ', '').replace('🗼 ', '').replace('🏯 ', '').replace('🌊 ', '').replace('🏗️ ', '').replace('🌆 ', '').replace('🌴 ', '').replace('🌁 ', '').replace('⛰️ ', '').replace('🏔️ ', '').replace('🏛️ ', '').replace('🏖️ ', '').replace('🌸 ', '')}</h2>
        <h3 style="color: {color}; margin: 0;">{condition}</h3>
        <p style="color: #a8b2d1; margin-top: 1rem;">Last Updated: {datetime.now().strftime('%I:%M %p')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown('<div class="glow-card floating">', unsafe_allow_html=True)
        st.metric(
            label="🌡️ Temperature",
            value=f"{current_temp:.1f}°C",
            delta=f"Feels {feels_like:.1f}°C"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown('<div class="glow-card floating">', unsafe_allow_html=True)
        st.metric(
            label="💧 Humidity",
            value=f"{humidity:.0f}%",
            delta="Optimal" if 40 <= humidity <= 60 else "High" if humidity > 60 else "Low"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown('<div class="glow-card floating">', unsafe_allow_html=True)
        st.metric(
            label="💨 Wind Speed",
            value=f"{wind_speed:.1f} km/h",
            delta=f"Gusts {wind_gusts:.1f} km/h"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown('<div class="glow-card floating">', unsafe_allow_html=True)
        st.metric(
            label="🌪️ Pressure",
            value=f"{pressure:.0f} hPa",
            delta="Normal" if 1013-20 <= pressure <= 1013+20 else "High" if pressure > 1013+20 else "Low"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Advanced Visualizations Row 1
    viz_col1, viz_col2, viz_col3 = st.columns([1, 1, 1])
    
    with viz_col1:
        st.markdown('<div class="glow-card">\n  <h3 style="margin-top:0;">🌡️ Temperature</h3>', unsafe_allow_html=True)
        temp_gauge = create_temperature_gauge(current_temp, feels_like)
        st.plotly_chart(temp_gauge, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_col2:
        st.markdown('<div class="glow-card">\n  <h3 style="margin-top:0;">🧭 Wind Direction</h3>', unsafe_allow_html=True)
        wind_compass = create_wind_compass(wind_speed, wind_direction)
        st.plotly_chart(wind_compass, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_col3:
        st.markdown('<div class="glow-card">\n  <h3 style="margin-top:0;">😊 Weather Mood</h3>', unsafe_allow_html=True)
        mood_indicator = create_weather_mood_indicator(weather_code, current_temp, humidity)
        st.plotly_chart(mood_indicator, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced Visualizations Row 2
    viz_col4, viz_col5 = st.columns([1, 1])
    
    with viz_col4:
        st.markdown('<div class="glow-card">\n  <h3 style="margin-top:0;">🔥 48-Hour Temperature Heatmap</h3>', unsafe_allow_html=True)
        heatmap = create_hourly_forecast_heatmap(hourly)
        st.plotly_chart(heatmap, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_col5:
        st.markdown('<div class="glow-card">\n  <h3 style="margin-top:0;">☔ 7-Day Precipitation Radar</h3>', unsafe_allow_html=True)
        precip_radar = create_precipitation_radar(daily)
        st.plotly_chart(precip_radar, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Comprehensive Timeline
    st.markdown('<div class="glow-card" style="margin-top: 2rem;">\n  <h3 style="margin-top:0;">📊 72-Hour Analytics</h3>', unsafe_allow_html=True)
    timeline = create_multi_metric_timeline(hourly)
    st.plotly_chart(timeline, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Weather Insights & Alerts
    insights = []

    # Temperature insights
    if current_temp > 30:
        insights.append("🔥 **Heat Alert**: Very hot conditions! Stay hydrated and seek shade.")
    elif current_temp < 0:
        insights.append("🧊 **Cold Alert**: Freezing temperatures! Bundle up and watch for ice.")
    elif 20 <= current_temp <= 25:
        insights.append("🌿 **Perfect Weather**: Ideal temperature for outdoor activities!")

    # Wind insights
    if wind_speed > 30:
        insights.append("💨 **Wind Warning**: Strong winds detected! Secure loose objects.")
    elif wind_speed < 5:
        insights.append("🍃 **Calm Conditions**: Very light winds, perfect for outdoor dining.")

    # Humidity insights
    if humidity > 80:
        insights.append("💧 **High Humidity**: Muggy conditions, feels warmer than actual temperature.")
    elif humidity < 30:
        insights.append("🏜️ **Low Humidity**: Dry air, consider using moisturizer and staying hydrated.")

    # Pressure insights
    if pressure < 1000:
        insights.append("📉 **Low Pressure**: Weather changes likely, possible storms approaching.")
    elif pressure > 1030:
        insights.append("📈 **High Pressure**: Stable, clear weather conditions expected.")

    # UV insights
    max_uv_today = daily['uv_index_max'][0] if daily['uv_index_max'] else 0
    if max_uv_today > 8:
        insights.append("☀️ **UV Warning**: Very high UV index! Use SPF 30+ sunscreen.")
    elif max_uv_today > 5:
        insights.append("🕶️ **UV Caution**: Moderate to high UV levels, wear sunglasses.")

    # Precipitation insights
    rain_today = daily['precipitation_probability_max'][0] if daily['precipitation_probability_max'] else 0
    if rain_today > 70:
        insights.append("☔ **Rain Alert**: High chance of rain today, carry an umbrella!")
    elif rain_today < 20:
        insights.append("☀️ **Dry Day**: Low chance of rain, perfect for outdoor plans!")

    insight_items = "".join(f"<li>{ins}</li>" for ins in insights[:5]) if insights else "<li>🌤️ <b>Normal Conditions</b>: Weather conditions are within typical ranges.</li>"

    st.markdown(f'''
<div class="glow-card" style="margin-top: 2rem;">
  <h2 style="margin-top:0;">🤖 AI WEATHER INSIGHTS</h2>
  <ul style="margin-bottom:0;">
    {insight_items}
  </ul>
</div>
''', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a8b2d1; margin: 2rem 0;">
        <h4 style="color: white; margin-bottom: 1rem;">⚡ ELITE WEATHER HUB ⚡</h4>
        <p>Powered by cutting-edge weather APIs and advanced data visualization</p>
        <p>Real-time data • Predictive analytics • Beautiful insights</p>
        <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.7;">
            Data provided by Open-Meteo | Visualizations by Plotly | Built with Streamlit ❤️
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()