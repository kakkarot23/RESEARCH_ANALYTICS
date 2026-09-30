import os
import numpy as np
import pandas as pd

def generate_tellco_data(num_records=12000, seed=42):
    np.random.seed(seed)
    
    # 1. User IDs (MSISDNs) - around 3000 unique users
    num_users = 3500
    user_pool = [f"336{np.random.randint(10000000, 99999999)}" for _ in range(num_users)]
    msisdn = np.random.choice(user_pool, size=num_records)
    bearer_ids = [f"1318615000000000{np.random.randint(10000, 99999)}" for _ in range(num_records)]
    
    # 2. Handsets and Manufacturers
    manufacturers = ["Apple", "Samsung", "Huawei", "Xiaomi", "OPPO", "ZTE"]
    mfg_weights = [0.40, 0.35, 0.15, 0.05, 0.03, 0.02]
    
    handset_map = {
        "Apple": ["iPhone 11 Pro", "iPhone 12", "iPhone XS", "iPhone 11", "iPhone 8"],
        "Samsung": ["Galaxy S10", "Galaxy A50", "Galaxy Note 10", "Galaxy S20", "Galaxy A10"],
        "Huawei": ["Honor 8X", "Mate 20 Lite", "P30 Lite", "P20 Lite", "Y7 Prime"],
        "Xiaomi": ["Redmi Note 8", "Redmi 7", "Mi 9T", "Redmi Note 7", "Mi A3"],
        "OPPO": ["A5", "F11 Pro", "Reno 2", "A9", "A3s"],
        "ZTE": ["Blade V10", "Blade A5", "Axon 10 Pro", "Blade L8", "Blade V9"]
    }
    
    mfg_list = np.random.choice(manufacturers, size=num_records, p=mfg_weights)
    handset_list = [np.random.choice(handset_map[m]) for m in mfg_list]
    
    # 3. Session Durations (ms)
    durations = np.random.exponential(scale=85000, size=num_records) + 5000
    
    # 4. Network Metrics
    tcp_dl_retrans = np.random.exponential(scale=2000000, size=num_records)
    tcp_ul_retrans = np.random.exponential(scale=150000, size=num_records)
    
    rtt_dl = np.random.gamma(shape=2, scale=30, size=num_records) + 5
    rtt_ul = np.random.gamma(shape=1.5, scale=10, size=num_records) + 2
    
    throughput_dl = np.random.lognormal(mean=7.5, sigma=1.0, size=num_records)  # kbps
    throughput_ul = np.random.lognormal(mean=5.5, sigma=0.8, size=num_records)  # kbps
    
    # 5. App Data (DL and UL in Bytes)
    apps = {
        "Social Media": (500000, 3000000),
        "Google": (1000000, 8000000),
        "Email": (200000, 1500000),
        "Youtube": (3000000, 25000000),
        "Netflix": (2500000, 20000000),
        "Gaming": (5000000, 45000000),
        "Other": (1000000, 10000000)
    }
    
    app_data = {}
    for app_name, (loc, scale) in apps.items():
        dl = np.random.exponential(scale=scale, size=num_records) + loc
        ul = np.random.exponential(scale=scale * 0.2, size=num_records) + loc * 0.1
        app_data[f"{app_name} DL (Bytes)"] = dl
        app_data[f"{app_name} UL (Bytes)"] = ul
        
    total_dl = sum(app_data[f"{app_name} DL (Bytes)"] for app_name in apps)
    total_ul = sum(app_data[f"{app_name} UL (Bytes)"] for app_name in apps)
    
    df = pd.DataFrame({
        "Bearer Id": bearer_ids,
        "MSISDN/Number": msisdn,
        "Handset Manufacturer": mfg_list,
        "Handset Type": handset_list,
        "Dur. (ms)": durations,
        "TCP DL Retrans. Vol (Bytes)": tcp_dl_retrans,
        "TCP UL Retrans. Vol (Bytes)": tcp_ul_retrans,
        "Avg RTT DL (ms)": rtt_dl,
        "Avg RTT UL (ms)": rtt_ul,
        "Avg Bearer TP DL (kbps)": throughput_dl,
        "Avg Bearer TP UL (kbps)": throughput_ul,
        **app_data,
        "Total DL (Bytes)": total_dl,
        "Total UL (Bytes)": total_ul
    })
    
    # Introduce ~3% missing values randomly for real-world missing data handling test
    mask_mfg = np.random.rand(num_records) < 0.02
    df.loc[mask_mfg, "Handset Manufacturer"] = np.nan
    mask_type = np.random.rand(num_records) < 0.02
    df.loc[mask_type, "Handset Type"] = np.nan
    
    num_cols = ["TCP DL Retrans. Vol (Bytes)", "Avg RTT DL (ms)", "Avg Bearer TP DL (kbps)"]
    for col in num_cols:
        mask = np.random.rand(num_records) < 0.03
        df.loc[mask, col] = np.nan
        
    # Introduce intentional outliers
    df.loc[0, "Dur. (ms)"] = 15000000
    df.loc[1, "Total DL (Bytes)"] = 500000000000
    
    out_dir = os.path.join("d:/PROJECT 1", "data")
    os.makedirs(out_dir, exist_ok=True)
    file_path = os.path.join(out_dir, "telecom_xDR_data.csv")
    df.to_csv(file_path, index=False)
    print(f"Generated dataset with {len(df)} rows and saved to {file_path}")
    return file_path

if __name__ == "__main__":
    generate_tellco_data()
