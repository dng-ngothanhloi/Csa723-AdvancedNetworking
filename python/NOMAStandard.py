## Simulation Improvement-1
import numpy as np
import matplotlib.pyplot as plt

# Thông số hệ thống . Good Simulation cải tiến
#Suy hao $ d^\alpha $: Thêm $ d_B^\alpha $ và $ d_E^\alpha $ vào $ \text{SNR} $, phản ánh đúng mô hình suy hao đường truyền.
#Shannon Capacity: Sử dụng $ C_{AB} = 180e3 \cdot \log_2(1 + \text{SNR}_{\text{Bob}}) $ và $ C_{AE} = 180e3 \cdot \log_2(1 + \text{SNR}_{\text{Eve}}) $, thay cho ngưỡng tuyến tính.
#Nhiễu thực tế: $ N_0 = 10^{-14} \, \text{W} $ thay cho $ 10^{-3} \, \text{W} $, phù hợp với kịch bản không dây thực tế.
#Khoảng cách thực tế: $ d_E = 100-500 \, \text{m} $ và $ d_B = 100, 50, 20 \, \text{m} $, thay cho $ 0.1-5 \, \text{m} $, phù hợp với IoT nông nghiệp.
#Ngưỡng bảo mật: $ \epsilon_S = 50e3 / 180e3 $ (bits/s/Hz) thay cho 2, đảm bảo đơn vị nhất quán.

P_A = 1                     # Công suất truyền (W)
N_0 = 10**((-134 - 30) / 10) # Nhiễu nền thực tế (-134 dBm -> Watt)
alpha = 3                   # Hệ số suy hao
epsilon_S = 50e3 / 180e3    # Ngưỡng bảo mật (50 kbps / 180 kHz -> bits/s/Hz)
num_samples = int(1e5)      # Số mẫu mô phỏng
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

print("==== THÔNG SỐ HỆ THỐNG ====")
print(f"Công suất truyền P_A: {P_A} W")
print(f"Nhiễu nền N_0: {N_0:.2e} W")
print(f"Hệ số suy hao alpha: {alpha}")
print(f"Ngưỡng bảo mật epsilon_S: {epsilon_S:.4f} (bits/s/Hz)")
print(f"Băng thông: 180 kHz")
print(f"Khoảng cách d_B: {dB_values}")
print(f"Khoảng cách d_E: {dE_range[0]:.1f} -> {dE_range[-1]:.1f} m (step {dE_range[1]-dE_range[0]:.1f})")
print("============================\n")

# Mô phỏng cho từng kịch bản
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

        # Tính dung lượng kênh theo Shannon
        C_AB = 180e3 * np.log2(1 + SNR_Bob)
        C_AE = 180e3 * np.log2(1 + SNR_Eve)

        # Tính Secrecy Capacity và Secrecy Outage
        C_S = np.maximum(0, C_AB - C_AE)
        O_S[j, i] = np.mean(C_S < epsilon_S * 180e3)
        print(f"d_E = {d_E:.1f} m | O_S = {O_S[j, i]:.4f}")

# Vẽ đồ thị
plt.figure(figsize=(8, 6))

# Vùng màu bảo mật
plt.fill_between(np.concatenate((dE_range, dE_range[::-1])),
                 np.concatenate((np.ones(len(dE_range)) * 0.8, np.ones(len(dE_range)))),
                 color=[1, 0.8, 0.8], edgecolor='none', alpha=0.5)  # Vùng đỏ nhạt
plt.fill_between(np.concatenate((dE_range, dE_range[::-1])),
                 np.concatenate((np.ones(len(dE_range)) * 0.4, np.ones(len(dE_range)) * 0.8)),
                 color=[1, 1, 0.6], edgecolor='none', alpha=0.5)  # Vùng vàng nhạt
plt.fill_between(np.concatenate((dE_range, dE_range[::-1])),
                 np.concatenate((np.zeros(len(dE_range)), np.ones(len(dE_range)) * 0.4)),
                 color=[0.8, 1, 0.8], edgecolor='none', alpha=0.5)  # Vùng xanh nhạt

# Vẽ 3 đường xác suất
for j in range(3):
    plt.plot(dE_range, O_S[j, :], color=colors[j], linewidth=2, label=labels[j])

# Gạch chỉ hướng (tương đương annotation textarrow)
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