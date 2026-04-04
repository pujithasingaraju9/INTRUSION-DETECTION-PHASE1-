import pandas as pd

columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label","difficulty"
]

# 🔥 Load only small part (FAST)
data = pd.read_csv("dataset/KDDTrain+.txt", names=columns, nrows=5000)

# Select required features
data = data[[
    "src_bytes", "dst_bytes", "count", "srv_count", "serror_rate", "label"
]]

# Rename
data.columns = ["packet_size", "protocol", "tcp", "udp", "icmp", "label"]

# Convert labels
data["label"] = data["label"].apply(lambda x: "normal" if x == "normal" else "attack")

# Save
data.to_csv("dataset/data.csv", index=False)

print("✅ Small dataset ready!")
