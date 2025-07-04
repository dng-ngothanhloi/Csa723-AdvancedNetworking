import numpy as np
import matplotlib.pyplot as plt
from numba import jit

@jit(nopython=True)
def compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A, alpha1, alpha2, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant):
    norm_h_B1 = np.sum(np.abs(h_B1)**2, axis=1)
    norm_h_B2 = np.sum(np.abs(h_B2)**2, axis=1)
    norm_h_E = np.sum(np.abs(h_E)**2, axis=1)
    norm_h_EB1 = np.sum(np.abs(h_EB1)**2, axis=1)
    norm_h_EB2 = np.sum(np.abs(h_EB2)**2, axis=1)
    
    SNR_B2 = (P_A * alpha2 * norm_h_B2) / (d_B2**alpha * N_0 + P_E * norm_h_EB2 / d_EB2**alpha)
    SNR_B1 = (P_A * alpha1 * norm_h_B1) / (d_B1**alpha * N_0 + epsilon * P_A * alpha2 * norm_h_B1 + P_E * norm_h_EB1 / d_EB1**alpha)
    SNR_E1 = (P_A * alpha1 * norm_h_E) / (d_E**alpha * N_0)
    SNR_E2 = (P_A * alpha2 * norm_h_E) / (d_E**alpha * N_0)
    return SNR_B1, SNR_B2, SNR_E1, SNR_E2

# Thông số hệ thống
P_A = 0.1  # 100mW
N_0 = 1e-15
alpha = 3
B = 10e6
num_samples = int(1e3)  # Giảm số mẫu
N_ant = 16
d_B1, d_B2, d_E = 30, 70, 50
epsilon = 0.01
alpha1, alpha2 = 0.3, 0.7

# Quét SNR
SNR_Bob_dB_range = np.arange(10, 21, 5)  # Giảm range
SNR_Eve_dB_range = np.arange(0, 21, 5)

R_s1 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
R_s2 = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))
R_s_sum = np.zeros((len(SNR_Bob_dB_range), len(SNR_Eve_dB_range)))

for bob_idx, SNR_Bob_dB in enumerate(SNR_Bob_dB_range):
    SNR_Bob_linear = 10**(SNR_Bob_dB / 10)
    P_A_eff = SNR_Bob_linear * d_B1**alpha * N_0

    for eve_idx, SNR_Eve_dB in enumerate(SNR_Eve_dB_range):
        SNR_Eve_linear = 10**(SNR_Eve_dB / 10)
        P_E = SNR_Eve_linear * d_E**alpha * N_0

        h_B1 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_B2 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_E = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_EB1 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        h_EB2 = np.sqrt(0.5) * (np.random.randn(num_samples, N_ant) + 1j * np.random.randn(num_samples, N_ant))
        
        d_EB1 = max(abs(d_E - d_B1), 5.0)
        d_EB2 = max(abs(d_E - d_B2), 5.0)

        SNR_B1, SNR_B2, SNR_E1, SNR_E2 = compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A_eff, alpha1, alpha2, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant)

        R1 = np.log2(1 + SNR_B1)
        R2 = np.log2(1 + SNR_B2)
        Re1 = np.log2(1 + SNR_E1)
        Re2 = np.log2(1 + SNR_E2)

        Rs1 = np.maximum(0, R1 - Re1)
        Rs2 = np.maximum(0, R2 - Re2)
        R_s1[bob_idx, eve_idx] = np.mean(Rs1)
        R_s2[bob_idx, eve_idx] = np.mean(Rs2)
        R_s_sum[bob_idx, eve_idx] = R_s1[bob_idx, eve_idx] + R_s2[bob_idx, eve_idx]

np.save('quick_baseline.npy', {
    'R_s1': R_s1, 'R_s2': R_s2, 'R_s_sum': R_s_sum,
    'SNR_Bob_dB': SNR_Bob_dB_range, 'SNR_Eve_dB': SNR_Eve_dB_range
})
print("Baseline completed")
