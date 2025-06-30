## Simulation Improvement-2
#Thêm $ R_s $ và $ \eta_s $:
# $ R_s = \max(0, \text{mean}(C_{AB}) - \text{mean}(C_{AE})) $.
# $ \eta_s = R_s / B $ với $ B = 10e6 $.

# Mô phỏng nghe lén chủ động: Thêm nhiễu giả mạo từ Eve, ví dụ: $ \text{SNR}_{\text{Eve}} += \text{noise\_eve} $ với $ \text{noise\_eve} \sim \mathcal{CN}(0, 0.1 \cdot P_A) $.
# Hiệu chỉnh $ \epsilon_S $: Điều chỉnh $ \epsilon_S = 50e3 / 10e6 = 0.005 \, \text{bits/s/Hz} $ để phù hợp với băng thông 10 MHz.
#  Tối ưu hóa: Giảm $ num_samples $ xuống 10^4 nếu cần, hoặc sử dụng vector hóa để tăng tốc.
import numpy as np
import matplotlib.pyplot as plt

# Thông số hệ thống
P_A = 1                     # Công suất truyền (W)
N_0 = 10**((-134 - 30) / 10) # Nhiễu nền thực tế (-164 dBm/Hz -> Watt)
alpha = 3                   # Hệ số suy hao
epsilon_S = 0.5             # Ngưỡng bảo mật (0.5 bits/s/Hz, điều chỉnh)
B = 10e6                    # Băng thông (10 MHz)
num_samples = int(1e4)      # Số mẫu mô phỏng
dE_range = np.linspace(100, 500, 50) # Khoảng cách Alice-Eve (m)

# Ba giá trị d_B tương ứng ba kịch bản
dB_values = [100, 50, 20]   # Khoảng cách Alice-Bob (m)
colors = ['g', 'b', 'r']
labels = [
    'd_B = 100 m (O_S ≈ 1)',
    'd_B = 50 m (O_S giảm)',
    'd_B = 20 m (O_S giảm gần 0)'
]
O_S = np.zeros((3, len(dE_range)))
R_s = np.zeros((3, len(dE_range)))
eta_s = np.zeros((3, len(dE_range)))

print("==== THÔNG SỐ HỆ THỐNG ====")
print(f"Công suất truyền P_A: {P_A} W")
print(f"Nhiễu nền N_0: {N_0:.2e} W")
print(f"Hệ số suy hao alpha: {alpha}")
print(f"Ngưỡng bảo mật epsilon_S: {epsilon_S:.4f} (bits/s/Hz)")
print(f"Băng thông: {B/1e6:.1f} MHz")
print(f"Khoảng cách d_B: {dB_values}")
print(f"Khoảng cách d_E: {dE_range[0]:.1f} -> {dE_range[-1]:.1f} m (step {dE_range[1]-dE_range[0]:.1f})")
print("============================\n")

# Mô phỏng cho từng kịch bản với nghe lén chủ động
for j in range(3):
    d_B = dB_values[j]
    print(f"\n--- Mô phỏng với d_B = {d_B} m ---")
    for i in range(len(dE_range)):
        d_E = dE_range[i]
        # Tạo kênh fading Rayleigh phức
        h_B = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        h_E = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))

        # Tính SNR với suy hao
        SNR_Bob = (P_A * np.abs(h_B)**2) / (d_B**alpha * N_0)
        SNR_Eve = (P_A * np.abs(h_E)**2) / (d_E**alpha * N_0)

        # Thêm nhiễu giả mạo từ Eve
        noise_eve = np.sqrt(0.3 * P_A) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        SNR_Eve += np.abs(noise_eve)**2 / N_0

        # Tính dung lượng kênh theo Shannon
        C_AB = B * np.log2(1 + SNR_Bob)
        C_AE = B * np.log2(1 + SNR_Eve)

        # Tính Secrecy Capacity và Secrecy Outage
        C_S = np.maximum(0, C_AB - C_AE)
        R_s[j, i] = np.mean(C_S) / B  # Secrecy Rate
        O_S[j, i] = np.mean(C_S < epsilon_S * B)  # Secrecy Outage Probability
        eta_s[j, i] = R_s[j, i]  # Secrecy Spectral Efficiency (bits/s/Hz)
        print(f"d_E = {d_E:.1f} m | O_S = {O_S[j, i]:.4f} | R_s = {R_s[j, i]:.4f} | eta_s = {eta_s[j, i]:.4f}")

# Vẽ đồ thị
plt.figure(figsize=(8, 6))

# Vùng màu bảo mật
plt.fill_between(np.concatenate((dE_range, dE_range[::-1])),
                 np.concatenate((np.ones(len(dE_range)) * 0.8, np.ones(len(dE_range)))),
                 color=[1, 0.8, 0.8], edgecolor='none', alpha=0.5)
plt.fill_between(np.concatenate((dE_range, dE_range[::-1])),
                 np.concatenate((np.ones(len(dE_range)) * 0.4, np.ones(len(dE_range)) * 0.8)),
                 color=[1, 1, 0.6], edgecolor='none', alpha=0.5)
plt.fill_between(np.concatenate((dE_range, dE_range[::-1])),
                 np.concatenate((np.zeros(len(dE_range)), np.ones(len(dE_range)) * 0.4)),
                 color=[0.8, 1, 0.8], edgecolor='none', alpha=0.5)

# Vẽ 3 đường xác suất
for j in range(3):
    plt.plot(dE_range, O_S[j, :], color=colors[j], linewidth=2, label=labels[j])

plt.annotate('Xu hướng giảm',
             xy=(float(np.mean(dE_range)), float(np.mean(O_S[0,:]))),
             xytext=(float(np.mean(dE_range)) - 100, float(np.mean(O_S[0,:])) + 0.2),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlabel('Khoảng cách từ A đến E (d_{AE}) (m)')
plt.ylabel('Xác suất dừng bảo mật O_S')
plt.title('Biểu diễn xác suất dừng với vùng màu và xu hướng')
plt.legend(loc='upper right')
plt.axhline(y=1, color='k', linestyle='--', label='O_S = 1')
plt.axhline(y=0.5, color='k', linestyle='--', label='O_S = 0.5')
plt.axhline(y=0, color='k', linestyle='--', label='O_S = 0')
plt.grid(True)
plt.show()

# Biểu đồ bổ sung cho R_s và eta_s
plt.figure(figsize=(8, 6))
for j in range(3):
    plt.plot(dE_range, R_s[j, :], color=colors[j], linewidth=2, label=labels[j] + ' R_s')
plt.xlabel('Khoảng cách từ A đến E (d_{AE}) (m)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Secrecy Rate theo khoảng cách d_{AE}')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
for j in range(3):
    plt.plot(dE_range, eta_s[j, :], color=colors[j], linewidth=2, label=labels[j] + ' eta_s')
plt.xlabel('Khoảng cách từ A đến E (d_{AE}) (m)')
plt.ylabel('Secrecy Spectral Efficiency (bits/s/Hz)')
plt.title('Secrecy Spectral Efficiency theo khoảng cách d_{AE}')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()