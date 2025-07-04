import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from tabulate import tabulate

# Hàm tính SNR với numba, tích hợp AN
@jit(nopython=True)
def compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A, alpha1, alpha2, phi, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant):
    # Tính norm của kênh cho Massive MIMO
    norm_h_B1 = np.sum(np.abs(h_B1)**2, axis=1)
    norm_h_B2 = np.sum(np.abs(h_B2)**2, axis=1)
    norm_h_E = np.sum(np.abs(h_E)**2, axis=1)
    norm_h_EB1 = np.sum(np.abs(h_EB1)**2, axis=1)
    norm_h_EB2 = np.sum(np.abs(h_EB2)**2, axis=1)

    # Công suất tín hiệu sau khi trừ công suất AN
    P_s = P_A * (1 - phi)

    # SNR với AN
    SNR_B2 = (P_s * alpha2 * norm_h_B2) / (d_B2**alpha * N_0 + P_E * norm_h_EB2 / d_EB2**alpha)
    SNR_B1 = (P_s * alpha1 * norm_h_B1) / (d_B1**alpha * N_0 + epsilon * P_s * alpha2 * norm_h_B1 + P_E * norm_h_EB1 / d_EB1**alpha)
    I_Bob = P_s * norm_h_E / d_E**alpha
    SNR_E1 = (P_s * alpha1 * norm_h_E) / (d_E**alpha * N_0 + I_Bob + P_A * phi * norm_h_E / d_E**alpha)
    SNR_E2 = (P_s * alpha2 * norm_h_E) / (d_E**alpha * N_0 + P_A * norm_h_EB2 / d_EB2**alpha + P_A * phi * norm_h_E / d_E**alpha)
    return SNR_B1, SNR_B2, SNR_E1, SNR_E2

# KỊCH BẢN 2: Multi-user NOMA, quét SNR_Eve (Eve chủ động gây nhiễu)
print("\n===== KỊCH BẢN 2: Multi-user NOMA, quét SNR_Eve (Eve chủ động gây nhiễu) =====")
# Thông số hệ thống
P_A = 1  # Công suất truyền tổng (W) ~ 30 dBm
N_0 = 1e-15  # Nhiễu nền (W)
alpha = 3  # Hệ số suy hao kênh
B = 10e6  # Băng thông (Hz)
num_samples = int(1e5)  # Số lần mô phỏng Monte Carlo
N_ant = 16  # Số anten (Massive MIMO)
d_B1 = 30  # Khoảng cách Bob1 (m)
d_B2 = 70  # Khoảng cách Bob2 (m)
d_E = 50  # Khoảng cách Eve cố định (m)
R_th = 1.0  # Ngưỡng bảo mật (bits/s/Hz)
epsilon = 0.005  # Tỷ lệ lỗi SIC
pilot_contamination_power = 0.0  # Công suất nhiễu pilot - loại bỏ Nhiễu Định vị của EVE
phi_values = [0.3]  # Tỷ lệ công suất AN

# Phân bổ công suất
alpha1 = 0.3
alpha2 = 1 - alpha1

print("==== THÔNG SỐ HỆ THỐNG KỊCH BẢN 2 ====")
print(f"Công suất truyền P_A: {P_A} W")
print(f"Nhiễu nền N_0: {N_0:.2e} W")
print(f"Hệ số suy hao alpha: {alpha}")
print(f"Băng thông: {B/1e6:.1f} MHz")
print(f"Số anten: {N_ant}")
print(f"Khoảng cách: Bob1 = {d_B1}m, Bob2 = {d_B2}m, Eve = {d_E}m")
print(f"Phân bổ công suất: alpha1 = {alpha1:.3f}, alpha2 = {alpha2:.3f} (tổng = {alpha1+alpha2:.3f})")
print(f"Tỷ lệ lỗi SIC: epsilon = {epsilon}")
print(f"Công suất nhiễu pilot: {pilot_contamination_power}")
print(f"Tỷ lệ công suất AN: phi = {phi_values}")
print("============================\n")

# Quét SNR_Bob và SNR_Eve
SNR_Bob_dB_range = np.arange(0, 21, 2)
SNR_Eve_dB_range = np.arange(0, 21, 2)

# Khởi tạo mảng kết quả cho Kịch bản 2
C_B1_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
C_B2_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
C_E_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
BER_B1_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
BER_B2_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
BER_E_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
R_s1_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
R_s2_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
R_s_sum_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
SOP1_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
SOP2_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
IP1_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
IP2_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
Erg_Rs1_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
Erg_Rs2_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
Cs1_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
Cs2_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
eta_s1_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))
eta_s2_2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range), len(phi_values)))

for phi_idx, phi in enumerate(phi_values):
    for bob_idx, SNR_Bob_dB in enumerate(SNR_Bob_dB_range):
        SNR_Bob_linear = 10**(SNR_Bob_dB / 10)
        P_A_eff = SNR_Bob_linear * d_B1**alpha * N_0  # Công suất hiệu quả

        for eve_idx, SNR_Eve_dB in enumerate(SNR_Eve_dB_range):
            SNR_Eve_linear = 10**(SNR_Eve_dB / 10)
            P_E = SNR_Eve_linear * d_E**alpha * N_0  # Công suất nhiễu của Eve

            # Kênh fading với Massive MIMO
            h_B1 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
            h_B2 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
            h_E = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
            h_EB1 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
            h_EB2 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))

            # Thêm ô nhiễm định vị
            pilot_contamination = pilot_contamination_power * np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
            h_B1 = h_B1 + pilot_contamination
            h_B2 = h_B2 + pilot_contamination

            d_EB1 = abs(d_E - d_B1) + 1e-3
            d_EB2 = max(abs(d_E - d_B2), 1)

            # Tính SNR với AN
            SNR_B1, SNR_B2, SNR_E1, SNR_E2 = compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A_eff, alpha1, alpha2, phi, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant)

            # Dung lượng kênh
            R1 = np.log2(1 + SNR_B1)
            R2 = np.log2(1 + SNR_B2)
            Re1 = np.log2(1 + SNR_E1)
            Re2 = np.log2(1 + SNR_E2)

            # Secrecy Rate
            Rs1 = np.maximum(0, R1 - Re1)
            Rs2 = np.maximum(0, R2 - Re2)
            R_s1_2[bob_idx, eve_idx, phi_idx] = np.mean(Rs1)
            R_s2_2[bob_idx, eve_idx, phi_idx] = np.mean(Rs2)
            R_s_sum_2[bob_idx, eve_idx, phi_idx] = R_s1_2[bob_idx, eve_idx, phi_idx] + R_s2_2[bob_idx, eve_idx, phi_idx]

            # Secrecy Outage Probability
            SOP1_2[bob_idx, eve_idx, phi_idx] = np.mean(Rs1 < R_th)
            SOP2_2[bob_idx, eve_idx, phi_idx] = np.mean(Rs2 < R_th)

            # Intercept Probability
            IP1_2[bob_idx, eve_idx, phi_idx] = np.mean(Re1 >= R1)
            IP2_2[bob_idx, eve_idx, phi_idx] = np.mean(Re2 >= R2)

            # Ergodic Secrecy Rate
            Erg_Rs1_2[bob_idx, eve_idx, phi_idx] = np.mean(Rs1)
            Erg_Rs2_2[bob_idx, eve_idx, phi_idx] = np.mean(Rs2)

            # Secrecy Capacity
            Cs1_2[bob_idx, eve_idx, phi_idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B1) - np.log2(1 + SNR_E1)))
            Cs2_2[bob_idx, eve_idx, phi_idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B2) - np.log2(1 + SNR_E2)))

            # Hiệu suất phổ bí mật
            eta_s1_2[bob_idx, eve_idx, phi_idx] = R_s1_2[bob_idx, eve_idx, phi_idx] / B
            eta_s2_2[bob_idx, eve_idx, phi_idx] = R_s2_2[bob_idx, eve_idx, phi_idx] / B

            # Dung lượng kênh trung bình
            C_B1_2[bob_idx, eve_idx, phi_idx] = np.mean(B * np.log2(1 + SNR_B1))
            C_B2_2[bob_idx, eve_idx, phi_idx] = np.mean(B * np.log2(1 + SNR_B2))
            C_E_2[bob_idx, eve_idx, phi_idx] = np.mean(B * np.log2(1 + np.maximum(SNR_E1, SNR_E2)))

            # BER (Mô phỏng BPSK thực tế)
            bits = np.random.randint(0, 2, num_samples)
            tx_signal = 2 * bits - 1
            P_s = P_A_eff * (1 - phi)
            norm_h_E = np.sum(np.abs(h_E)**2, axis=1)  # Tính norm_h_E cho nhiễu AN
            rx_signal_B1 = np.sqrt(P_s * alpha1) * np.sum(h_B1, axis=1) * tx_signal + np.sqrt(epsilon * P_s * alpha2) * np.sum(h_B1, axis=1) * tx_signal + np.sqrt(P_E / d_EB1**alpha) * np.sum(h_EB1, axis=1) * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
            rx_signal_B2 = np.sqrt(P_s * alpha2) * np.sum(h_B2, axis=1) * tx_signal + np.sqrt(P_E / d_EB2**alpha) * np.sum(h_EB2, axis=1) * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
            rx_signal_E = np.sqrt(P_s * alpha1) * np.sum(h_E, axis=1) * tx_signal + np.sqrt(P_s * alpha2) * np.sum(h_E, axis=1) * tx_signal + np.sqrt(P_A_eff * phi * norm_h_E / d_E**alpha) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples)) + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
            rx_bits_B1 = (rx_signal_B1.real > 0).astype(int)
            rx_bits_B2 = (rx_signal_B2.real > 0).astype(int)
            rx_bits_E = (rx_signal_E.real > 0).astype(int)
            BER_B1_2[bob_idx, eve_idx, phi_idx] = np.mean(bits != rx_bits_B1)
            BER_B2_2[bob_idx, eve_idx, phi_idx] = np.mean(bits != rx_bits_B2)
            BER_E_2[bob_idx, eve_idx, phi_idx] = np.mean(bits != rx_bits_E)

            print(f"SNR_Bob = {SNR_Bob_dB} dB, SNR_Eve = {SNR_Eve_dB} dB, phi = {phi} | C_B1 = {C_B1_2[bob_idx, eve_idx, phi_idx]/1e6:.2f} Mbps | C_B2 = {C_B2_2[bob_idx, eve_idx, phi_idx]/1e6:.2f} Mbps | C_E = {C_E_2[bob_idx, eve_idx, phi_idx]/1e6:.2f} Mbps | BER_B1 = {BER_B1_2[bob_idx, eve_idx, phi_idx]:.4e} | BER_B2 = {BER_B2_2[bob_idx, eve_idx, phi_idx]:.4e} | BER_E = {BER_E_2[bob_idx, eve_idx, phi_idx]:.4e} | R_s1 = {R_s1_2[bob_idx, eve_idx, phi_idx]:.2f} | R_s2 = {R_s2_2[bob_idx, eve_idx, phi_idx]:.2f} | SOP1 = {SOP1_2[bob_idx, eve_idx, phi_idx]:.2f} | SOP2 = {SOP2_2[bob_idx, eve_idx, phi_idx]:.2f} | IP1 = {IP1_2[bob_idx, eve_idx, phi_idx]:.2f} | IP2 = {IP2_2[bob_idx, eve_idx, phi_idx]:.2f} | eta_s1 = {eta_s1_2[bob_idx, eve_idx, phi_idx]:.2e} | eta_s2 = {eta_s2_2[bob_idx, eve_idx, phi_idx]:.2e}")

# Lưu kết quả Kịch bản 2
np.save('simulation_results_snr_an.npy', {
    'SNR_Bob_dB': SNR_Bob_dB_range,
    'SNR_Eve_dB': SNR_Eve_dB_range,
    'phi': np.array(phi_values),
    'R_s1': R_s1_2, 'R_s2': R_s2_2, 'R_s_sum': R_s_sum_2,
    'SOP1': SOP1_2, 'SOP2': SOP2_2,
    'IP1': IP1_2, 'IP2': IP2_2,
    'Erg_Rs1': Erg_Rs1_2, 'Erg_Rs2': Erg_Rs2_2,
    'Cs1': Cs1_2, 'Cs2': Cs2_2,
    'C_B1': C_B1_2, 'C_B2': C_B2_2, 'C_E': C_E_2,
    'BER_B1': BER_B1_2, 'BER_B2': BER_B2_2, 'BER_E': BER_E_2,
    'eta_s1': eta_s1_2, 'eta_s2': eta_s2_2
})

# Vẽ biểu đồ Kịch bản 2
bob_idx_plot = np.where(SNR_Bob_dB_range == 20)[0][0]
plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.plot(SNR_Eve_dB_range, R_s1_2[bob_idx_plot, :, phi_idx], label=f'R_s1, phi={phi}', linestyle='-', marker='o')
    plt.plot(SNR_Eve_dB_range, R_s2_2[bob_idx_plot, :, phi_idx], label=f'R_s2, phi={phi}', linestyle='--', marker='s')
    plt.plot(SNR_Eve_dB_range, R_s_sum_2[bob_idx_plot, :, phi_idx], label=f'R_s_sum, phi={phi}', linestyle=':', marker='^')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Secrecy Rate vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.savefig('scenario_2_rs1_rs2_an.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.plot(SNR_Eve_dB_range, SOP1_2[bob_idx_plot, :, phi_idx], label=f'SOP1, phi={phi}', linestyle='-', marker='o')
    plt.plot(SNR_Eve_dB_range, SOP2_2[bob_idx_plot, :, phi_idx], label=f'SOP2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Outage Probability')
plt.title('Secrecy Outage Probability vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.savefig('scenario_2_sop1_sop2_an.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.plot(SNR_Eve_dB_range, IP1_2[bob_idx_plot, :, phi_idx], label=f'IP1, phi={phi}', linestyle='-', marker='o')
    plt.plot(SNR_Eve_dB_range, IP2_2[bob_idx_plot, :, phi_idx], label=f'IP2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Intercept Probability')
plt.title('Intercept Probability vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.savefig('scenario_2_ip1_ip2_an.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.semilogy(SNR_Eve_dB_range, BER_B1_2[bob_idx_plot, :, phi_idx], label=f'BER_B1, phi={phi}', linestyle='-', marker='o')
    plt.semilogy(SNR_Eve_dB_range, BER_B2_2[bob_idx_plot, :, phi_idx], label=f'BER_B2, phi={phi}', linestyle='--', marker='s')
    plt.semilogy(SNR_Eve_dB_range, BER_E_2[bob_idx_plot, :, phi_idx], label=f'BER_E, phi={phi}', linestyle=':', marker='^')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('BER (BPSK, Rayleigh)')
plt.title('BER vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True, which='both')
plt.savefig('scenario_2_ber_b1_b2_e_an.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.plot(SNR_Eve_dB_range, eta_s1_2[bob_idx_plot, :, phi_idx], label=f'eta_s1, phi={phi}', linestyle='-', marker='o')
    plt.plot(SNR_Eve_dB_range, eta_s2_2[bob_idx_plot, :, phi_idx], label=f'eta_s2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Spectral Efficiency (bits/s/Hz)')
plt.title('Secrecy Spectral Efficiency vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.savefig('scenario_2_eta_s1_s2_an.png')
plt.show()
plt.close()

# KỊCH BẢN 3: Multi-user NOMA, quét d_E (Eve chủ động gây nhiễu)
print("\n===== KỊCH BẢN 3: Multi-user NOMA, quét d_E (Eve chủ động gây nhiễu) =====")
d_E_range = np.arange(20, 151, 10)
SNR_Bob_dB = 20
SNR_Eve_dB = 30
SNR_Bob_linear = 10**(SNR_Bob_dB / 10)
SNR_Eve_linear = 10**(SNR_Eve_dB / 10)
P_A_eff = SNR_Bob_linear * d_B1**alpha * N_0
num_samples = int(1e5)  # Đồng bộ với mã gốc
min_distance = 5  # Ràng buộc khoảng cách tối thiểu

print("==== THÔNG SỐ HỆ THỐNG KỊCH BẢN 3 ====")
print(f"Công suất truyền P_A: {P_A} W")
print(f"Nhiễu nền N_0: {N_0:.2e} W")
print(f"Hệ số suy hao alpha: {alpha}")
print(f"Băng thông: {B/1e6:.1f} MHz")
print(f"Số anten: {N_ant}")
print(f"Khoảng cách: Bob1 = {d_B1}m, Bob2 = {d_B2}m, d_E = {d_E_range[0]}-{d_E_range[-1]}m (bước 10m)")
print(f"Phân bổ công suất: alpha1 = {alpha1:.3f}, alpha2 = {alpha2:.3f} (tổng = {alpha1+alpha2:.3f})")
print(f"Tỷ lệ lỗi SIC: epsilon = {epsilon}")
print(f"SNR_Bob: {SNR_Bob_dB} dB, SNR_Eve: {SNR_Eve_dB} dB")
print(f"Công suất nhiễu pilot: {pilot_contamination_power}")
print(f"Tỷ lệ công suất AN: phi = {phi_values}")
print(f"Ràng buộc khoảng cách: min(|d_Bi - d_E|) >= {min_distance} m")
print("============================\n")

# Khởi tạo mảng kết quả cho Kịch bản 3
C_B1_3 = np.zeros((len(d_E_range), len(phi_values)))
C_B2_3 = np.zeros((len(d_E_range), len(phi_values)))
C_E_3 = np.zeros((len(d_E_range), len(phi_values)))
BER_B1_3 = np.zeros((len(d_E_range), len(phi_values)))
BER_B2_3 = np.zeros((len(d_E_range), len(phi_values)))
BER_E_3 = np.zeros((len(d_E_range), len(phi_values)))
R_s1_3 = np.zeros((len(d_E_range), len(phi_values)))
R_s2_3 = np.zeros((len(d_E_range), len(phi_values)))
R_s_sum_3 = np.zeros((len(d_E_range), len(phi_values)))
SOP1_3 = np.zeros((len(d_E_range), len(phi_values)))
SOP2_3 = np.zeros((len(d_E_range), len(phi_values)))
IP1_3 = np.zeros((len(d_E_range), len(phi_values)))
IP2_3 = np.zeros((len(d_E_range), len(phi_values)))
Erg_Rs1_3 = np.zeros((len(d_E_range), len(phi_values)))
Erg_Rs2_3 = np.zeros((len(d_E_range), len(phi_values)))
Cs1_3 = np.zeros((len(d_E_range), len(phi_values)))
Cs2_3 = np.zeros((len(d_E_range), len(phi_values)))
eta_s1_3 = np.zeros((len(d_E_range), len(phi_values)))
eta_s2_3 = np.zeros((len(d_E_range), len(phi_values)))

for phi_idx, phi in enumerate(phi_values):
    for idx, d_E in enumerate(d_E_range):
        # Áp dụng ràng buộc min(|d_Bi - d_E|) >= 5 m
        if abs(d_E - d_B1) < min_distance:
            d_E = d_B1 + min_distance
            print(f"Adjusted d_E from {d_E_range[idx]} to {d_E} to satisfy min(|d_B1 - d_E|) >= {min_distance} m")
        if abs(d_E - d_B2) < min_distance:
            d_E = d_B2 + min_distance
            print(f"Adjusted d_E from {d_E_range[idx]} to {d_E} to satisfy min(|d_B2 - d_E|) >= {min_distance} m")

        P_E = SNR_Eve_linear * d_E**alpha * N_0

        # Kênh fading với Massive MIMO
        h_B1 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_B2 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_E = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_EB1 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_EB2 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))

        # Thêm ô nhiễm định vị
        pilot_contamination = pilot_contamination_power * np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_B1 = h_B1 + pilot_contamination
        h_B2 = h_B2 + pilot_contamination

        d_EB1 = abs(d_E - d_B1) + 1e-3
        d_EB2 = max(abs(d_E - d_B2), 1)

        # Tính SNR với AN
        SNR_B1, SNR_B2, SNR_E1, SNR_E2 = compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A_eff, alpha1, alpha2, phi, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant)

        # Dung lượng kênh
        R1 = np.log2(1 + SNR_B1)
        R2 = np.log2(1 + SNR_B2)
        Re1 = np.log2(1 + SNR_E1)
        Re2 = np.log2(1 + SNR_E2)

        # Secrecy Rate
        Rs1 = np.maximum(0, R1 - Re1)
        Rs2 = np.maximum(0, R2 - Re2)
        R_s1_3[idx, phi_idx] = np.mean(Rs1)
        R_s2_3[idx, phi_idx] = np.mean(Rs2)
        R_s_sum_3[idx, phi_idx] = R_s1_3[idx, phi_idx] + R_s2_3[idx, phi_idx]

        # Secrecy Outage Probability
        SOP1_3[idx, phi_idx] = np.mean(Rs1 < R_th)
        SOP2_3[idx, phi_idx] = np.mean(Rs2 < R_th)

        # Intercept Probability
        IP1_3[idx, phi_idx] = np.mean(Re1 >= R1)
        IP2_3[idx, phi_idx] = np.mean(Re2 >= R2)

        # Ergodic Secrecy Rate
        Erg_Rs1_3[idx, phi_idx] = np.mean(Rs1)
        Erg_Rs2_3[idx, phi_idx] = np.mean(Rs2)

        # Secrecy Capacity
        Cs1_3[idx, phi_idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B1) - np.log2(1 + SNR_E1)))
        Cs2_3[idx, phi_idx] = np.mean(np.maximum(0, np.log2(1 + SNR_B2) - np.log2(1 + SNR_E2)))

        # Hiệu suất phổ bí mật
        eta_s1_3[idx, phi_idx] = R_s1_3[idx, phi_idx] / B
        eta_s2_3[idx, phi_idx] = R_s2_3[idx, phi_idx] / B

        # Dung lượng kênh trung bình
        C_B1_3[idx, phi_idx] = np.mean(B * np.log2(1 + SNR_B1))
        C_B2_3[idx, phi_idx] = np.mean(B * np.log2(1 + SNR_B2))
        C_E_3[idx, phi_idx] = np.mean(B * np.log2(1 + np.maximum(SNR_E1, SNR_E2)))

        # BER (Mô phỏng BPSK thực tế)
        bits = np.random.randint(0, 2, num_samples)
        tx_signal = 2 * bits - 1
        P_s = P_A_eff * (1 - phi)
        norm_h_E = np.sum(np.abs(h_E)**2, axis=1)
        rx_signal_B1 = np.sqrt(P_s * alpha1) * np.sum(h_B1, axis=1) * tx_signal + np.sqrt(epsilon * P_s * alpha2) * np.sum(h_B1, axis=1) * tx_signal + np.sqrt(P_E / d_EB1**alpha) * np.sum(h_EB1, axis=1) * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        rx_signal_B2 = np.sqrt(P_s * alpha2) * np.sum(h_B2, axis=1) * tx_signal + np.sqrt(P_E / d_EB2**alpha) * np.sum(h_EB2, axis=1) * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        rx_signal_E = np.sqrt(P_s * alpha1) * np.sum(h_E, axis=1) * tx_signal + np.sqrt(P_s * alpha2) * np.sum(h_E, axis=1) * tx_signal + np.sqrt(P_A_eff * phi * norm_h_E / d_E**alpha) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples)) + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
        rx_bits_B1 = (rx_signal_B1.real > 0).astype(int)
        rx_bits_B2 = (rx_signal_B2.real > 0).astype(int)
        rx_bits_E = (rx_signal_E.real > 0).astype(int)
        BER_B1_3[idx, phi_idx] = np.mean(bits != rx_bits_B1)
        BER_B2_3[idx, phi_idx] = np.mean(bits != rx_bits_B2)
        BER_E_3[idx, phi_idx] = np.mean(bits != rx_bits_E)

        print(f"d_E = {d_E} m, phi = {phi} | C_B1 = {C_B1_3[idx, phi_idx]/1e6:.2f} Mbps | C_B2 = {C_B2_3[idx, phi_idx]/1e6:.2f} Mbps | C_E = {C_E_3[idx, phi_idx]/1e6:.2f} Mbps | BER_B1 = {BER_B1_3[idx, phi_idx]:.4e} | BER_B2 = {BER_B2_3[idx, phi_idx]:.4e} | BER_E = {BER_E_3[idx, phi_idx]:.4e} | R_s1 = {R_s1_3[idx, phi_idx]:.2f} | R_s2 = {R_s2_3[idx, phi_idx]:.2f} | SOP1 = {SOP1_3[idx, phi_idx]:.2f} | SOP2 = {SOP2_3[idx, phi_idx]:.2f} | IP1 = {IP1_3[idx, phi_idx]:.2f} | IP2 = {IP2_3[idx, phi_idx]:.2f} | eta_s1 = {eta_s1_3[idx, phi_idx]:.2e} | eta_s2 = {eta_s2_3[idx, phi_idx]:.2e}")

# Lưu kết quả Kịch bản 3
np.save('simulation_results_de_an.npy', {
    'd_E': d_E_range,
    'phi': np.array(phi_values),
    'R_s1': R_s1_3, 'R_s2': R_s2_3, 'R_s_sum': R_s_sum_3,
    'SOP1': SOP1_3, 'SOP2': SOP2_3,
    'IP1': IP1_3, 'IP2': IP2_3,
    'Erg_Rs1': Erg_Rs1_3, 'Erg_Rs2': Erg_Rs2_3,
    'Cs1': Cs1_3, 'Cs2': Cs2_3,
    'C_B1': C_B1_3, 'C_B2': C_B2_3, 'C_E': C_E_3,
    'BER_B1': BER_B1_3, 'BER_B2': BER_B2_3, 'BER_E': BER_E_3,
    'eta_s1': eta_s1_3, 'eta_s2': eta_s2_3
})

# Vẽ biểu đồ Kịch bản 3
plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.plot(d_E_range, R_s1_3[:, phi_idx], label=f'R_s1, phi={phi}', linestyle='-', marker='o')
    plt.plot(d_E_range, R_s2_3[:, phi_idx], label=f'R_s2, phi={phi}', linestyle='--', marker='s')
    plt.plot(d_E_range, R_s_sum_3[:, phi_idx], label=f'R_s_sum, phi={phi}', linestyle=':', marker='^')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Secrecy Rate vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True)
plt.savefig('scenario_3_rs1_rs2_an.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.plot(d_E_range, SOP1_3[:, phi_idx], label=f'SOP1, phi={phi}', linestyle='-', marker='o')
    plt.plot(d_E_range, SOP2_3[:, phi_idx], label=f'SOP2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Secrecy Outage Probability')
plt.title('Secrecy Outage Probability vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True)
plt.savefig('scenario_3_sop1_sop2_an.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.plot(d_E_range, IP1_3[:, phi_idx], label=f'IP1, phi={phi}', linestyle='-', marker='o')
    plt.plot(d_E_range, IP2_3[:, phi_idx], label=f'IP2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Intercept Probability')
plt.title('Intercept Probability vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True)
plt.savefig('scenario_3_ip1_ip2_an.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.semilogy(d_E_range, BER_B1_3[:, phi_idx], label=f'BER_B1, phi={phi}', linestyle='-', marker='o')
    plt.semilogy(d_E_range, BER_B2_3[:, phi_idx], label=f'BER_B2, phi={phi}', linestyle='--', marker='s')
    plt.semilogy(d_E_range, BER_E_3[:, phi_idx], label=f'BER_E, phi={phi}', linestyle=':', marker='^')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('BER (BPSK, Rayleigh)')
plt.title('BER vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True, which='both')
plt.savefig('scenario_3_ber_b1_b2_e_an.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
for phi_idx, phi in enumerate(phi_values):
    plt.plot(d_E_range, eta_s1_3[:, phi_idx], label=f'eta_s1, phi={phi}', linestyle='-', marker='o')
    plt.plot(d_E_range, eta_s2_3[:, phi_idx], label=f'eta_s2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Secrecy Spectral Efficiency (bits/s/Hz)')
plt.title('Secrecy Spectral Efficiency vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True)
plt.savefig('scenario_3_eta_s1_s2_an.png')
plt.show()
plt.close()