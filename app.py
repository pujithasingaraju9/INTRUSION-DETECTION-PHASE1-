import streamlit as st
import pandas as pd
import packet_capture
from datetime import datetime
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="DARKSHIELD Threat Intel", layout="wide")

# --- SESSION STATE INIT ---
if "started" not in st.session_state:
    st.session_state.started = False

if "history" not in st.session_state:
    st.session_state.history = {
        "attacks": [],
        "normal": [],
        "time": []
    }

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
}
.status-online {
    color: #00ffc3;
    font-size: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2, col3 = st.columns([2,5,2])

with col1:
    st.markdown("### 🛡️ DARKSHIELD")
    st.caption("THREAT INTELLIGENCE v2.0")

with col3:
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    st.markdown(
        f"<p class='status-online'>● ACTIVE THREAT | ● AI ONLINE | {current_time}</p>",
        unsafe_allow_html=True
    )

st.divider()

# --- START BUTTON ---
if st.button("Start Network Monitoring") and not st.session_state.started:
    packet_capture.run_sniffer()
    st.session_state.started = True
    st.success("🚀 Monitoring Started!")

if st.session_state.started:
    st.info("🟢 Live Monitoring Running...")

st.divider()

# --- UPDATE HISTORY ---
if st.session_state.started:
    st.session_state.history["attacks"].append(packet_capture.stats["attack"])
    st.session_state.history["normal"].append(packet_capture.stats["normal"])
    st.session_state.history["time"].append(datetime.now().strftime("%H:%M:%S"))

    # Limit to last 20 points
    if len(st.session_state.history["attacks"]) > 20:
        st.session_state.history["attacks"].pop(0)
        st.session_state.history["normal"].pop(0)
        st.session_state.history["time"].pop(0)

# --- METRICS ---
m1, m2, m3, m4 = st.columns(4)

metrics = [
    ("Active Threats", str(packet_capture.stats["attack"])),
    ("Normal Traffic", str(packet_capture.stats["normal"])),
    ("DoS Attacks", str(packet_capture.attack_counts["DoS"])),
    ("Probe Attacks", str(packet_capture.attack_counts["Probe"]))
]

for i, col in enumerate([m1, m2, m3, m4]):
    with col:
        st.markdown(f"""
        <div class="css-card">
            <div style="font-size:12px;color:#8b949e;">{metrics[i][0]}</div>
            <div style="font-size:28px;font-weight:bold;">{metrics[i][1]}</div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
col_left, col_mid, col_right = st.columns([1.5,3.5,1.5])

# LEFT: Threat Categories
with col_left:
    st.markdown("### THREAT CATEGORIES")

    for cat, val in packet_capture.attack_counts.items():
        st.write(f"**{val}** {cat}")
        st.progress(min(val/50, 1.0))

# MIDDLE: LIVE GRAPH
with col_mid:
    st.markdown("### 📈 Live Attack Trend")

    if st.session_state.history["attacks"]:
        chart_data = pd.DataFrame({
            "Attacks": st.session_state.history["attacks"],
            "Normal": st.session_state.history["normal"]
        }, index=st.session_state.history["time"])

        st.line_chart(chart_data)
    else:
        st.write("Waiting for data...")

    st.markdown("### 🧠 AI CLASSIFIER STATUS")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Confidence", "96.6%", "High")
    c2.metric("Model", "Random Forest", "Stable")
    c3.metric("Risk Score", "4.1/10", "-0.2")
    c4.metric("Detection Rate", "87.3%", "Active")

# RIGHT: Alerts
with col_right:
    st.markdown("### 🚨 LIVE ALERTS")

    if packet_capture.alerts:
        for alert in packet_capture.alerts[-10:]:
            st.write(alert)
    else:
        st.write("No alerts yet.")

# --- EVENT LOG ---
st.markdown("### 📜 EVENT LOG")

st.write(f"Packets → Normal: {packet_capture.stats['normal']} | Attacks: {packet_capture.stats['attack']}")

log_data = pd.DataFrame([
    {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Event": "Monitoring Active",
        "Status": "Running"
    }
])

st.table(log_data)

# --- AUTO REFRESH ---
time.sleep(2)
st.rerun()
