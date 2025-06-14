import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

# Hàm chuyển đổi dB sang tuyến tính
def db_to_linear(db_value):
    return 10 ** (db_value / 10)

# Hàm chuyển đổi tuyến tính sang dB
def linear_to_db(linear_value):
    if linear_value <= 0:
        return float('-inf')
    return 10 * math.log10(linear_value)

# Hàm tạo kênh fading Rayleigh với suy hao đường truyền
def generate_channel_gain(d, theta, size):
    # h0 = np.sqrt(np.random.exponential(scale=1.0, size=size))  # Thành phần fading Rayleigh
    # Sửa: Generate Rayleigh coefficient directly, squared magnitude follows exponential
    h0_squared = np.random.exponential(scale=1.0, size=size) # |h0|^2 follows exponential with mean 1

    # Tính suy hao đường truyền
    path_loss = d ** theta

    # Tính độ lợi kênh TỔNG (bao gồm fading và pathloss)
    # Độ lợi kênh = Fading Gain / Path Loss
    channel_gain_squared = h0_squared / path_loss

    return channel_gain_squared

# Tham số mô phỏng
n_realizations = 100000  # Số lần thực hiện Monte Carlo, tăng để cải thiện độ chính xác (có thể thay đổi: 1000-100000)
P_total = 1  # Tổng công suất truyền (chuẩn hóa), có thể thay đổi để điều chỉnh năng lượng hệ thống 5G (1.0-10)
N0_base = 1e-9  # Mức nhiễu nền ban đầu (chuẩn hóa), điều chỉnh để thay đổi điều kiện nhiễu (-20 đến 0 dB)
N0_db = linear_to_db(N0_base)  # Chuyển nhiễu nền sang tuyến tính

# User distances and path loss
d1 = 50  # Khoảng cách từ trạm gốc đến UE1 (xa) tính bằng mét, thay đổi để mô phỏng khoảng cách khác (100-1000m)
d2 = 150  # Khoảng cách từ trạm gốc đến UE2 (gần) tính bằng mét, thay đổi để mô phỏng khoảng cách khác (50-500m)
theta = 3.0  # Hệ số suy hao đường truyền, điều chỉnh theo môi trường (2.0 cho thành phố, 3.0-4.0 cho nông thôn)

# Power allocation
alpha = 0.7    # Hệ số phân bổ công suất cho UE1 (xa), điều chỉnh để ưu tiên UE1 (0.5-0.9)
P1 = alpha * P_total  # Công suất cho UE1 (xa), tự động tính dựa trên alpha
P2 = (1 - alpha) * P_total  # Công suất cho UE2 (gần), tự động tính dựa trên alpha

# SINR thresholds
Gamma1_db = 5  # Ngưỡng SINR cho UE1 (xa) tính bằng dB, thay đổi để điều chỉnh yêu cầu chất lượng (0-8 dB)
Gamma2_db = 10 # Ngưỡng SINR cho UE2 (gần) tính bằng dB, thay đổi để điều chỉnh yêu cầu chất lượng (5-10 dB < Tầng phát nguồn)
Gamma1_linear = db_to_linear(Gamma1_db)  # Chuyển ngưỡng UE1 sang tuyến tính
Gamma2_linear = db_to_linear(Gamma2_db)  # Chuyển ngưỡng UE2 sang tuyến tính

# SNR range for analysis
snr_db_range = np.arange(0, 31, 5)  # SNR range from 0 to 30 dB in steps of 5 dB
throughput_stats = []

# Analyze performance for different SNR values
for snr_db in snr_db_range:
    # Calculate noise power for current SNR
    snr_linear = db_to_linear(snr_db)
    N0_sim = P_total / snr_linear if snr_linear > 0 else float('inf')
    
    # Generate channel gains with path loss
    h1_sq = (d1**(-theta)) * np.random.exponential(scale=1.0, size=n_realizations)
    h2_sq = (d2**(-theta)) * np.random.exponential(scale=1.0, size=n_realizations)
    
    # Calculate SINRs
    sinr_ue1 = (P1 * h1_sq) / (P2 * h1_sq + N0_sim)
    sinr_ue2_to1 = (P1 * h2_sq) / (P2 * h2_sq + N0_sim)
    sinr_ue2_to2 = (P2 * h2_sq) / N0_sim
    
    # Calculate throughputs
    throughput_ue1 = np.log2(1 + sinr_ue1)
    throughput_ue2 = np.log2(1 + sinr_ue2_to2)
    throughput_oma = 0.5 * (np.log2(1 + (P_total * h1_sq / N0_sim)) + 
                           np.log2(1 + (P_total * h2_sq / N0_sim)))
    
    # Calculate statistics
    avg_throughput_ue1 = np.mean(throughput_ue1)
    avg_throughput_ue2 = np.mean(throughput_ue2)
    avg_throughput_noma = avg_throughput_ue1 + avg_throughput_ue2
    avg_throughput_oma = np.mean(throughput_oma)
    
    # Calculate outage probabilities
    outage_ue1 = np.sum(sinr_ue1 < Gamma1_linear) / n_realizations
    outage_ue2 = (np.sum(sinr_ue2_to1 < Gamma1_linear) + 
                 np.sum((sinr_ue2_to1 >= Gamma1_linear) & (sinr_ue2_to2 < Gamma2_linear))) / n_realizations
    
    # Store statistics
    throughput_stats.append({
        'SNR_dB': snr_db,
        'NOMA_UE1': avg_throughput_ue1,
        'NOMA_UE2': avg_throughput_ue2,
        'NOMA_Total': avg_throughput_noma,
        'OFDMA': avg_throughput_oma,
        'Outage_UE1': outage_ue1,
        'Outage_UE2': outage_ue2
    })

# Convert to DataFrame for better analysis
df_stats = pd.DataFrame(throughput_stats)

# Display detailed statistics
print("\n==================================================")
print("===== Detailed Throughput Statistics =====")
print("==================================================")
print("\nThroughput Statistics by SNR:")
print(df_stats.round(4))

# Calculate summary statistics
print("\nSummary Statistics:")
print(f"Maximum NOMA Throughput: {df_stats['NOMA_Total'].max():.4f} bits/s/Hz at {df_stats.loc[df_stats['NOMA_Total'].idxmax(), 'SNR_dB']} dB")
print(f"Maximum OFDMA Throughput: {df_stats['OFDMA'].max():.4f} bits/s/Hz at {df_stats.loc[df_stats['OFDMA'].idxmax(), 'SNR_dB']} dB")
print(f"Average Throughput Gain: {((df_stats['NOMA_Total'] / df_stats['OFDMA'])-1).mean() * 100:.2f}%")

# Plot results
plt.figure(figsize=(15, 10))

# Plot 1: Throughput vs SNR
plt.subplot(2, 2, 1)
plt.plot(df_stats['SNR_dB'], df_stats['NOMA_UE1'], 'b-', label='NOMA UE1 (Near)')
plt.plot(df_stats['SNR_dB'], df_stats['NOMA_UE2'], 'r-', label='NOMA UE2 (Far)')
plt.plot(df_stats['SNR_dB'], df_stats['NOMA_Total'], 'g-', label='NOMA Total')
plt.plot(df_stats['SNR_dB'], df_stats['OFDMA'], 'k--', label='OFDMA')
plt.xlabel('SNR (dB)')
plt.ylabel('Throughput (bits/s/Hz)')
plt.title('Throughput vs SNR')
plt.legend()
plt.grid(True)

# Plot 2: Outage Probability vs SNR
plt.subplot(2, 2, 2)
plt.semilogy(df_stats['SNR_dB'], df_stats['Outage_UE1'], 'b-', label='UE1 (Near)')
plt.semilogy(df_stats['SNR_dB'], df_stats['Outage_UE2'], 'r-', label='UE2 (Far)')
plt.xlabel('SNR (dB)')
plt.ylabel('Outage Probability')
plt.title('Outage Probability vs SNR')
plt.legend()
plt.grid(True)

# Plot 3: Throughput Gain vs SNR
plt.subplot(2, 2, 3)
throughput_gain = (df_stats['NOMA_Total'] / df_stats['OFDMA'] - 1) * 100
plt.plot(df_stats['SNR_dB'], throughput_gain, 'g-')
plt.xlabel('SNR (dB)')
plt.ylabel('Throughput Gain (%)')
plt.title('NOMA vs OFDMA Throughput Gain')
plt.grid(True)

# Plot 4: Throughput Distribution at Maximum SNR
plt.subplot(2, 2, 4)
max_snr_idx = df_stats['SNR_dB'].idxmax()
throughput_data = [df_stats.loc[max_snr_idx, 'NOMA_UE1'],
                  df_stats.loc[max_snr_idx, 'NOMA_UE2'],
                  df_stats.loc[max_snr_idx, 'OFDMA']]
plt.bar(['NOMA UE1', 'NOMA UE2', 'OFDMA'], throughput_data)
plt.ylabel('Throughput (bits/s/Hz)')
plt.title(f'Throughput Distribution at {df_stats.loc[max_snr_idx, "SNR_dB"]} dB')
plt.grid(True)

plt.tight_layout()
plt.show()

# Save statistics to CSV
df_stats.to_csv('noma_throughput_statistics.csv', index=False)
print("\nStatistics have been saved to 'noma_throughput_statistics.csv'")