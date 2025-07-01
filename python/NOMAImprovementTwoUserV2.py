import numpy as np
import matplotlib.pyplot as plt

# KỊCH BẢN 2: Multi-user NOMA, quét SNR_Eve (Eve chủ động gây nhiễu)
print("\n===== KỊCH BẢN 2: Multi-user NOMA, quét SNR_Eve (Eve chủ động gây nhiễu) =====")
# Thông số hệ thống
P_A = 1  # Công suất truyền tổng (W)
N_0 = 10**((-134 - 30) / 10)  # Nhiễu nền (W)
alpha = 3  # Hệ số suy hao kênh
B = 10e6  # Băng thông (Hz)
num_samples = int(1e4)  # Số lần mô phỏng Monte Carlo
d_B1 = 50  # Khoảng cách Bob1 (m)
d_B2 = 100  # Khoảng cách Bob2 (m)
d_E = 70  # Khoảng cách Eve cố định (m)
R_th = 0.1  # Ngưỡng bảo mật (bits/s/Hz)
epsilon = 0.001  # Tỷ lệ lỗi SIC (Cập nhật từ 0.01 xuống 0.001)

# Phân bổ công suất theo path loss
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
print(f"Tỷ lệ lỗi SIC: epsilon = {epsilon}")
print("============================\n")

# Quét SNR_Bob và SNR_Eve
SNR_Bob_dB_range = np.arange(0, 21, 2)  # Giữ nguyên quét, nhưng ưu tiên 20 dB
SNR_Eve_dB_range = np.arange(0, 21, 2)

# Khởi tạo mảng kết quả
C_B1 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
C_B2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
C_E = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
BER_B1 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
BER_B2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
BER_E = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
R_s1 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
R_s2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
R_s_sum = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
SOP1 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
SOP2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
IP1 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
IP2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
Erg_Rs1 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
Erg_Rs2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
Cs1 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
Cs2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))

for bob_idx, SNR_Bob_dB in enumerate(SNR_Bob_dB_range):
    SNR_Bob_linear = 10**(SNR_Bob_dB / 10)
    P_A_eff = SNR_Bob_linear * d_B1**alpha * N_0  # Công suất hiệu quả

    for eve_idx, SNR_Eve_dB in enumerate(SNR_Eve_dB_range):
        SNR_Eve_linear = 10**(SNR_Eve_dB / 10)
        P_E = SNR_Eve_linear * d_E**alpha * N_0  # Công suất nhiễu của Eve

        # Kênh fading
        h_B1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        h_B2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        h_E = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        h_EB1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        h_EB2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        d_EB1 = abs(d_E - d_B1) + 1e-3
        d_EB2 = abs(d_E - d_B2) + 1e-3

        # SNR (Cập nhật: Thêm nhiễu chéo cho SNR_E)
        SNR_B2 = (P_A_eff * alpha2 * np.abs(h_B2)**2) / (d_B2**alpha * N_0 + P_E * np.abs(h_EB2)**2 / (d_EB2**alpha))
        SNR_B1 = (P_A_eff * alpha1 * np.abs(h_B1)**2) / (d_B1**alpha * N_0 + epsilon * P_A_eff * alpha2 * np.abs(h_B1)**2 + P_E * np.abs(h_EB1)**2 / (d_EB1**alpha))
        I_Bob = P_A_eff * np.abs(h_E)**2 / (d_E**alpha)  # Nhiễu chéo tổng hợp từ Bob
        SNR_E1 = (P_A_eff * alpha1 * np.abs(h_E)**2) / (d_E**alpha * N_0 + I_Bob)
        SNR_E2 = (P_A_eff * alpha2 * np.abs(h_E)**2) / (d_E**alpha * N_0 + I_Bob)

        # Dung lượng kênh
        R1 = np.log2(1 + SNR_B1)
        R2 = np.log2(1 + SNR_B2)
        Re1 = np.log2(1 + SNR_E1)
        Re2 = np.log2(1 + SNR_E2)

        # Secrecy Rate
        Rs1 = np.maximum(0, R1 - Re1)
        Rs2 = np.maximum(0, R2 - Re2)
        R_s1[bob_idx, eve_idx] = np.mean(Rs1)
        R_s2[bob_idx, eve_idx] = np.mean(Rs2)
        R_s_sum[bob_idx, eve_idx] = R_s1[bob_idx, eve_idx] + R_s2[bob_idx, eve_idx]

        # Secrecy Outage Probability
        SOP1[bob_idx, eve_idx] = np.mean(Rs1 < R_th)
        SOP2[bob_idx, eve_idx] = np.mean(Rs2 < R_th)

        # Intercept Probability
        IP1[bob_idx, eve_idx] = np.mean(Re1 >= R1)
        IP2[bob_idx, eve_idx] = np.mean(Re2 >= R2)

        # Ergodic Secrecy Rate
        Erg_Rs1[bob_idx, eve_idx] = np.mean(Rs1)
        Erg_Rs2[bob_idx, eve_idx] = np.mean(Rs2)

        # Secrecy Capacity
        Cs1[bob_idx, eve_idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B1) - np.log2(1 + SNR_E1)))
        Cs2[bob_idx, eve_idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B2) - np.log2(1 + SNR_E2)))

        # Dung lượng kênh trung bình
        C_B1[bob_idx, eve_idx] = np.mean(B * np.log2(1 + SNR_B1))
        C_B2[bob_idx, eve_idx] = np.mean(B * np.log2(1 + SNR_B2))
        C_E[bob_idx, eve_idx] = np.mean(B * np.log2(1 + np.maximum(SNR_E1, SNR_E2)))

        # BER (Mô phỏng BPSK thực tế)
        bits = np.random.randint(0, 2, num_samples)
        tx_signal = 2 * bits - 1
        rx_signal_B1 = np.sqrt(P_A_eff * alpha1) * h_B1 * tx_signal + np.sqrt(epsilon * P_A_eff * alpha2) * h_B1 * tx_signal + np.sqrt(P_E / d_EB1**alpha) * h_EB1 * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        rx_signal_B2 = np.sqrt(P_A_eff * alpha2) * h_B2 * tx_signal + np.sqrt(P_E / d_EB2**alpha) * h_EB2 * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        rx_signal_E = np.sqrt(P_A_eff * alpha1) * h_E * tx_signal + np.sqrt(P_A_eff * alpha2) * h_E * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        rx_bits_B1 = (rx_signal_B1.real > 0).astype(int)
        rx_bits_B2 = (rx_signal_B2.real > 0).astype(int)
        rx_bits_E = (rx_signal_E.real > 0).astype(int)
        BER_B1[bob_idx, eve_idx] = np.mean(bits != rx_bits_B1)
        BER_B2[bob_idx, eve_idx] = np.mean(bits != rx_bits_B2)
        BER_E[bob_idx, eve_idx] = np.mean(bits != rx_bits_E)

        print(f"SNR_Bob = {SNR_Bob_dB} dB, SNR_Eve = {SNR_Eve_dB} dB | C_B1 = {C_B1[bob_idx, eve_idx]/1e6:.2f} Mbps | C_B2 = {C_B2[bob_idx, eve_idx]/1e6:.2f} Mbps | C_E = {C_E[bob_idx, eve_idx]/1e6:.2f} Mbps | BER_B1 = {BER_B1[bob_idx, eve_idx]:.4e} | BER_B2 = {BER_B2[bob_idx, eve_idx]:.4e} | BER_E = {BER_E[bob_idx, eve_idx]:.4e} | R_s1 = {R_s1[bob_idx, eve_idx]:.2f} | R_s2 = {R_s2[bob_idx, eve_idx]:.2f} | SOP1 = {SOP1[bob_idx, eve_idx]:.2f} | SOP2 = {SOP2[bob_idx, eve_idx]:.2f} | IP1 = {IP1[bob_idx, eve_idx]:.2f} | IP2 = {IP2[bob_idx, eve_idx]:.2f}")

# Lưu kết quả
np.save('simulation_results_snr.npy', {
    'SNR_Bob_dB': SNR_Bob_dB_range,
    'SNR_Eve_dB': SNR_Eve_dB_range,
    'R_s1': R_s1, 'R_s2': R_s2, 'R_s_sum': R_s_sum,
    'SOP1': SOP1, 'SOP2': SOP2,
    'IP1': IP1, 'IP2': IP2,
    'Erg_Rs1': Erg_Rs1, 'Erg_Rs2': Erg_Rs2,
    'Cs1': Cs1, 'Cs2': Cs2,
    'C_B1': C_B1, 'C_B2': C_B2, 'C_E': C_E,
    'BER_B1': BER_B1, 'BER_B2': BER_B2, 'BER_E': BER_E
})

# Vẽ biểu đồ
bob_idx_plot = np.where(SNR_Bob_dB_range == 20)[0][0]  # Cập nhật vẽ tại SNR_Bob = 20 dB
plt.figure(figsize=(8,6))
plt.plot(SNR_Eve_dB_range, R_s1[bob_idx_plot], 'g-o', label='Secrecy Rate Bob1')
plt.plot(SNR_Eve_dB_range, R_s2[bob_idx_plot], 'b-s', label='Secrecy Rate Bob2')
plt.plot(SNR_Eve_dB_range, R_s_sum[bob_idx_plot], 'k-^', label='Secrecy Sum Rate')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Secrecy Rate vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.plot(SNR_Eve_dB_range, SOP1[bob_idx_plot], 'g-o', label='SOP Bob1')
plt.plot(SNR_Eve_dB_range, SOP2[bob_idx_plot], 'b-s', label='SOP Bob2')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Outage Probability')
plt.title('Secrecy Outage Probability vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.plot(SNR_Eve_dB_range, IP1[bob_idx_plot], 'g-o', label='Intercept Prob. Bob1')
plt.plot(SNR_Eve_dB_range, IP2[bob_idx_plot], 'b-s', label='Intercept Prob. Bob2')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Intercept Probability')
plt.title('Intercept Probability vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.semilogy(SNR_Eve_dB_range, BER_B1[bob_idx_plot], 'g-o', label='BER Bob1')
plt.semilogy(SNR_Eve_dB_range, BER_B2[bob_idx_plot], 'b-s', label='BER Bob2')
plt.semilogy(SNR_Eve_dB_range, BER_E[bob_idx_plot], 'r-^', label='BER Eve')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('BER (BPSK, Rayleigh)')
plt.title('BER vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True, which='both')
plt.show()

# KỊCH BẢN 3: Multi-user NOMA, quét d_E (Eve chủ động gây nhiễu)
print("\n===== KỊCH BẢN 3: Multi-user NOMA, quét d_E (Eve chủ động gây nhiễu) =====")
d_E_range = np.arange(20, 151, 10)
P_E = 1  # Công suất nhiễu của Eve cố định
SNR_Bob_dB = 20  # Cập nhật SNR_Bob lên 20 dB
SNR_Bob_linear = 10**(SNR_Bob_dB / 10)
P_A_eff = SNR_Bob_linear * d_B1**alpha * N_0

print("==== THÔNG SỐ HỆ THỐNG KỊCH BẢN 3 ====")
print(f"Công suất truyền P_A: {P_A} W")
print(f"Nhiễu nền N_0: {N_0:.2e} W")
print(f"Hệ số suy hao alpha: {alpha}")
print(f"Băng thông: {B/1e6:.1f} MHz")
print(f"Khoảng cách: Bob1 = {d_B1}m, Bob2 = {d_B2}m, d_E = {d_E_range[0]}-{d_E_range[-1]}m (bước 10m)")
print(f"Phân bổ công suất: alpha1 = {alpha1:.3f}, alpha2 = {alpha2:.3f} (tổng = {alpha1+alpha2:.3f})")
print(f"Tỷ lệ lỗi SIC: epsilon = {epsilon}")
print(f"SNR_Bob: {SNR_Bob_dB} dB")
print("============================\n")

# Khởi tạo mảng kết quả
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
    # Kênh fading
    h_B1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_B2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_E = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_EB1 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    h_EB2 = np.sqrt(0.5) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    d_EB1 = abs(d_E - d_B1) + 1e-3
    d_EB2 = abs(d_E - d_B2) + 1e-3

    # SNR (Cập nhật: Thêm nhiễu chéo cho SNR_E)
    SNR_B2 = (P_A_eff * alpha2 * np.abs(h_B2)**2) / (d_B2**alpha * N_0 + P_E * np.abs(h_EB2)**2 / (d_EB2**alpha))
    SNR_B1 = (P_A_eff * alpha1 * np.abs(h_B1)**2) / (d_B1**alpha * N_0 + epsilon * P_A_eff * alpha2 * np.abs(h_B1)**2 + P_E * np.abs(h_EB1)**2 / (d_EB1**alpha))
    I_Bob = P_A_eff * np.abs(h_E)**2 / (d_E**alpha)  # Nhiễu chéo tổng hợp từ Bob
    SNR_E1 = (P_A_eff * alpha1 * np.abs(h_E)**2) / (d_E**alpha * N_0 + I_Bob)
    SNR_E2 = (P_A_eff * alpha2 * np.abs(h_E)**2) / (d_E**alpha * N_0 + I_Bob)

    # Dung lượng kênh
    R1 = np.log2(1 + SNR_B1)
    R2 = np.log2(1 + SNR_B2)
    Re1 = np.log2(1 + SNR_E1)
    Re2 = np.log2(1 + SNR_E2)

    # Secrecy Rate
    Rs1 = np.maximum(0, R1 - Re1)
    Rs2 = np.maximum(0, R2 - Re2)
    R_s1_3[idx] = np.mean(Rs1)
    R_s2_3[idx] = np.mean(Rs2)
    R_s_sum_3[idx] = R_s1_3[idx] + R_s2_3[idx]

    # Secrecy Outage Probability
    SOP1_3[idx] = np.mean(Rs1 < R_th)
    SOP2_3[idx] = np.mean(Rs2 < R_th)

    # Intercept Probability
    IP1_3[idx] = np.mean(Re1 >= R1)
    IP2_3[idx] = np.mean(Re2 >= R2)

    # Ergodic Secrecy Rate
    Erg_Rs1_3[idx] = np.mean(Rs1)
    Erg_Rs2_3[idx] = np.mean(Rs2)

    # Secrecy Capacity
    Cs1_3[idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B1) - np.log2(1 + SNR_E1)))
    Cs2_3[idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B2) - np.log2(1 + SNR_E2)))

    # Dung lượng kênh trung bình
    C_B1_3[idx] = np.mean(B * np.log2(1 + SNR_B1))
    C_B2_3[idx] = np.mean(B * np.log2(1 + SNR_B2))
    C_E_3[idx] = np.mean(B * np.log2(1 + np.maximum(SNR_E1, SNR_E2)))

    # BER (Mô phỏng BPSK thực tế)
    bits = np.random.randint(0, 2, num_samples)
    tx_signal = 2 * bits - 1
    rx_signal_B1 = np.sqrt(P_A_eff * alpha1) * h_B1 * tx_signal + np.sqrt(epsilon * P_A_eff * alpha2) * h_B1 * tx_signal + np.sqrt(P_E / d_EB1**alpha) * h_EB1 * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    rx_signal_B2 = np.sqrt(P_A_eff * alpha2) * h_B2 * tx_signal + np.sqrt(P_E / d_EB2**alpha) * h_EB2 * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    rx_signal_E = np.sqrt(P_A_eff * alpha1) * h_E * tx_signal + np.sqrt(P_A_eff * alpha2) * h_E * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
    rx_bits_B1 = (rx_signal_B1.real > 0).astype(int)
    rx_bits_B2 = (rx_signal_B2.real > 0).astype(int)
    rx_bits_E = (rx_signal_E.real > 0).astype(int)
    BER_B1_3[idx] = np.mean(bits != rx_bits_B1)
    BER_B2_3[idx] = np.mean(bits != rx_bits_B2)
    BER_E_3[idx] = np.mean(bits != rx_bits_E)

    print(f"d_E = {d_E} m | C_B1 = {C_B1_3[idx]/1e6:.2f} Mbps | C_B2 = {C_B2_3[idx]/1e6:.2f} Mbps | C_E = {C_E_3[idx]/1e6:.2f} Mbps | BER_B1 = {BER_B1_3[idx]:.4e} | BER_B2 = {BER_B2_3[idx]:.4e} | BER_E = {BER_E_3[idx]:.4e} | R_s1 = {R_s1_3[idx]:.2f} | R_s2 = {R_s2_3[idx]:.2f} | SOP1 = {SOP1_3[idx]:.2f} | SOP2 = {SOP2_3[idx]:.2f} | IP1 = {IP1_3[idx]:.2f} | IP2 = {IP2_3[idx]:.2f}")

# Lưu kết quả
np.save('simulation_results_de.npy', {
    'd_E': d_E_range,
    'R_s1': R_s1_3, 'R_s2': R_s2_3, 'R_s_sum': R_s_sum_3,
    'SOP1': SOP1_3, 'SOP2': SOP2_3,
    'IP1': IP1_3, 'IP2': IP2_3,
    'Erg_Rs1': Erg_Rs1_3, 'Erg_Rs2': Erg_Rs2_3,
    'Cs1': Cs1_3, 'Cs2': Cs2_3,
    'C_B1': C_B1_3, 'C_B2': C_B2_3, 'C_E': C_E_3,
    'BER_B1': BER_B1_3, 'BER_B2': BER_B2_3, 'BER_E': BER_E_3
})

# Vẽ biểu đồ
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