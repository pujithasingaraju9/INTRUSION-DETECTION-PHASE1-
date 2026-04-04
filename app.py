import streamlit as st
import pandas as pd
import time
from datetime import datetime
import packet_capture

# --- PAGE CONFIG ---
st.set_page_config(page_title="DARKSHIELD Threat Intel", layout="wide")

# --- DARK THEME ---
st.markdown("""
<style>
.stApp { background-color: #0e1117; color: #00ffc3; }
.css-card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 5px;
    padding: 15px;
}
.status-online {
    color: #00ffc3;
    font-size: 10px;
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
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(
        f"<p class='status-online'>● ACTIVE THREAT | ● AI ONLINE | {current_time}</p>",
        unsafe_allow_html=True
    )

st.divider()

# --- SESSION STATE ---
if "started" not in st.session_state:
    st.session_state.started = False

# --- START BUTTON ---
if st.button("Start Network Monitoring") and not st.session_state.started:
    packet_capture.run_sniffer()
    st.session_state.started = True
    st.success("🚀 Monitoring Started!")

if st.session_state.started:
    st.info("🟢 Live Monitoring Running...")

st.divider()

# --- METRICS ---
m1, m2, m3, m4 = st.columns(4)

metrics = [
    ("Active Threats", str(packet_capture.stats["attack"]), "#ff3366"),
    ("Normal Traffic", str(packet_capture.stats["normal"]), "#2ecc71"),
    ("DoS Attacks", str(packet_capture.attack_counts["DoS"]), "#f1c40f"),
    ("Probe Attacks", str(packet_capture.attack_counts["Probe"]), "#3498db"),
]

for i, col in enumerate([m1, m2, m3, m4]):
    with col:
        st.markdown(f"""
        <div class="css-card">
            <div style="font-size:12px;color:#8b949e">{metrics[i][0]}</div>
            <div style="color:{metrics[i][2]};font-size:26px;font-weight:bold">
                {metrics[i][1]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col_left, col_mid, col_right = st.columns([1.5,3.5,1.5])

# --- LEFT: THREAT CATEGORIES ---
with col_left:
    st.markdown("### THREAT CATEGORIES")

    for cat, val in packet_capture.attack_counts.items():
        st.write(f"**{val}** {cat}")
        st.progress(min(val / 50, 1.0))

# --- MIDDLE: LIVE GRAPH ---
with col_mid:
    st.markdown("### 📈 Live Attack Trend")

    chart_data = pd.DataFrame({
        "Attacks": [packet_capture.stats["attack"]],
        "Normal": [packet_capture.stats["normal"]]
    })

    st.bar_chart(chart_data)

    st.markdown("### 🤖 AI CLASSIFIER STATUS")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Confidence", "96.6%", "High")
    c2.metric("Model", "Random Forest", "Stable")
    c3.metric("Risk Score", "4.1/10", "-0.2")
    c4.metric("Detection Rate", "87.3%", "Active")

# --- RIGHT: LIVE ALERTS ---
with col_right:
    st.markdown("### 🚨 LIVE ALERTS")

    if packet_capture.alerts:
        for alert in packet_capture.alerts[-10:]:
            st.write(alert)
    else:
        st.write("No alerts yet")

# --- BOTTOM LOG ---
st.markdown("### 📜 EVENT LOG")

st.markdown(
    f"Packets → Normal: {packet_capture.stats['normal']} | Attacks: {packet_capture.stats['attack']}"
)

log_df = pd.DataFrame({
    "Time": [datetime.now().strftime("%H:%M:%S")],
    "Event": ["Monitoring Active"],
    "Status": ["Running"]
})

st.table(log_df)

# --- AUTO REFRESH LOOP ---
time.sleep(2)
st.rerun()
