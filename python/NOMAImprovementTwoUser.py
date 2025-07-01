## Simulation Improvement: Kết hợp hai kịch bản
# Kịch bản 1: 1 user hợp lệ (Bob), 1 Eve, mô phỏng theo khoảng cách d_{AE}
# Kịch bản 2: Multi-user NOMA (Bob1, Bob2, Eve), mô phỏng theo SNR, BER/SER, dung lượng

import numpy as np
import matplotlib.pyplot as plt

# ===================== KỊCH BẢN 2: MULTI-USER NOMA, SNR_EVE SWEEP (ACTIVE JAMMING) =====================
print("\n===== KỊCH BẢN 2: Multi-user NOMA, quét SNR_Eve (Eve chủ động gây nhiễu) =====")
# Thông số hệ thống
P_A = 1
N_0 = 10**((-134 - 30) / 10)
alpha = 3
B = 10e6
num_samples = int(1e4)
d_B1 = 50  # Bob1
d_B2 = 100 # Bob2
d_E = 70   # Eve cố định
R_th = 0.1  # Ngưỡng bảo mật (bits/s/Hz)

# Power allocation theo path loss
alpha1_p = d_B1**alpha
alpha2_p = d_B2**alpha
alpha1 = alpha1_p / (alpha1_p + alpha2_p)
alpha2 = alpha2_p / (alpha1_p + alpha2_p)

print("==== THÔNG SỐ HỆ THỐNG KỊCH BẢN 2 ====")
print(f"Công suất truyền P_A: {P_A} W")
print(f"Nhiễu nền N_0: {N_0:.2e} W")
print(f"Hệ số suy hao alpha: {alpha}")
print(f"Băng thông: {B/1e6:.1f} MHz")
print(f"Khoảng cách: Bob1 = {d_B1}m, Bob2 = {d_B2}m, Eve = {d_E}m")
print(f"Phân bổ công suất: alpha1 = {alpha1:.3f}, alpha2 = {alpha2:.3f} (tổng = {alpha1+alpha2:.3f})")
print("============================\n")

SNR_Bob_dB = 10  # SNR của Bob1, Bob2 cố định
SNR_Bob_linear = 10**(SNR_Bob_dB/10)
P_A_eff = SNR_Bob_linear * d_B1**alpha * N_0

SNR_Eve_dB_range = np.arange(0, 21, 2)
C_B1 = np.zeros(len(SNR_Eve_dB_range))
C_B2 = np.zeros(len(SNR_Eve_dB_range))
C_E = np.zeros(len(SNR_Eve_dB_range))
BER_B1 = np.zeros(len(SNR_Eve_dB_range))
BER_B2 = np.zeros(len(SNR_Eve_dB_range))
BER_E = np.zeros(len(SNR_Eve_dB_range))
R_s1 = np.zeros(len(SNR_Eve_dB_range))
R_s2 = np.zeros(len(SNR_Eve_dB_range))
R_s_sum = np.zeros(len(SNR_Eve_dB_range))
SOP1 = np.zeros(len(SNR_Eve_dB_range))
SOP2 = np.zeros(len(SNR_Eve_dB_range))
IP1 = np.zeros(len(SNR_Eve_dB_range))
IP2 = np.zeros(len(SNR_Eve_dB_range))
Erg_Rs1 = np.zeros(len(SNR_Eve_dB_range))
Erg_Rs2 = np.zeros(len(SNR_Eve_dB_range))
Cs1 = np.zeros(len(SNR_Eve_dB_range))
Cs2 = np.zeros(len(SNR_Eve_dB_range))

for idx, SNR_Eve_dB in enumerate(SNR_Eve_dB_range):
    SNR_Eve_linear = 10**(SNR_Eve_dB/10)
    # Tính P_E để đạt SNR_Eve mong muốn tại d_E
    P_E = SNR_Eve_linear * d_E**alpha * N_0
    # Kênh fading
    h_B1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_B2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_E = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_EB1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_EB2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    d_EB1 = abs(d_E - d_B1) + 1e-3  # tránh chia 0
    d_EB2 = abs(d_E - d_B2) + 1e-3
    # SNR các user (có nhiễu từ Eve)
    SNR_B2 = (P_A_eff * alpha2 * np.abs(h_B2)**2) / (d_B2**alpha * N_0 + P_E * np.abs(h_EB2)**2 / (d_EB2**alpha))
    SNR_B1 = (P_A_eff * alpha1 * np.abs(h_B1)**2) / (d_B1**alpha * N_0 + P_A_eff * alpha2 * np.abs(h_B1)**2 + P_E * np.abs(h_EB1)**2 / (d_EB1**alpha))
    SNR_E = (P_E * np.abs(h_E)**2) / (d_E**alpha * N_0)
    # Dung lượng kênh
    R1 = np.log2(1 + SNR_B1)
    R2 = np.log2(1 + SNR_B2)
    Re1 = np.log2(1 + SNR_E)
    Re2 = np.log2(1 + SNR_E)
    # Secrecy Rate
    Rs1 = np.maximum(0, R1 - Re1)
    Rs2 = np.maximum(0, R2 - Re2)
    R_s1[idx] = np.mean(Rs1)
    R_s2[idx] = np.mean(Rs2)
    R_s_sum[idx] = R_s1[idx] + R_s2[idx]
    # Secrecy Outage Probability
    SOP1[idx] = np.mean(Rs1 < R_th)
    SOP2[idx] = np.mean(Rs2 < R_th)
    # Intercept Probability
    IP1[idx] = np.mean(Re1 >= R1)
    IP2[idx] = np.mean(Re2 >= R2)
    # Ergodic Secrecy Rate
    Erg_Rs1[idx] = np.mean(Rs1)
    Erg_Rs2[idx] = np.mean(Rs2)
    # Secrecy Capacity
    Cs1[idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B1) - np.log2(1 + SNR_E)))
    Cs2[idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B2) - np.log2(1 + SNR_E)))
    # Dung lượng kênh trung bình
    C_B1[idx] = np.mean(B * np.log2(1 + SNR_B1))
    C_B2[idx] = np.mean(B * np.log2(1 + SNR_B2))
    C_E[idx] = np.mean(B * np.log2(1 + SNR_E))
    # BER (BPSK, Rayleigh)
    BER_B1[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_B1 / (1 + SNR_B1))))
    BER_B2[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_B2 / (1 + SNR_B2))))
    BER_E[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_E / (1 + SNR_E))))
    print(f"SNR_Eve = {SNR_Eve_dB} dB | C_B1 = {C_B1[idx]/1e6:.2f} Mbps | C_B2 = {C_B2[idx]/1e6:.2f} Mbps | C_E = {C_E[idx]/1e6:.2f} Mbps | BER_B1 = {BER_B1[idx]:.4e} | BER_B2 = {BER_B2[idx]:.4e} | BER_E = {BER_E[idx]:.4e}")

# Vẽ các biểu đồ tương ứng (ví dụ: Secrecy Rate, SOP, BER, Intercept Probability)
plt.figure(figsize=(8,6))
plt.plot(SNR_Eve_dB_range, R_s1, 'g-o', label='Secrecy Rate Bob1')
plt.plot(SNR_Eve_dB_range, R_s2, 'b-s', label='Secrecy Rate Bob2')
plt.plot(SNR_Eve_dB_range, R_s_sum, 'k-^', label='Secrecy Sum Rate')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Secrecy Rate vs SNR_Eve')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.plot(SNR_Eve_dB_range, SOP1, 'g-o', label='SOP Bob1')
plt.plot(SNR_Eve_dB_range, SOP2, 'b-s', label='SOP Bob2')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Outage Probability')
plt.title('Secrecy Outage Probability vs SNR_Eve')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.plot(SNR_Eve_dB_range, IP1, 'g-o', label='Intercept Prob. Bob1')
plt.plot(SNR_Eve_dB_range, IP2, 'b-s', label='Intercept Prob. Bob2')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Intercept Probability')
plt.title('Intercept Probability vs SNR_Eve')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.semilogy(SNR_Eve_dB_range, BER_B1, 'g-o', label='BER Bob1')
plt.semilogy(SNR_Eve_dB_range, BER_B2, 'b-s', label='BER Bob2')
plt.semilogy(SNR_Eve_dB_range, BER_E, 'r-^', label='BER Eve')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('BER (BPSK, Rayleigh)')
plt.title('BER vs SNR_Eve')
plt.legend()
plt.grid(True, which='both')
plt.show()

# ===================== KỊCH BẢN 3: MULTI-USER NOMA, d_E SWEEP (ACTIVE JAMMING) =====================
print("\n===== KỊCH BẢN 3: Multi-user NOMA, quét d_E (Eve chủ động gây nhiễu) =====")
d_E_range = np.arange(20, 151, 10)
P_E = 1  # Công suất gây nhiễu của Eve cố định
C_B1_3 = np.zeros(len(d_E_range))
C_B2_3 = np.zeros(len(d_E_range))
C_E_3 = np.zeros(len(d_E_range))
BER_B1_3 = np.zeros(len(d_E_range))
BER_B2_3 = np.zeros(len(d_E_range))
BER_E_3 = np.zeros(len(d_E_range))
R_s1_3 = np.zeros(len(d_E_range))
R_s2_3 = np.zeros(len(d_E_range))
R_s_sum_3 = np.zeros(len(d_E_range))
SOP1_3 = np.zeros(len(d_E_range))
SOP2_3 = np.zeros(len(d_E_range))
IP1_3 = np.zeros(len(d_E_range))
IP2_3 = np.zeros(len(d_E_range))
Erg_Rs1_3 = np.zeros(len(d_E_range))
Erg_Rs2_3 = np.zeros(len(d_E_range))
Cs1_3 = np.zeros(len(d_E_range))
Cs2_3 = np.zeros(len(d_E_range))

for idx, d_E in enumerate(d_E_range):
    h_B1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_B2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_E = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_EB1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_EB2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    d_EB1 = abs(d_E - d_B1) + 1e-3
    d_EB2 = abs(d_E - d_B2) + 1e-3
    SNR_B2 = (P_A_eff * alpha2 * np.abs(h_B2)**2) / (d_B2**alpha * N_0 + P_E * np.abs(h_EB2)**2 / (d_EB2**alpha))
    SNR_B1 = (P_A_eff * alpha1 * np.abs(h_B1)**2) / (d_B1**alpha * N_0 + P_A_eff * alpha2 * np.abs(h_B1)**2 + P_E * np.abs(h_EB1)**2 / (d_EB1**alpha))
    SNR_E = (P_E * np.abs(h_E)**2) / (d_E**alpha * N_0)
    R1 = np.log2(1 + SNR_B1)
    R2 = np.log2(1 + SNR_B2)
    Re1 = np.log2(1 + SNR_E)
    Re2 = np.log2(1 + SNR_E)
    Rs1 = np.maximum(0, R1 - Re1)
    Rs2 = np.maximum(0, R2 - Re2)
    R_s1_3[idx] = np.mean(Rs1)
    R_s2_3[idx] = np.mean(Rs2)
    R_s_sum_3[idx] = R_s1_3[idx] + R_s2_3[idx]
    SOP1_3[idx] = np.mean(Rs1 < R_th)
    SOP2_3[idx] = np.mean(Rs2 < R_th)
    IP1_3[idx] = np.mean(Re1 >= R1)
    IP2_3[idx] = np.mean(Re2 >= R2)
    Erg_Rs1_3[idx] = np.mean(Rs1)
    Erg_Rs2_3[idx] = np.mean(Rs2)
    Cs1_3[idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B1) - np.log2(1 + SNR_E)))
    Cs2_3[idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B2) - np.log2(1 + SNR_E)))
    C_B1_3[idx] = np.mean(B * np.log2(1 + SNR_B1))
    C_B2_3[idx] = np.mean(B * np.log2(1 + SNR_B2))
    C_E_3[idx] = np.mean(B * np.log2(1 + SNR_E))
    BER_B1_3[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_B1 / (1 + SNR_B1))))
    BER_B2_3[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_B2 / (1 + SNR_B2))))
    BER_E_3[idx] = np.mean(0.5 * (1 - np.sqrt(SNR_E / (1 + SNR_E))))
    print(f"d_E = {d_E} m | C_B1 = {C_B1_3[idx]/1e6:.2f} Mbps | C_B2 = {C_B2_3[idx]/1e6:.2f} Mbps | C_E = {C_E_3[idx]/1e6:.2f} Mbps | BER_B1 = {BER_B1_3[idx]:.4e} | BER_B2 = {BER_B2_3[idx]:.4e} | BER_E = {BER_E_3[idx]:.4e}")

plt.figure(figsize=(8,6))
plt.plot(d_E_range, R_s1_3, 'g-o', label='Secrecy Rate Bob1')
plt.plot(d_E_range, R_s2_3, 'b-s', label='Secrecy Rate Bob2')
plt.plot(d_E_range, R_s_sum_3, 'k-^', label='Secrecy Sum Rate')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Secrecy Rate vs d_E')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.plot(d_E_range, SOP1_3, 'g-o', label='SOP Bob1')
plt.plot(d_E_range, SOP2_3, 'b-s', label='SOP Bob2')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Secrecy Outage Probability')
plt.title('Secrecy Outage Probability vs d_E')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.plot(d_E_range, IP1_3, 'g-o', label='Intercept Prob. Bob1')
plt.plot(d_E_range, IP2_3, 'b-s', label='Intercept Prob. Bob2')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Intercept Probability')
plt.title('Intercept Probability vs d_E')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.semilogy(d_E_range, BER_B1_3, 'g-o', label='BER Bob1')
plt.semilogy(d_E_range, BER_B2_3, 'b-s', label='BER Bob2')
plt.semilogy(d_E_range, BER_E_3, 'r-^', label='BER Eve')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('BER (BPSK, Rayleigh)')
plt.title('BER vs d_E')
plt.legend()
plt.grid(True, which='both')
plt.show()
