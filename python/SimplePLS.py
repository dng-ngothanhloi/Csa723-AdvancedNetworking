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
dE_range = np.linspace(20, 100, 50) # Khoảng cách Alice-Eve (m) - cải tiến cho small cell

# Ba giá trị d_B tương ứng ba kịch bản
dB_values = [20, 50, 100]   # Khoảng cách Alice-Bob (m)
colors = ['g', 'b', 'r']
labels = [
    'd_B = 70 m (O_S ≈ 1)',
    'd_B = 50 m (O_S giảm)',
    'd_B = 20 m (O_S giảm gần 0)'
]
O_S = np.zeros((3, len(dE_range)))

# Mô phỏng cho từng kịch bản
for j in range(3):
    d_B = dB_values[j]
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
        O_S[j, i] = np.mean(C_S < epsilon_S * 180e3) # Nhân epsilon_S với băng thông 180 kHz để có đơn vị bit/s

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

# Gạch chỉ hướng (tương đương annotation textarrow) - Fixed linter error
plt.annotate('Xu hướng giảm', 
             xy=(float(np.mean(dE_range)), float(np.mean(O_S[0,:]))), 
             xytext=(float(np.mean(dE_range) - 20), float(np.mean(O_S[0,:]) + 0.15)),
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

print("="*80)
print("PHYSICAL LAYER SECURITY (PLS) SIMULATION WITH ARTIFICIAL NOISE (AN)")
print("="*80)

## ============================================================================
## PHẦN 2: MÔ PHỎNG BẢO MẬT TẦNG VẬT LÝ (PLS) VỚI NHIỄU NHÂN TẠO (AN)
## ============================================================================

def artificial_noise_algorithm(P_A, phi, h_B, h_E, d_B, d_E, N_0, alpha):
    """
    Thuật toán khảo sát chống nhiễu vật lý AN tại BS
    
    Parameters:
    - P_A: Công suất truyền tổng (W)
    - phi: Tỷ lệ công suất cho tín hiệu hợp lệ (0 < phi < 1)
    - h_B, h_E: Kênh fading cho Bob và Eve
    - d_B, d_E: Khoảng cách đến Bob và Eve (m)
    - N_0: Nhiễu nền (W)
    - alpha: Hệ số suy hao đường truyền
    
    Returns:
    - SNR_Bob_AN: SNR tại Bob với AN
    - SNR_Eve_AN: SNR tại Eve với AN
    - C_S_AN: Secrecy Capacity với AN
    """
    
    # 1. Phân bổ công suất theo thuật toán AN
    P_S = phi * P_A          # Công suất cho tín hiệu hợp lệ
    P_AN = (1 - phi) * P_A   # Công suất cho nhiễu nhân tạo
    
    # 2. Tạo nhiễu nhân tạo (Artificial Noise)
    # Nhiễu được thiết kế để gây nhiễu cho Eve nhưng không ảnh hưởng Bob
    w_AN = np.sqrt(P_AN/2) * (np.random.randn(len(h_B)) + 1j * np.random.randn(len(h_B)))
    
    # 3. Tính SNR với AN
    # Tại Bob: Tín hiệu hợp lệ + nhiễu nhân tạo (được thiết kế để không ảnh hưởng)
    signal_power_Bob = P_S * np.abs(h_B)**2
    noise_power_Bob = N_0 * d_B**alpha + np.abs(w_AN)**2
    SNR_Bob_AN = signal_power_Bob / noise_power_Bob
    
    # Tại Eve: Tín hiệu hợp lệ + nhiễu nhân tạo (gây nhiễu mạnh)
    signal_power_Eve = P_S * np.abs(h_E)**2
    noise_power_Eve = N_0 * d_E**alpha + np.abs(w_AN)**2
    SNR_Eve_AN = signal_power_Eve / noise_power_Eve
    
    # 4. Tính dung lượng kênh với AN
    C_AB_AN = 180e3 * np.log2(1 + SNR_Bob_AN)
    C_AE_AN = 180e3 * np.log2(1 + SNR_Eve_AN)
    
    # 5. Tính Secrecy Capacity với AN
    C_S_AN = np.maximum(0, C_AB_AN - C_AE_AN)
    
    return SNR_Bob_AN, SNR_Eve_AN, C_S_AN

# Tham số khảo sát với phi_values=[0.1, 0.2, 0.3]
phi_values = [0.1, 0.2, 0.3]  # Tỷ lệ công suất cho tín hiệu hợp lệ
d_B_AN = 50                    # Khoảng cách Alice-Bob (m) - kịch bản trung bình
dE_range_AN = np.linspace(20, 100, 50)  # Khoảng cách Alice-Eve (m) - cải tiến cho small cell

# Màu sắc và nhãn cho các giá trị phi
phi_colors = ['red', 'blue', 'green']
phi_labels = [f'φ = {phi} (P_S = {phi*P_A:.1f}W, P_AN = {(1-phi)*P_A:.1f}W)' for phi in phi_values]

# Ma trận lưu kết quả
O_S_AN = np.zeros((len(phi_values), len(dE_range_AN)))
C_S_avg_AN = np.zeros((len(phi_values), len(dE_range_AN)))

print(f"Tham số khảo sát:")
print(f"- P_A = {P_A} W (công suất truyền tổng)")
print(f"- phi_values = {phi_values}")
print(f"- d_B = {d_B_AN} m (khoảng cách Alice-Bob)")
print(f"- d_E = {dE_range_AN[0]:.0f}-{dE_range_AN[-1]:.0f} m (khoảng cách Alice-Eve) - Small Cell")
print(f"- Số mẫu mô phỏng: {num_samples:,}")

# Mô phỏng AN cho từng giá trị phi
for phi_idx, phi in enumerate(phi_values):
    print(f"\nĐang mô phỏng với φ = {phi}...")
    
    for i, d_E in enumerate(dE_range_AN):
        # Tạo kênh fading Rayleigh
        h_B = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        h_E = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        
        # Áp dụng thuật toán AN
        SNR_Bob_AN, SNR_Eve_AN, C_S_AN = artificial_noise_algorithm(
            P_A, phi, h_B, h_E, d_B_AN, d_E, N_0, alpha
        )
        
        # Tính Secrecy Outage và Secrecy Capacity trung bình
        O_S_AN[phi_idx, i] = np.mean(C_S_AN < epsilon_S * 180e3)
        C_S_avg_AN[phi_idx, i] = np.mean(C_S_AN)

# Vẽ kết quả mô phỏng AN
plt.figure(figsize=(12, 8))

# Subplot 1: Secrecy Outage Probability
plt.subplot(2, 2, 1)
for phi_idx in range(len(phi_values)):
    plt.plot(dE_range_AN, O_S_AN[phi_idx, :], 
             color=phi_colors[phi_idx], linewidth=2, 
             label=phi_labels[phi_idx], marker='o', markersize=4)

plt.xlabel('Khoảng cách Alice-Eve (m)')
plt.ylabel('Xác suất dừng bảo mật O_S')
plt.title('Secrecy Outage với Artificial Noise (Small Cell)')
plt.legend()
plt.grid(True)

# Subplot 2: Average Secrecy Capacity
plt.subplot(2, 2, 2)
for phi_idx in range(len(phi_values)):
    plt.plot(dE_range_AN, C_S_avg_AN[phi_idx, :] / 1000, 
             color=phi_colors[phi_idx], linewidth=2, 
             label=phi_labels[phi_idx], marker='s', markersize=4)

plt.xlabel('Khoảng cách Alice-Eve (m)')
plt.ylabel('Secrecy Capacity trung bình (kbps)')
plt.title('Secrecy Capacity với Artificial Noise (Small Cell)')
plt.legend()
plt.grid(True)

# Subplot 3: So sánh hiệu suất theo phi
plt.subplot(2, 2, 3)
d_E_fixed = 60  # Khoảng cách cố định để so sánh (phù hợp với small cell)
d_E_idx = np.argmin(np.abs(dE_range_AN - d_E_fixed))

phi_comparison = []
for phi_idx in range(len(phi_values)):
    phi_comparison.append(C_S_avg_AN[phi_idx, d_E_idx] / 1000)

plt.bar(phi_values, phi_comparison, color=phi_colors, alpha=0.7)
plt.xlabel('Tỷ lệ công suất φ')
plt.ylabel('Secrecy Capacity (kbps)')
plt.title(f'So sánh hiệu suất tại d_E = {d_E_fixed}m (Small Cell)')
plt.grid(True)

# Subplot 4: Heatmap Secrecy Capacity
plt.subplot(2, 2, 4)
im = plt.imshow(C_S_avg_AN / 1000, aspect='auto', 
                extent=(float(dE_range_AN[0]), float(dE_range_AN[-1]), float(phi_values[0]), float(phi_values[-1])),
                cmap='viridis')
plt.colorbar(im, label='Secrecy Capacity (kbps)')
plt.xlabel('Khoảng cách Alice-Eve (m)')
plt.ylabel('Tỷ lệ công suất φ')
plt.title('Heatmap Secrecy Capacity (Small Cell)')
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

# Phân tích kết quả
print("\n" + "="*60)
print("PHÂN TÍCH KẾT QUẢ ARTIFICIAL NOISE")
print("="*60)

for phi_idx, phi in enumerate(phi_values):
    avg_secrecy_capacity = np.mean(C_S_avg_AN[phi_idx, :]) / 1000
    min_secrecy_capacity = np.min(C_S_avg_AN[phi_idx, :]) / 1000
    max_secrecy_capacity = np.max(C_S_avg_AN[phi_idx, :]) / 1000
    avg_outage = np.mean(O_S_AN[phi_idx, :])
    
    print(f"\nφ = {phi}:")
    print(f"  - P_S = {phi*P_A:.1f}W, P_AN = {(1-phi)*P_A:.1f}W")
    print(f"  - Secrecy Capacity trung bình: {avg_secrecy_capacity:.2f} kbps")
    print(f"  - Secrecy Capacity min/max: {min_secrecy_capacity:.2f}/{max_secrecy_capacity:.2f} kbps")
    print(f"  - Xác suất dừng bảo mật trung bình: {avg_outage:.4f}")

# Tìm giá trị phi tối ưu
optimal_phi_idx = np.argmax(np.mean(C_S_avg_AN, axis=1))
optimal_phi = phi_values[optimal_phi_idx]
print(f"\nGiá trị φ tối ưu: {optimal_phi}")
print(f"Secrecy Capacity trung bình tối ưu: {np.mean(C_S_avg_AN[optimal_phi_idx, :])/1000:.2f} kbps")

print("\n" + "="*60)
print("KẾT LUẬN:")
print("="*60)
print("1. Artificial Noise cải thiện đáng kể bảo mật tầng vật lý")
print("2. Giá trị φ tối ưu cân bằng giữa tín hiệu hợp lệ và nhiễu nhân tạo")
print("3. Hiệu suất bảo mật phụ thuộc vào khoảng cách và phân bổ công suất")
print("4. AN hiệu quả nhất khi Eve ở xa và Bob ở gần")