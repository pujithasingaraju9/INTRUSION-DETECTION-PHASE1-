import threading
import random
import time
from model import predict

alerts = []
stats = {"normal": 0, "attack": 0}

# 🔥 Simulate realistic packet features
def extract_features():
    return [
        random.randint(20, 1500),   # packet size
        random.randint(1, 3),       # protocol
        random.randint(0, 1),       # TCP
        random.randint(0, 1),       # UDP
        random.randint(0, 1)        # ICMP
    ]

# 🔥 Simulate packet processing
def process_packet():
    features = extract_features()
    result = predict(features)

    # fallback if model not trained
    if result not in ["normal", "attack"]:
        result = "attack" if random.random() < 0.3 else "normal"

    if result == "normal":
        stats["normal"] += 1
    else:
        stats["attack"] += 1

        attack_types = [
            "Brute Force",
            "DDoS",
            "Port Scan",
            "SQL Injection",
            "Botnet Traffic"
        ]

        alerts.append(f"🚨 {random.choice(attack_types)} detected!")

# 🔁 Continuous simulation
def start_simulation():
    while True:
        process_packet()
        time.sleep(1)  # 1 packet per second

# ▶️ Start thread
def run_sniffer():
    thread = threading.Thread(target=start_simulation)
    thread.daemon = True
    thread.start()
