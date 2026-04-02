from scapy.all import sniff
import threading

# ✅ GLOBAL VARIABLES (must exist)
alerts = []
stats = {"normal": 0, "attack": 0}

# Dummy predict (for testing if model not loaded yet)
def predict(features):
    return "attack" if sum(features) % 2 == 0 else "normal"

def extract_features(packet):
    try:
        return [
            len(packet),
            packet.proto if hasattr(packet, 'proto') else 0,
            1 if packet.haslayer('TCP') else 0,
            1 if packet.haslayer('UDP') else 0,
            1 if packet.haslayer('ICMP') else 0
        ]
    except:
        return [0, 0, 0, 0, 0]

def process_packet(packet):
    features = extract_features(packet)
    result = predict(features)

    if result == "normal":
        stats["normal"] += 1
    else:
        stats["attack"] += 1
        alert_msg = f"🚨 {result} attack detected!"
        alerts.append(alert_msg)

def start_sniffing():
    sniff(prn=process_packet, store=False)

# ✅ REQUIRED FUNCTION
def run_sniffer():
    thread = threading.Thread(target=start_sniffing)
    thread.daemon = True
    thread.start()