import threading
import random
import time

# 🔥 GLOBAL DATA (shared with Streamlit)
alerts = []
stats = {"normal": 0, "attack": 0}

attack_counts = {
    "DoS": 0,
    "Probe": 0,
    "R2L": 0,
    "U2R": 0
}

attack_types = ["DoS", "Probe", "R2L", "U2R"]

running = False  # control flag


# 🔥 BACKGROUND TRAFFIC GENERATOR
def generate_traffic():
    global running

    while running:
        time.sleep(2)  # ⏱️ update every 2 seconds

        # 40% attack chance
        if random.random() > 0.6:
            attack = random.choice(attack_types)

            stats["attack"] += 1
            attack_counts[attack] += 1

            alerts.append(f"🚨 {attack} attack detected!")

        else:
            stats["normal"] += 1


# 🔥 START FUNCTION (RUNS ONCE)
def run_sniffer():
    global running

    if not running:
        running = True
        thread = threading.Thread(target=generate_traffic)
        thread.daemon = True
        thread.start()
