import streamlit as st
import pandas as pd
import random
from streamlit_echarts import st_echarts
import packet_capture
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# 🔥 AUTO REFRESH EVERY 2 SECONDS
st_autorefresh(interval=2000, key="refresh")

# --- PAGE CONFIG ---
st.set_page_config(page_title="DARKSHIELD Threat Intel", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FOR DARK THEME ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #00ffc3;
    }
    .css-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .metric-val {
        font-size: 24px;
        font-weight: bold;
        color: #ff3366;
    }
    .metric-label {
        font-size: 12px;
        color: #8b949e;
        text-transform: uppercase;
    }
    .status-online {
        color: #00ffc3;
        font-size: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_h1, col_h2, col_h3 = st.columns([2, 5, 2])
with col_h1:
    st.markdown("### 🛡️ DARKSHIELD")
    st.caption("THREAT INTELLIGENCE v2.0")

with col_h3:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(
        f"<p class='status-online'>● ACTIVE THREAT | ● AI ONLINE | {current_time}</p>",
        unsafe_allow_html=True
    )

st.divider()

# Start Packet Sniffing
if st.button("Start Network Monitoring"):
    packet_capture.run_sniffer()
    st.success("Network monitoring started!")

st.divider()

# --- METRICS ---
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("Active Threats", "633", "#ff3366"),
    ("Brute Force", "515", "#f1c40f"),
    ("IPS Blocked", "12.4K", "#3498db"),
    ("Dark Mentions", "89", "#2ecc71")
]

for i, col in enumerate([m1, m2, m3, m4]):
    with col:
        st.markdown(f"""
        <div class="css-card">
