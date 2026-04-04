import streamlit as st
import pandas as pd
import random
import packet_capture
from datetime import datetime
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="DARKSHIELD Threat Intel", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS ---
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

# --- HEADER ---
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

# ✅ SESSION STATE
if "started" not in st.session_state:
    st.session_state.started = False

# ✅ START BUTTON
if st.button("Start Network Monitoring") and not st.session_state.started:
    packet_capture.run_sniffer()
    st.session_state.started = True
    st.success("Monitoring Started!")

# ✅ STATUS
if st.session_state.started:
    st.info("🟢 Monitoring is running...")

st.divider()

# --- METRICS ---
m1, m2, m3, m4 = st.columns(4)

metrics = [
    ("Active Threats", str(packet_capture.stats["attack"]), "#ff3366"),
    ("Brute Force", "515", "#f1c40f"),
    ("IPS Blocked", "12.4K", "#3498db"),
    ("Dark Mentions", "89", "#2ecc71")
]

for i, col in enumerate([m1, m2, m3, m4]):
    with col:
        st.markdown(f"""
        <div class="css-card">
            <div class="metric-label">{metrics[i][0]}</div>
            <div style="color:{metrics[i][2]}; font-size: 28px; font-weight: bold;">
                {metrics[i][1]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
col_left, col_mid, col_right = st.columns([1.5, 3.5, 1.5])

# LEFT PANEL
with col_left:
    st.markdown("#### THREAT CATEGORIES")
    categories = {
        "Credential Stuffing": 234,
        "Tor Exit Attacks": 187,
        "Password Spray": 141,
        "Ransomware C2": 98,
        "Data Exfil Attempt": 54,
        "DotWeb Scanner": 51
    }

    for cat, val in categories.items():
        st.write(f"**{val}** {cat}")
        st.progress(val / 250)

# MIDDLE PANEL (REPLACED GRAPH)
with col_mid:
    st.markdown("#### 📡 Live Attack Visualization")

    chart_data = pd.DataFrame({
        "Normal Traffic": [packet_capture.stats["normal"] + random.randint(0, 5) for _ in range(10)],
        "Attack Traffic": [packet_capture.stats["attack"] + random.randint(0, 5) for _ in range(10)]
    })

    st.line_chart(chart_data)

    st.markdown("#### AI BRUTE FORCE CLASSIFIER")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("LSTM Score", "96.6%", "High")
    c2.metric("Random Forest", "97.2%", "Stable")
    c3.metric("IP Reputation", "4.1/10", "-0.2")
    c4.metric("Correlation", "87.3%", "Active")

# RIGHT PANEL
with col_right:
    st.markdown("#### DARKWEB INTEL FEED")

    feeds = [
        ("NYXRA MAGNET DEC LEAKED", "Critical"),
        ("BREACH FORUM 0X2 INTEL", "High"),
        ("ORION PASTE D&C SCAN", "Med"),
    ]

    for title, sev in feeds:
        st.markdown(f"""
        <div style="font-size: 12px; margin-bottom: 10px; border-left: 3px solid #ff3366; padding-left: 5px;">
            <b>{title}</b><br>
            <span style="color: grey;">Severity: {sev}</span>
        </div>
        """, unsafe_allow_html=True)

# --- LIVE EVENT STREAM ---
st.markdown("#### // LIVE EVENT STREAM")

if packet_capture.alerts:
    for alert in packet_capture.alerts[-10:]:
        st.write(alert)
else:
    st.write("No alerts yet.")

st.markdown(
    f"**Packets Analyzed:** Normal: {packet_capture.stats['normal']}, "
    f"Attacks: {packet_capture.stats['attack']}"
)

log_data = pd.DataFrame([
    {"Time": "22:11:58", "Event": "BRUTE FORCE", "IP": "185.220.101.33", "Status": "BLOCKED"},
    {"Time": "22:11:54", "Event": "MODEL RETRAINED", "IP": "AI ENGINE", "Status": "SUCCESS"},
    {"Time": "22:11:52", "Event": "RANSOMWARE C2", "IP": "155.133.245.98", "Status": "MATCHED"},
])

st.table(log_data)

# 🔥 AUTO REFRESH ONLY WHEN RUNNING
if st.session_state.started:
    time.sleep(2)
    st.rerun()
