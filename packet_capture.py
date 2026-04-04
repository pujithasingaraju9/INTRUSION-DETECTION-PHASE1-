from scapy.all import sniff, get_if_list
import threading
from model import predict

alerts = []
stats = {"normal": 0, "attack": 0}

def extract_features(packet):
    try:
        return [
            len(packet),
            1 if packet.haslayer('TCP') else 2 if packet.haslayer('UDP') else 3,
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
        alerts.append(f"🚨 Attack detected!")

def start_sniffing():
    interfaces = get_if_list()
    print("Available Interfaces:", interfaces)

    sniff(prn=process_packet, store=False, iface=interfaces[0])  # 👈 important

def run_sniffer():
    thread = threading.Thread(target=start_sniffing)
    thread.daemon = True
    thread.start()
