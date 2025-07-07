## Added AN for NOMAImprovementTwoUserFinal.py AN & DPA
# ORIGINAL
import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from tabulate import tabulate
import cvxpy as cp
from scipy.optimize import minimize

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

def adaptive_alpha2_for_bob2(d_E, SNR_Eve_dB, h_B2_mean, h_E_mean, P_A, N_0, phi):
    """
    Tối ưu hóa α₂ để cải thiện Bob2 khi Eve ở xa
    """
    # Tính SINR Bob2 với α₂ hiện tại
    alpha2_current = 0.5
    SINR_B2_current = (P_A * alpha2_current * h_B2_mean) / (N_0 + phi * P_A * h_B2_mean)
    
    # Tính SINR Eve với α₂ hiện tại  
    SINR_E2_current = (P_A * alpha2_current * h_E_mean) / (N_0 + phi * P_A * h_E_mean)
    
    # Tốc độ bí mật hiện tại
    R_s2_current = max(np.log2(1 + SINR_B2_current) - np.log2(1 + SINR_E2_current), 0)
    
    # Thử tăng α₂ từng bước
    alpha2_candidates = np.linspace(0.1, 0.8, 20)
    best_alpha2 = alpha2_current
    best_R_s2 = R_s2_current
    
    for alpha2_test in alpha2_candidates:
        SINR_B2_test = (P_A * alpha2_test * h_B2_mean) / (N_0 + phi * P_A * h_B2_mean)
        SINR_E2_test = (P_A * alpha2_test * h_E_mean) / (N_0 + phi * P_A * h_E_mean)
        R_s2_test = max(np.log2(1 + SINR_B2_test) - np.log2(1 + SINR_E2_test), 0)
        
        if R_s2_test > best_R_s2:
            best_R_s2 = R_s2_test
            best_alpha2 = alpha2_test
    
    return best_alpha2

def adaptive_phi(d_E, d_B1, d_B2, SNR_Eve_dB):
    """
    Điều chỉnh φ dựa trên vị trí Eve
    φ cao khi Eve gần, φ thấp khi Eve xa
    """
    # Khoảng cách tương đối của Eve
    d_E_relative = min(d_E / min(d_B1, d_B2), 5.0)
    
    # φ cơ bản
    phi_base = 0.2
    
    # Điều chỉnh dựa trên khoảng cách
    if d_E_relative < 1.5:  # Eve rất gần
        phi_adaptive = phi_base * 2.0  # Tăng AN
    elif d_E_relative < 3.0:  # Eve ở khoảng cách trung bình
        phi_adaptive = phi_base * 1.5
    else:  # Eve ở xa
        phi_adaptive = phi_base * 0.5  # Giảm AN
    
    # Điều chỉnh dựa trên công suất Eve
    power_adjustment = max(0.5, SNR_Eve_dB / 20)
    phi_final = phi_adaptive * power_adjustment
    
    # Ràng buộc: 0.05 ≤ φ ≤ 0.4
    return np.clip(phi_final, 0.05, 0.4)

def adaptive_power_control(d_E, SNR_Eve_dB, P_A_max=0.1):
    """
    Điều chỉnh công suất truyền dựa trên vị trí Eve
    """
    # Khoảng cách tương đối
    d_E_relative = d_E / min(d_B1, d_B2)
    
    # Công suất cơ bản
    P_A_base = P_A_max
    
    # Điều chỉnh công suất
    if d_E_relative < 1.2:  # Eve rất gần
        power_reduction = 0.3  # Giảm 30%
    elif d_E_relative < 2.0:  # Eve gần
        power_reduction = 0.15  # Giảm 15%
    else:  # Eve xa
        power_reduction = 0.0  # Không giảm
    
    # Điều chỉnh thêm dựa trên công suất Eve
    if SNR_Eve_dB > 15:
        power_reduction += 0.1  # Giảm thêm 10%
    
    P_A_adaptive = P_A_base * (1 - power_reduction)
    
    return np.clip(P_A_adaptive, 0.01, P_A_max)

def comprehensive_dpa_optimization(d_E, SNR_Eve_dB, h_B1_mean, h_B2_mean, h_E_mean, P_A_max=0.1):
    """
    Tối ưu hóa tổng hợp: α₁, α₂, φ, P_A
    """
    # Bước 1: Điều chỉnh công suất
    P_A_adaptive = adaptive_power_control(d_E, SNR_Eve_dB, P_A_max)
    
    # Bước 2: Tối ưu hóa φ
    phi_opt = adaptive_phi(d_E, d_B1, d_B2, SNR_Eve_dB)
    
    # Bước 3: Tối ưu hóa α₂ cho Bob2
    alpha2_opt = adaptive_alpha2_for_bob2(d_E, SNR_Eve_dB, h_B2_mean, h_E_mean, P_A_adaptive, N_0, phi_opt)
    
    # Bước 4: Tính α₁ từ ràng buộc
    alpha1_opt = 1.0 - alpha2_opt - phi_opt
    
    # Đảm bảo ràng buộc
    if alpha1_opt < 0.1:
        alpha1_opt = 0.1
        alpha2_opt = 0.9 - phi_opt
    
    return alpha1_opt, alpha2_opt, phi_opt, P_A_adaptive

def objective_function(x, P_A, N_0, B, h_B1_mean, h_B2_mean, h_E_mean, epsilon):
    """
    Hàm mục tiêu để tối ưu hóa: maximize min(R_s1, R_s2)
    x = [alpha1, alpha2, phi]
    """
    alpha1, alpha2, phi = x
    
    # Ràng buộc: alpha1 + alpha2 + phi = 1
    if abs(alpha1 + alpha2 + phi - 1.0) > 1e-6:
        return -1e6  # Penalty cho vi phạm ràng buộc
    
    # Ràng buộc: alpha1, alpha2, phi >= 0
    if alpha1 < 0 or alpha2 < 0 or phi < 0:
        return -1e6
    
    # Tính SINR
    SINR_B1 = (P_A * alpha1 * h_B1_mean) / (P_A * alpha2 * h_B1_mean * epsilon + N_0 + phi * P_A * h_B1_mean)
    SINR_B2 = (P_A * alpha2 * h_B2_mean) / (N_0 + phi * P_A * h_B2_mean)
    SINR_E1 = (P_A * alpha1 * h_E_mean) / (N_0 + phi * P_A * h_E_mean)
    SINR_E2 = (P_A * alpha2 * h_E_mean) / (N_0 + phi * P_A * h_E_mean)
    
    # Tính dung lượng kênh
    C_B1 = B * np.log2(1 + SINR_B1)
    C_B2 = B * np.log2(1 + SINR_B2)
    C_E1 = B * np.log2(1 + SINR_E1)
    C_E2 = B * np.log2(1 + SINR_E2)
    
    # Tính tốc độ bí mật
    R_s1 = max(C_B1 - C_E1, 0)
    R_s2 = max(C_B2 - C_E2, 0)
    
    # Hàm mục tiêu: maximize min(R_s1, R_s2)
    return min(R_s1, R_s2)

def optimize_dpa(P_A, N_0, B, h_B1_mean, h_B2_mean, h_E_mean, epsilon):
    """
    Tối ưu hóa DPA sử dụng scipy.optimize thay vì cvxpy
    """
    try:
        # Khởi tạo giá trị ban đầu
        x0 = [0.3, 0.5, 0.2]  # alpha1, alpha2, phi
        
        # Ràng buộc: alpha1 + alpha2 + phi = 1
        constraints = ({'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] - 1.0})
        
        # Giới hạn: alpha1, alpha2, phi >= 0
        bounds = [(0.01, 0.98), (0.01, 0.98), (0.01, 0.98)]
        
        # Tối ưu hóa
        result = minimize(
            lambda x: -objective_function(x, P_A, N_0, B, h_B1_mean, h_B2_mean, h_E_mean, epsilon),
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )
        
        if result.success:
            alpha1, alpha2, phi = result.x
            return alpha1, alpha2, phi
        else:
            # Fallback nếu tối ưu hóa thất bại
            return 0.3, 0.5, 0.2
            
    except Exception as e:
        print(f"Lỗi tối ưu hóa DPA: {e}")
        # Fallback nếu có lỗi
        return 0.3, 0.5, 0.2

# KỊCH BẢN 2: Multi-user NOMA, quét SNR_Eve (Eve chủ động gây nhiễu)
print("\n===== KỊCH BẢN 2: Multi-user NOMA, quét SNR_Eve (Eve chủ động gây nhiễu) =====")
# Thông số hệ thống
P_A = 1 # Công suất truyền tổng (W) ~ 20 dBm - THAY ĐỔI TỪ 1W XUỐNG 0.1W
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
pilot_contamination_power = 0.2  # Công suất nhiễu pilot - loại bỏ Nhiễu Định vị của EVE
phi_values = [0.3]  # Tỷ lệ công suất AN

# Phân bổ công suất
# alpha1 = 0.3
# alpha2 = 1 - alpha1

print("==== THÔNG SỐ HỆ THỐNG KỊCH BẢN 2 ====")
print(f"Công suất truyền P_A: {P_A} W (100 mW - 20 dBm)")
print(f"Nhiễu nền N_0: {N_0:.2e} W")
print(f"Hệ số suy hao alpha: {alpha}")
print(f"Băng thông: {B/1e6:.1f} MHz")
print(f"Số anten: {N_ant}")
print(f"Khoảng cách: Bob1 = {d_B1}m, Bob2 = {d_B2}m, Eve = {d_E}m")
#print(f"Phân bổ công suất: alpha1 = {alpha1:.3f}, alpha2 = {alpha2:.3f} (tổng = {alpha1+alpha2:.3f})") được phân bổ động
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
            d_EB2 = float(max(float(abs(d_E - d_B2)), 1.0))

            # Lấy CSI trung bình để tối ưu hóa DPA
            norm_h_B1 = np.sum(np.abs(h_B1)**2, axis=1)
            norm_h_B2 = np.sum(np.abs(h_B2)**2, axis=1)
            norm_h_E = np.sum(np.abs(h_E)**2, axis=1)
            
            # SỬ DỤNG COMPREHENSIVE DPA OPTIMIZATION THAY VÌ OPTIMIZE_DPA CŨ
            alpha1, alpha2, phi_opt, P_A_adaptive = comprehensive_dpa_optimization(d_E, SNR_Eve_dB, norm_h_B1.mean(), norm_h_B2.mean(), norm_h_E.mean(), float(P_A_eff))
            
            # Fallback nếu tối ưu hóa trả về None
            if alpha1 is None or alpha2 is None:
                alpha1 = 0.3
                alpha2 = 0.7
            if phi_opt is not None:
                phi = phi_opt
            else:
                phi = phi_values[phi_idx]
            if phi is None:
                phi = 0.3
            # Đảm bảo alpha1, alpha2 là float
            alpha1 = float(alpha1)
            alpha2 = float(alpha2)
            phi = float(phi)
            
            # Sử dụng P_A_adaptive thay vì P_A_eff
            P_A_final = P_A_adaptive if P_A_adaptive is not None else P_A_eff
            
            # Tính SNR với AN
            SNR_B1, SNR_B2, SNR_E1, SNR_E2 = compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A_final, alpha1, alpha2, phi, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant)

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
            P_s = P_A_final * (1 - phi)
            norm_h_E = np.sum(np.abs(h_E)**2, axis=1)  # Tính norm_h_E cho nhiễu AN
            rx_signal_B1 = np.sqrt(P_s * alpha1) * np.sum(h_B1, axis=1) * tx_signal + np.sqrt(epsilon * P_s * alpha2) * np.sum(h_B1, axis=1) * tx_signal + np.sqrt(P_E / d_EB1**alpha) * np.sum(h_EB1, axis=1) * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
            rx_signal_B2 = np.sqrt(P_s * alpha2) * np.sum(h_B2, axis=1) * tx_signal + np.sqrt(P_E / d_EB2**alpha) * np.sum(h_EB2, axis=1) * tx_signal + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
            rx_signal_E = np.sqrt(P_s * alpha1) * np.sum(h_E, axis=1) * tx_signal + np.sqrt(P_s * alpha2) * np.sum(h_E, axis=1) * tx_signal + np.sqrt(P_A_final * phi * norm_h_E / d_E**alpha) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples)) + np.sqrt(N_0) * (np.random.randn(num_samples) + 1j * np.random.randn(num_samples))
            rx_bits_B1 = (rx_signal_B1.real > 0).astype(int)
            rx_bits_B2 = (rx_signal_B2.real > 0).astype(int)
            rx_bits_E = (rx_signal_E.real > 0).astype(int)
            BER_B1_2[bob_idx, eve_idx, phi_idx] = np.mean(bits != rx_bits_B1)
            BER_B2_2[bob_idx, eve_idx, phi_idx] = np.mean(bits != rx_bits_B2)
            BER_E_2[bob_idx, eve_idx, phi_idx] = np.mean(bits != rx_bits_E)

            print(f"SNR_Bob = {SNR_Bob_dB} dB, SNR_Eve = {SNR_Eve_dB} dB, phi = {phi:.3f}, P_A = {P_A_final:.3f}W | C_B1 = {C_B1_2[bob_idx, eve_idx, phi_idx]/1e6:.2f} Mbps | C_B2 = {C_B2_2[bob_idx, eve_idx, phi_idx]/1e6:.2f} Mbps | C_E = {C_E_2[bob_idx, eve_idx, phi_idx]/1e6:.2f} Mbps | BER_B1 = {BER_B1_2[bob_idx, eve_idx, phi_idx]:.4e} | BER_B2 = {BER_B2_2[bob_idx, eve_idx, phi_idx]:.4e} | BER_E = {BER_E_2[bob_idx, eve_idx, phi_idx]:.4e} | R_s1 = {R_s1_2[bob_idx, eve_idx, phi_idx]:.2f} | R_s2 = {R_s2_2[bob_idx, eve_idx, phi_idx]:.2f} | SOP1 = {SOP1_2[bob_idx, eve_idx, phi_idx]:.2f} | SOP2 = {SOP2_2[bob_idx, eve_idx, phi_idx]:.2f} | IP1 = {IP1_2[bob_idx, eve_idx, phi_idx]:.2f} | IP2 = {IP2_2[bob_idx, eve_idx, phi_idx]:.2f} | eta_s1 = {eta_s1_2[bob_idx, eve_idx, phi_idx]:.2e} | eta_s2 = {eta_s2_2[bob_idx, eve_idx, phi_idx]:.2e}")

# Lưu kết quả Kịch bản 2
np.savez('simulation_results_snr_an_dpa.npz',
    SNR_Bob_dB=SNR_Bob_dB_range,
    SNR_Eve_dB=SNR_Eve_dB_range,
    phi=np.array(phi_values),
    R_s1=R_s1_2, R_s2=R_s2_2, R_s_sum=R_s_sum_2,
    SOP1=SOP1_2, SOP2=SOP2_2,
    IP1=IP1_2, IP2=IP2_2,
    Erg_Rs1=Erg_Rs1_2, Erg_Rs2=Erg_Rs2_2,
    Cs1=Cs1_2, Cs2=Cs2_2,
    C_B1=C_B1_2, C_B2=C_B2_2, C_E=C_E_2,
    BER_B1=BER_B1_2, BER_B2=BER_B2_2, BER_E=BER_E_2,
    eta_s1=eta_s1_2, eta_s2=eta_s2_2
)

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
plt.savefig('scenario_2_rs1_rs2_an_dpa.png')
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
plt.savefig('scenario_2_sop1_sop2_an_dpa.png')
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
plt.savefig('scenario_2_ip1_ip2_an_dpa.png')
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
plt.savefig('scenario_2_ber_b1_b2_e_an_dpa.png')
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
plt.savefig('scenario_2_eta_s1_s2_an_dpa.png')
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
##print(f"Phân bổ công suất: alpha1 = {alpha1:.3f}, alpha2 = {alpha2:.3f} (tổng = {alpha1+alpha2:.3f})") sẽ được phân bổ động
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
        d_EB2 = float(max(float(abs(d_E - d_B2)), 1.0))

        # Lấy CSI trung bình để tối ưu hóa DPA
        norm_h_B1 = np.sum(np.abs(h_B1)**2, axis=1)
        norm_h_B2 = np.sum(np.abs(h_B2)**2, axis=1)
        norm_h_E = np.sum(np.abs(h_E)**2, axis=1)
        alpha1, alpha2, phi_opt = optimize_dpa(P_A_eff, N_0, B, norm_h_B1.mean(), norm_h_B2.mean(), norm_h_E.mean(), epsilon)
        if alpha1 is None or alpha2 is None:
            alpha1 = 0.3
            alpha2 = 0.7
        if phi_opt is not None:
            phi = phi_opt
        else:
            phi = phi_values[phi_idx]
        if phi is None:
            phi = 0.3
        alpha1 = float(alpha1)
        alpha2 = float(alpha2)
        phi = float(phi)
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
np.savez('simulation_results_de_an_dpa.npz',
    d_E=d_E_range,
    phi=np.array(phi_values),
    R_s1=R_s1_3, R_s2=R_s2_3, R_s_sum=R_s_sum_3,
    SOP1=SOP1_3, SOP2=SOP2_3,
    IP1=IP1_3, IP2=IP2_3,
    Erg_Rs1=Erg_Rs1_3, Erg_Rs2=Erg_Rs2_3,
    Cs1=Cs1_3, Cs2=Cs2_3,
    C_B1=C_B1_3, C_B2=C_B2_3, C_E=C_E_3,
    BER_B1=BER_B1_3, BER_B2=BER_B2_3, BER_E=BER_E_3,
    eta_s1=eta_s1_3, eta_s2=eta_s2_3
)

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
plt.savefig('scenario_3_rs1_rs2_an_dpa.png')
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
plt.savefig('scenario_3_sop1_sop2_an_dpa.png')
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
plt.savefig('scenario_3_ip1_ip2_an_dpa.png')
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
plt.savefig('scenario_3_ber_b1_b2_e_an_dpa.png')
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
plt.savefig('scenario_3_eta_s1_s2_an_dpa.png')
plt.show()
plt.close()