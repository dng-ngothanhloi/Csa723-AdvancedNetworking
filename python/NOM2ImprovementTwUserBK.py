## Simulation Improvement: Kết hợp hai kịch bản
# Kịch bản 1: 1 user hợp lệ (Bob), 1 Eve, mô phỏng theo khoảng cách d_{AE}
# Kịch bản 2: Multi-user NOMA (Bob1, Bob2, Eve), mô phỏng theo SNR, BER/SER, dung lượng

import numpy as np
import matplotlib.pyplot as plt

# ===================== KỊCH BẢN 1: THEO KHOẢNG CÁCH d_{AE} =====================
print("\n===== KỊCH BẢN 1: 1 user + Eve, mô phỏng theo d_{AE} =====")
# Thông số hệ thống
P_A = 1
N_0 = 10**((-134 - 30) / 10)
alpha = 3
epsilon_S = 0.5
B = 10e6
num_samples = int(1e4)
dE_range = np.linspace(100, 500, 50)
dB = 50  # Bob cố định
O_S = np.zeros(len(dE_range))
R_s = np.zeros(len(dE_range))
eta_s = np.zeros(len(dE_range))

print("==== THÔNG SỐ HỆ THỐNG ====")
print(f"Công suất truyền P_A: {P_A} W")
print(f"Nhiễu nền N_0: {N_0:.2e} W")
print(f"Hệ số suy hao alpha: {alpha}")
print(f"Ngưỡng bảo mật epsilon_S: {epsilon_S:.4f} (bits/s/Hz)")
print(f"Băng thông: {B/1e6:.1f} MHz")
print(f"Khoảng cách d_B: {dB}")
print(f"Khoảng cách d_E: {dE_range[0]:.1f} -> {dE_range[-1]:.1f} m (step {dE_range[1]-dE_range[0]:.1f})")
print("============================\n")

for i in range(len(dE_range)):
    d_E = dE_range[i]
    h_B = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_E = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    SNR_Bob = (P_A * np.abs(h_B)**2) / (dB**alpha * N_0)
    SNR_Eve = (P_A * np.abs(h_E)**2) / (d_E**alpha * N_0)
    C_AB = B * np.log2(1 + SNR_Bob)
    C_AE = B * np.log2(1 + SNR_Eve)
    C_S = np.maximum(0, C_AB - C_AE)
    R_s[i] = np.mean(C_S) / B
    O_S[i] = np.mean(C_S < epsilon_S * B)
    eta_s[i] = R_s[i]
    print(f"d_E = {d_E:.1f} m | O_S = {O_S[i]:.4f} | R_s = {R_s[i]:.4f} | eta_s = {eta_s[i]:.4f}")

# Biểu đồ xác suất dừng
plt.figure(figsize=(8,6))
plt.plot(dE_range, O_S, 'b-o', label='Secrecy Outage Probability')
plt.xlabel('Khoảng cách từ A đến E (d_{AE}) (m)')
plt.ylabel('Xác suất dừng bảo mật O_S')
plt.title('Biểu diễn xác suất dừng theo khoảng cách d_{AE}')
plt.grid(True)
plt.legend()
plt.show()

# Biểu đồ Secrecy Rate
printf = plt.figure(figsize=(8,6))
plt.plot(dE_range, R_s, 'g-s', label='Secrecy Rate')
plt.xlabel('Khoảng cách từ A đến E (d_{AE}) (m)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Secrecy Rate theo khoảng cách d_{AE}')
plt.grid(True)
plt.legend()
plt.show()

# Biểu đồ Secrecy Spectral Efficiency
plt.figure(figsize=(8,6))
plt.plot(dE_range, eta_s, 'r-^', label='Secrecy Spectral Efficiency')
plt.xlabel('Khoảng cách từ A đến E (d_{AE}) (m)')
plt.ylabel('Secrecy Spectral Efficiency (bits/s/Hz)')
plt.title('Secrecy Spectral Efficiency theo khoảng cách d_{AE}')
plt.grid(True)
plt.legend()
plt.show()

# ===================== KỊCH BẢN 2: MULTI-USER, THEO SNR =====================
print("\n===== KỊCH BẢN 2: Multi-user NOMA, mô phỏng theo SNR =====")
# Thông số hệ thống
SNR_dB_range = np.arange(-10, 21, 2)
alpha1 = 0.7
alpha2 = 0.3
d_B1 = 50
d_B2 = 100
d_E = 200
C_B1 = np.zeros(len(SNR_dB_range))
C_B2 = np.zeros(len(SNR_dB_range))
C_E = np.zeros(len(SNR_dB_range))
BER_B1 = np.zeros(len(SNR_dB_range))
BER_B2 = np.zeros(len(SNR_dB_range))
BER_E = np.zeros(len(SNR_dB_range))
SER_B1 = np.zeros(len(SNR_dB_range))
SER_B2 = np.zeros(len(SNR_dB_range))
SER_E = np.zeros(len(SNR_dB_range))

print(f"Phân bổ công suất: alpha1 = {alpha1}, alpha2 = {alpha2} (tổng = {alpha1+alpha2})")
print(f"Khoảng cách: Bob1 = {d_B1}m, Bob2 = {d_B2}m, Eve = {d_E}m")

for idx, SNR_dB in enumerate(SNR_dB_range):
    SNR_linear = 10**(SNR_dB/10)
    P_A_eff = SNR_linear * d_B1**alpha * N_0
    h_B1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_B2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_E = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    SNR_B2 = (P_A_eff * alpha2 * np.abs(h_B2)**2) / (d_B2**alpha * N_0)
    SNR_B1 = (P_A_eff * alpha1 * np.abs(h_B1)**2) / (d_B1**alpha * N_0 + P_A_eff * alpha2 * np.abs(h_B1)**2)
    SNR_E = (P_A_eff * np.abs(h_E)**2) / (d_E**alpha * N_0)
    C_B1[idx] = np.mean(B * np.log2(1 + SNR_B1))
    C_B2[idx] = np.mean(B * np.log2(1 + SNR_B2))
    C_E[idx] = np.mean(B * np.log2(1 + SNR_E))
    BER_B1[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_B1 / (1 + SNR_B1))))
    BER_B2[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_B2 / (1 + SNR_B2))))
    BER_E[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_E / (1 + SNR_E))))
    SER_B1[idx] = BER_B1[idx]
    SER_B2[idx] = BER_B2[idx]
    SER_E[idx] = BER_E[idx]
    print(f"SNR = {SNR_dB} dB | C_B1 = {C_B1[idx]/1e6:.2f} Mbps | C_B2 = {C_B2[idx]/1e6:.2f} Mbps | C_E = {C_E[idx]/1e6:.2f} Mbps | BER_B1 = {BER_B1[idx]:.4e} | BER_B2 = {BER_B2[idx]:.4e} | BER_E = {BER_E[idx]:.4e}")

# Vẽ biểu đồ dung lượng kênh
plt.figure(figsize=(8,6))
plt.plot(SNR_dB_range, C_B1/1e6, 'g-o', label='Bob1 (gần)')
plt.plot(SNR_dB_range, C_B2/1e6, 'b-s', label='Bob2 (xa)')
plt.plot(SNR_dB_range, C_E/1e6, 'r-^', label='Eve (nghe lén)')
plt.xlabel('SNR (dB)')
plt.ylabel('Dung lượng kênh trung bình (Mbps)')
plt.title('Dung lượng kênh của từng user và Eve theo SNR')
plt.legend()
plt.grid(True)
plt.show()

# Vẽ biểu đồ BER
plt.figure(figsize=(8,6))
plt.semilogy(SNR_dB_range, BER_B1, 'g-o', label='Bob1 (gần)')
plt.semilogy(SNR_dB_range, BER_B2, 'b-s', label='Bob2 (xa)')
plt.semilogy(SNR_dB_range, BER_E, 'r-^', label='Eve (nghe lén)')
plt.xlabel('SNR (dB)')
plt.ylabel('BER (BPSK, Rayleigh)')
plt.title('BER của từng user và Eve theo SNR')
plt.legend()
plt.grid(True, which='both')
plt.show()

# Vẽ biểu đồ SER (ở đây SER = BER do BPSK)
plt.figure(figsize=(8,6))
plt.semilogy(SNR_dB_range, SER_B1, 'g-o', label='Bob1 (gần)')
plt.semilogy(SNR_dB_range, SER_B2, 'b-s', label='Bob2 (xa)')
plt.semilogy(SNR_dB_range, SER_E, 'r-^', label='Eve (nghe lén)')
plt.xlabel('SNR (dB)')
plt.ylabel('SER (BPSK, Rayleigh)')
plt.title('SER của từng user và Eve theo SNR')
plt.legend()
plt.grid(True, which='both')
plt.show()