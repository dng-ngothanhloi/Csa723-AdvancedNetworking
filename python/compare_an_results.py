import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Hàm để tải dữ liệu từ file .npy
def load_results(file_path):
    data = np.load(file_path, allow_pickle=True).item()
    return data

# Hàm tính sai số tương đối
def relative_difference(metric_an, metric_no_an, epsilon=1e-10):
    return np.abs(metric_an - metric_no_an) / (np.abs(metric_no_an) + epsilon)

# Tải dữ liệu
results_snr = load_results('simulation_results_snr.npy')
results_de = load_results('simulation_results_de.npy')
results_snr_an = load_results('simulation_results_snr_an.npy')
results_de_an = load_results('simulation_results_de_an.npy')

# Kiểm tra dữ liệu
print("Kiểm tra dữ liệu đã tải:")
print("Kịch bản 2 (SNR):", list(results_snr.keys()))
print("Kịch bản 3 (d_E):", list(results_de.keys()))
print("Kịch bản 2 (SNR, AN):", list(results_snr_an.keys()))
print("Kịch bản 3 (d_E, AN):", list(results_de_an.keys()))

# Danh sách các chỉ số để so sánh
metrics = ['R_s1', 'R_s2', 'R_s_sum', 'SOP1', 'SOP2', 'IP1', 'IP2', 'BER_B1', 'BER_B2', 'BER_E', 'eta_s1', 'eta_s2']

# Kịch bản 2: So sánh tại SNR_Bob = 20 dB
SNR_Bob_dB_range = results_snr['SNR_Bob_dB']
SNR_Eve_dB_range = results_snr['SNR_Eve_dB']
phi_values = [ 0.3]
#results_snr_an['phi']
bob_idx_plot = np.where(SNR_Bob_dB_range == 20)[0][0]

# So sánh số học cho Kịch bản 2
print("\n=== So sánh số học Kịch bản 2 (SNR_Bob = 20 dB) ===")
table_snr = []
for metric in metrics:
    row = [metric]
    for phi_idx, phi in enumerate(phi_values):
        diff = relative_difference(
            results_snr_an[metric][bob_idx_plot, :, phi_idx],
            results_snr[metric][bob_idx_plot]
        )
        max_diff = np.max(diff)
        mean_diff = np.mean(diff)
        row.extend([f"{max_diff:.4e}", f"{mean_diff:.4e}"])
    table_snr.append(row)
print(tabulate(table_snr, headers=['Metric', 'Max Diff (phi=0.0)', 'Mean Diff (phi=0.0)', 
                                  'Max Diff (phi=0.1)', 'Mean Diff (phi=0.1)', 
                                  'Max Diff (phi=0.2)', 'Mean Diff (phi=0.2)', 
                                  'Max Diff (phi=0.3)', 'Mean Diff (phi=0.3)'], tablefmt='grid'))

# Vẽ biểu đồ so sánh Kịch bản 2
plt.figure(figsize=(8, 6))
plt.plot(SNR_Eve_dB_range, results_snr['R_s1'][bob_idx_plot], 'k-', label='R_s1 (No AN)', linewidth=2)
plt.plot(SNR_Eve_dB_range, results_snr['R_s2'][bob_idx_plot], 'k--', label='R_s2 (No AN)', linewidth=2)
plt.plot(SNR_Eve_dB_range, results_snr['R_s_sum'][bob_idx_plot], 'k:', label='R_s_sum (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.plot(SNR_Eve_dB_range, results_snr_an['R_s1'][bob_idx_plot, :, phi_idx], label=f'R_s1, phi={phi}', linestyle='-', marker='o')
    plt.plot(SNR_Eve_dB_range, results_snr_an['R_s2'][bob_idx_plot, :, phi_idx], label=f'R_s2, phi={phi}', linestyle='--', marker='s')
    plt.plot(SNR_Eve_dB_range, results_snr_an['R_s_sum'][bob_idx_plot, :, phi_idx], label=f'R_s_sum, phi={phi}', linestyle=':', marker='^')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Comparison: Secrecy Rate vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.savefig('compare_scenario_2_rs1_rs2.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.plot(SNR_Eve_dB_range, results_snr['SOP1'][bob_idx_plot], 'k-', label='SOP1 (No AN)', linewidth=2)
plt.plot(SNR_Eve_dB_range, results_snr['SOP2'][bob_idx_plot], 'k--', label='SOP2 (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.plot(SNR_Eve_dB_range, results_snr_an['SOP1'][bob_idx_plot, :, phi_idx], label=f'SOP1, phi={phi}', linestyle='-', marker='o')
    plt.plot(SNR_Eve_dB_range, results_snr_an['SOP2'][bob_idx_plot, :, phi_idx], label=f'SOP2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Outage Probability')
plt.title('Comparison: Secrecy Outage Probability vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.savefig('compare_scenario_2_sop1_sop2.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.plot(SNR_Eve_dB_range, results_snr['IP1'][bob_idx_plot], 'k-', label='IP1 (No AN)', linewidth=2)
plt.plot(SNR_Eve_dB_range, results_snr['IP2'][bob_idx_plot], 'k--', label='IP2 (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.plot(SNR_Eve_dB_range, results_snr_an['IP1'][bob_idx_plot, :, phi_idx], label=f'IP1, phi={phi}', linestyle='-', marker='o')
    plt.plot(SNR_Eve_dB_range, results_snr_an['IP2'][bob_idx_plot, :, phi_idx], label=f'IP2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Intercept Probability')
plt.title('Comparison: Intercept Probability vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.savefig('compare_scenario_2_ip1_ip2.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.semilogy(SNR_Eve_dB_range, results_snr['BER_B1'][bob_idx_plot], 'k-', label='BER_B1 (No AN)', linewidth=2)
plt.semilogy(SNR_Eve_dB_range, results_snr['BER_B2'][bob_idx_plot], 'k--', label='BER_B2 (No AN)', linewidth=2)
plt.semilogy(SNR_Eve_dB_range, results_snr['BER_E'][bob_idx_plot], 'k:', label='BER_E (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.semilogy(SNR_Eve_dB_range, results_snr_an['BER_B1'][bob_idx_plot, :, phi_idx], label=f'BER_B1, phi={phi}', linestyle='-', marker='o')
    plt.semilogy(SNR_Eve_dB_range, results_snr_an['BER_B2'][bob_idx_plot, :, phi_idx], label=f'BER_B2, phi={phi}', linestyle='--', marker='s')
    plt.semilogy(SNR_Eve_dB_range, results_snr_an['BER_E'][bob_idx_plot, :, phi_idx], label=f'BER_E, phi={phi}', linestyle=':', marker='^')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('BER (BPSK, Rayleigh)')
plt.title('Comparison: BER vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True, which='both')
plt.savefig('compare_scenario_2_ber_b1_b2_e.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.plot(SNR_Eve_dB_range, results_snr['eta_s1'][bob_idx_plot], 'k-', label='eta_s1 (No AN)', linewidth=2)
plt.plot(SNR_Eve_dB_range, results_snr['eta_s2'][bob_idx_plot], 'k--', label='eta_s2 (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.plot(SNR_Eve_dB_range, results_snr_an['eta_s1'][bob_idx_plot, :, phi_idx], label=f'eta_s1, phi={phi}', linestyle='-', marker='o')
    plt.plot(SNR_Eve_dB_range, results_snr_an['eta_s2'][bob_idx_plot, :, phi_idx], label=f'eta_s2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('SNR_Eve (dB)')
plt.ylabel('Secrecy Spectral Efficiency (bits/s/Hz)')
plt.title('Comparison: Secrecy Spectral Efficiency vs SNR_Eve (SNR_Bob = 20 dB)')
plt.legend()
plt.grid(True)
plt.savefig('compare_scenario_2_eta_s1_s2.png')
plt.show()
plt.close()

# Kịch bản 3: So sánh quét d_E
d_E_range = results_de['d_E']

# So sánh số học cho Kịch bản 3
print("\n=== So sánh số học Kịch bản 3 (SNR_Bob = 20 dB, SNR_Eve = 30 dB) ===")
table_de = []
for metric in metrics:
    row = [metric]
    for phi_idx, phi in enumerate(phi_values):
        diff = relative_difference(
            results_de_an[metric][:, phi_idx],
            results_de[metric]
        )
        max_diff = np.max(diff)
        mean_diff = np.mean(diff)
        row.extend([f"{max_diff:.4e}", f"{mean_diff:.4e}"])
    table_de.append(row)
print(tabulate(table_de, headers=['Metric', 'Max Diff (phi=0.0)', 'Mean Diff (phi=0.0)', 
                                 'Max Diff (phi=0.1)', 'Mean Diff (phi=0.1)', 
                                 'Max Diff (phi=0.2)', 'Mean Diff (phi=0.2)', 
                                 'Max Diff (phi=0.3)', 'Mean Diff (phi=0.3)'], tablefmt='grid'))

# Vẽ biểu đồ so sánh Kịch bản 3
plt.figure(figsize=(8, 6))
plt.plot(d_E_range, results_de['R_s1'], 'k-', label='R_s1 (No AN)', linewidth=2)
plt.plot(d_E_range, results_de['R_s2'], 'k--', label='R_s2 (No AN)', linewidth=2)
plt.plot(d_E_range, results_de['R_s_sum'], 'k:', label='R_s_sum (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.plot(d_E_range, results_de_an['R_s1'][:, phi_idx], label=f'R_s1, phi={phi}', linestyle='-', marker='o')
    plt.plot(d_E_range, results_de_an['R_s2'][:, phi_idx], label=f'R_s2, phi={phi}', linestyle='--', marker='s')
    plt.plot(d_E_range, results_de_an['R_s_sum'][:, phi_idx], label=f'R_s_sum, phi={phi}', linestyle=':', marker='^')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Secrecy Rate (bits/s/Hz)')
plt.title('Comparison: Secrecy Rate vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True)
plt.savefig('compare_scenario_3_rs1_rs2.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.plot(d_E_range, results_de['SOP1'], 'k-', label='SOP1 (No AN)', linewidth=2)
plt.plot(d_E_range, results_de['SOP2'], 'k--', label='SOP2 (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.plot(d_E_range, results_de_an['SOP1'][:, phi_idx], label=f'SOP1, phi={phi}', linestyle='-', marker='o')
    plt.plot(d_E_range, results_de_an['SOP2'][:, phi_idx], label=f'SOP2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Secrecy Outage Probability')
plt.title('Comparison: Secrecy Outage Probability vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True)
plt.savefig('compare_scenario_3_sop1_sop2.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.plot(d_E_range, results_de['IP1'], 'k-', label='IP1 (No AN)', linewidth=2)
plt.plot(d_E_range, results_de['IP2'], 'k--', label='IP2 (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.plot(d_E_range, results_de_an['IP1'][:, phi_idx], label=f'IP1, phi={phi}', linestyle='-', marker='o')
    plt.plot(d_E_range, results_de_an['IP2'][:, phi_idx], label=f'IP2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Intercept Probability')
plt.title('Comparison: Intercept Probability vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True)
plt.savefig('compare_scenario_3_ip1_ip2.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.semilogy(d_E_range, results_de['BER_B1'], 'k-', label='BER_B1 (No AN)', linewidth=2)
plt.semilogy(d_E_range, results_de['BER_B2'], 'k--', label='BER_B2 (No AN)', linewidth=2)
plt.semilogy(d_E_range, results_de['BER_E'], 'k:', label='BER_E (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.semilogy(d_E_range, results_de_an['BER_B1'][:, phi_idx], label=f'BER_B1, phi={phi}', linestyle='-', marker='o')
    plt.semilogy(d_E_range, results_de_an['BER_B2'][:, phi_idx], label=f'BER_B2, phi={phi}', linestyle='--', marker='s')
    plt.semilogy(d_E_range, results_de_an['BER_E'][:, phi_idx], label=f'BER_E, phi={phi}', linestyle=':', marker='^')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('BER (BPSK, Rayleigh)')
plt.title('Comparison: BER vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True, which='both')
plt.savefig('compare_scenario_3_ber_b1_b2_e.png')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.plot(d_E_range, results_de['eta_s1'], 'k-', label='eta_s1 (No AN)', linewidth=2)
plt.plot(d_E_range, results_de['eta_s2'], 'k--', label='eta_s2 (No AN)', linewidth=2)
for phi_idx, phi in enumerate(phi_values):
    plt.plot(d_E_range, results_de_an['eta_s1'][:, phi_idx], label=f'eta_s1, phi={phi}', linestyle='-', marker='o')
    plt.plot(d_E_range, results_de_an['eta_s2'][:, phi_idx], label=f'eta_s2, phi={phi}', linestyle='--', marker='s')
plt.xlabel('Khoảng cách d_E (m)')
plt.ylabel('Secrecy Spectral Efficiency (bits/s/Hz)')
plt.title('Comparison: Secrecy Spectral Efficiency vs d_E (SNR_Bob = 20 dB, SNR_Eve = 30 dB)')
plt.legend()
plt.grid(True)
plt.savefig('compare_scenario_3_eta_s1_s2.png')
plt.show()
plt.close()