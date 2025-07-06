#!/usr/bin/env python3
"""
Script so sánh nhanh hiệu quả các phương pháp bảo mật NOMA
- Giảm số mẫu để chạy nhanh hơn
- So sánh Baseline, AN, và DPA
"""

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time
import os
from datetime import datetime

def create_quick_baseline():
    """Tạo phiên bản nhanh của baseline"""
    code = '''import numpy as np
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
P_A = 1  # 100mW
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
'''
    
    with open('quick_baseline.py', 'w') as f:
        f.write(code)

def create_quick_an():
    """Tạo phiên bản nhanh với AN"""
    code = '''import numpy as np
import matplotlib.pyplot as plt
from numba import jit

@jit(nopython=True)
def compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A, alpha1, alpha2, phi, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant):
    norm_h_B1 = np.sum(np.abs(h_B1)**2, axis=1)
    norm_h_B2 = np.sum(np.abs(h_B2)**2, axis=1)
    norm_h_E = np.sum(np.abs(h_E)**2, axis=1)
    norm_h_EB1 = np.sum(np.abs(h_EB1)**2, axis=1)
    norm_h_EB2 = np.sum(np.abs(h_EB2)**2, axis=1)

    P_s = P_A * (1 - phi)

    SNR_B2 = (P_s * alpha2 * norm_h_B2) / (d_B2**alpha * N_0 + P_E * norm_h_EB2 / d_EB2**alpha)
    SNR_B1 = (P_s * alpha1 * norm_h_B1) / (d_B1**alpha * N_0 + epsilon * P_s * alpha2 * norm_h_B1 + P_E * norm_h_EB1 / d_EB1**alpha)
    SNR_E1 = (P_s * alpha1 * norm_h_E) / (d_E**alpha * N_0 + P_A * phi * norm_h_E / d_E**alpha)
    SNR_E2 = (P_s * alpha2 * norm_h_E) / (d_E**alpha * N_0 + P_A * phi * norm_h_E / d_E**alpha)
    return SNR_B1, SNR_B2, SNR_E1, SNR_E2

# Thông số hệ thống
P_A = 1
N_0 = 1e-15
alpha = 3
B = 10e6
num_samples = int(1e3)
N_ant = 16
d_B1, d_B2, d_E = 30, 70, 50
epsilon = 0.01
alpha1, alpha2 = 0.3, 0.7
phi = 0.2

# Quét SNR
SNR_Bob_dB_range = np.arange(10, 21, 5)
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

        SNR_B1, SNR_B2, SNR_E1, SNR_E2 = compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A_eff, alpha1, alpha2, phi, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant)

        R1 = np.log2(1 + SNR_B1)
        R2 = np.log2(1 + SNR_B2)
        Re1 = np.log2(1 + SNR_E1)
        Re2 = np.log2(1 + SNR_E2)

        Rs1 = np.maximum(0, R1 - Re1)
        Rs2 = np.maximum(0, R2 - Re2)
        R_s1[bob_idx, eve_idx] = np.mean(Rs1)
        R_s2[bob_idx, eve_idx] = np.mean(Rs2)
        R_s_sum[bob_idx, eve_idx] = R_s1[bob_idx, eve_idx] + R_s2[bob_idx, eve_idx]

np.save('quick_an.npy', {
    'R_s1': R_s1, 'R_s2': R_s2, 'R_s_sum': R_s_sum,
    'SNR_Bob_dB': SNR_Bob_dB_range, 'SNR_Eve_dB': SNR_Eve_dB_range
})
print("AN completed")
'''
    
    with open('quick_an.py', 'w') as f:
        f.write(code)

def create_quick_dpa():
    """Tạo phiên bản nhanh với DPA"""
    code = '''import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from scipy.optimize import minimize

@jit(nopython=True)
def compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A, alpha1, alpha2, phi, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant):
    norm_h_B1 = np.sum(np.abs(h_B1)**2, axis=1)
    norm_h_B2 = np.sum(np.abs(h_B2)**2, axis=1)
    norm_h_E = np.sum(np.abs(h_E)**2, axis=1)
    norm_h_EB1 = np.sum(np.abs(h_EB1)**2, axis=1)
    norm_h_EB2 = np.sum(np.abs(h_EB2)**2, axis=1)

    P_s = P_A * (1 - phi)

    SNR_B2 = (P_s * alpha2 * norm_h_B2) / (d_B2**alpha * N_0 + P_E * norm_h_EB2 / d_EB2**alpha)
    SNR_B1 = (P_s * alpha1 * norm_h_B1) / (d_B1**alpha * N_0 + epsilon * P_s * alpha2 * norm_h_B1 + P_E * norm_h_EB1 / d_EB1**alpha)
    SNR_E1 = (P_s * alpha1 * norm_h_E) / (d_E**alpha * N_0 + P_A * phi * norm_h_E / d_E**alpha)
    SNR_E2 = (P_s * alpha2 * norm_h_E) / (d_E**alpha * N_0 + P_A * phi * norm_h_E / d_E**alpha)
    return SNR_B1, SNR_B2, SNR_E1, SNR_E2

def adaptive_dpa(d_E, SNR_Eve_dB, h_B1_mean, h_B2_mean, h_E_mean, P_A_max=0.1):
    """DPA đơn giản"""
    d_E_relative = d_E / min(30, 70)
    
    if d_E_relative < 1.5:
        phi = 0.3
        alpha1, alpha2 = 0.4, 0.3
    elif d_E_relative < 3.0:
        phi = 0.2
        alpha1, alpha2 = 0.5, 0.3
    else:
        phi = 0.1
        alpha1, alpha2 = 0.6, 0.3
    
    return alpha1, alpha2, phi

# Thông số hệ thống
P_A = 1
N_0 = 1e-15
alpha = 3
B = 10e6
num_samples = int(1e3)
N_ant = 16
d_B1, d_B2, d_E = 30, 70, 50
epsilon = 0.01

# Quét SNR
SNR_Bob_dB_range = np.arange(10, 21, 5)
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

        # DPA
        h_B1_mean = np.mean(np.sum(np.abs(h_B1)**2, axis=1))
        h_B2_mean = np.mean(np.sum(np.abs(h_B2)**2, axis=1))
        h_E_mean = np.mean(np.sum(np.abs(h_E)**2, axis=1))
        
        alpha1, alpha2, phi = adaptive_dpa(d_E, SNR_Eve_dB, h_B1_mean, h_B2_mean, h_E_mean, P_A_eff)

        SNR_B1, SNR_B2, SNR_E1, SNR_E2 = compute_snr(h_B1, h_B2, h_E, h_EB1, h_EB2, P_A_eff, alpha1, alpha2, phi, N_0, P_E, d_B1, d_B2, d_E, d_EB1, d_EB2, epsilon, N_ant)

        R1 = np.log2(1 + SNR_B1)
        R2 = np.log2(1 + SNR_B2)
        Re1 = np.log2(1 + SNR_E1)
        Re2 = np.log2(1 + SNR_E2)

        Rs1 = np.maximum(0, R1 - Re1)
        Rs2 = np.maximum(0, R2 - Re2)
        R_s1[bob_idx, eve_idx] = np.mean(Rs1)
        R_s2[bob_idx, eve_idx] = np.mean(Rs2)
        R_s_sum[bob_idx, eve_idx] = R_s1[bob_idx, eve_idx] + R_s2[bob_idx, eve_idx]

np.save('quick_dpa.npy', {
    'R_s1': R_s1, 'R_s2': R_s2, 'R_s_sum': R_s_sum,
    'SNR_Bob_dB': SNR_Bob_dB_range, 'SNR_Eve_dB': SNR_Eve_dB_range
})
print("DPA completed")
'''
    
    with open('quick_dpa.py', 'w') as f:
        f.write(code)

def run_quick_simulations():
    """Chạy các mô phỏng nhanh"""
    print("🚀 Tạo và chạy các mô phỏng nhanh...")
    
    # Tạo các script nhanh
    create_quick_baseline()
    create_quick_an()
    create_quick_dpa()
    
    # Chạy các script
    scripts = [
        ('quick_baseline.py', 'Baseline'),
        ('quick_an.py', 'AN'),
        ('quick_dpa.py', 'DPA')
    ]
    
    execution_times = {}
    
    for script_name, description in scripts:
        print(f"\n📊 Chạy {description}...")
        start_time = time.time()
        
        try:
            result = subprocess.run(['python3', script_name], 
                                  capture_output=True, text=True, timeout=60)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            if result.returncode == 0:
                print(f"✅ {description} hoàn thành trong {execution_time:.2f}s")
                execution_times[description] = execution_time
            else:
                print(f"❌ {description} lỗi: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"❌ {description} timeout")
        except Exception as e:
            print(f"❌ {description} lỗi: {e}")
    
    return execution_times

def analyze_quick_results():
    """Phân tích kết quả nhanh"""
    print("\n📈 Phân tích kết quả...")
    
    results = {}
    files = [
        ('quick_baseline.npy', 'Baseline'),
        ('quick_an.npy', 'AN'),
        ('quick_dpa.npy', 'DPA')
    ]
    
    for filename, description in files:
        if os.path.exists(filename):
            try:
                data = np.load(filename, allow_pickle=True).item()
                
                r_s1_avg = np.mean(data['R_s1'])
                r_s2_avg = np.mean(data['R_s2'])
                r_sum_avg = np.mean(data['R_s_sum'])
                
                results[description] = {
                    'R_s1_avg': r_s1_avg,
                    'R_s2_avg': r_s2_avg,
                    'R_sum_avg': r_sum_avg
                }
                
                print(f"\n📊 {description}:")
                print(f"   R_s1: {r_s1_avg:.4f} bits/s/Hz")
                print(f"   R_s2: {r_s2_avg:.4f} bits/s/Hz")
                print(f"   R_sum: {r_sum_avg:.4f} bits/s/Hz")
                
            except Exception as e:
                print(f"❌ Lỗi đọc {filename}: {e}")
        else:
            print(f"⚠️  {filename} không tồn tại")
    
    return results

def create_comparison_plot(results):
    """Tạo biểu đồ so sánh với tên file dễ phân biệt"""
    if not results:
        print("❌ Không có dữ liệu để vẽ")
        return
    
    methods = list(results.keys())
    r_s1_values = [results[m]['R_s1_avg'] for m in methods]
    r_s2_values = [results[m]['R_s2_avg'] for m in methods]
    r_sum_values = [results[m]['R_sum_avg'] for m in methods]
    
    # Tạo thư mục cho charts
    charts_dir = "comparison_charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    # Biểu đồ 1: So sánh R_s1 (Bob1)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(methods, r_s1_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
    ax.set_title('Secrecy Rate Bob1 (R_s1) - P_A=1W', fontsize=16, fontweight='bold')
    ax.set_ylabel('Bits/s/Hz', fontsize=14)
    ax.set_xlabel('Phương pháp', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Thêm giá trị trên bars
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/01_Rs1_Bob1_Comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # Biểu đồ 2: So sánh R_s2 (Bob2)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars2 = ax.bar(methods, r_s2_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
    ax.set_title('Secrecy Rate Bob2 (R_s2) - P_A=1W', fontsize=16, fontweight='bold')
    ax.set_ylabel('Bits/s/Hz', fontsize=14)
    ax.set_xlabel('Phương pháp', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Thêm giá trị trên bars
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/02_Rs2_Bob2_Comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # Biểu đồ 3: So sánh R_sum (Tổng)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars3 = ax.bar(methods, r_sum_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
    ax.set_title('Sum Secrecy Rate (R_sum) - P_A=1W', fontsize=16, fontweight='bold')
    ax.set_ylabel('Bits/s/Hz', fontsize=14)
    ax.set_xlabel('Phương pháp', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Thêm giá trị trên bars
    for bar in bars3:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/03_Rsum_Total_Comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # Biểu đồ 4: So sánh tổng hợp (3 metrics)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # R_s1
    bars1 = ax1.bar(methods, r_s1_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
    ax1.set_title('R_s1 (Bob1)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Bits/s/Hz', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # R_s2
    bars2 = ax2.bar(methods, r_s2_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
    ax2.set_title('R_s2 (Bob2)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Bits/s/Hz', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # R_sum
    bars3 = ax3.bar(methods, r_sum_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.7)
    ax3.set_title('R_sum (Total)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Bits/s/Hz', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # Thêm giá trị trên bars
    for bars, ax in [(bars1, ax1), (bars2, ax2), (bars3, ax3)]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.suptitle('NOMA Security Methods Comparison - P_A=1W', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/04_Combined_Comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    print(f"📊 Đã tạo 4 biểu đồ trong thư mục: {charts_dir}/")
    print(f"   - 01_Rs1_Bob1_Comparison.png")
    print(f"   - 02_Rs2_Bob2_Comparison.png")
    print(f"   - 03_Rsum_Total_Comparison.png")
    print(f"   - 04_Combined_Comparison.png")

def generate_quick_report(results, execution_times):
    """Tạo báo cáo nhanh"""
    print(f"\n{'='*50}")
    print("BÁO CÁO SO SÁNH NHANH")
    print(f"{'='*50}")
    
    if not results:
        print("❌ Không có kết quả để báo cáo")
        return
    
    # Tìm tốt nhất
    best_r_sum = max(results.items(), key=lambda x: x[1]['R_sum_avg'])
    
    print(f"\n🏆 PHƯƠNG PHÁP TỐT NHẤT:")
    print(f"   {best_r_sum[0]}: {best_r_sum[1]['R_sum_avg']:.4f} bits/s/Hz")
    
    print(f"\n📊 CHI TIẾT:")
    for method, data in results.items():
        print(f"   {method}:")
        print(f"     R_s1: {data['R_s1_avg']:.4f} bits/s/Hz")
        print(f"     R_s2: {data['R_s2_avg']:.4f} bits/s/Hz")
        print(f"     R_sum: {data['R_sum_avg']:.4f} bits/s/Hz")
    
    print(f"\n⏱️  THỜI GIAN THỰC THI:")
    for method, time_taken in execution_times.items():
        print(f"   {method}: {time_taken:.2f}s")
    
    # Tính cải thiện
    baseline = list(results.keys())[0]
    baseline_r_sum = results[baseline]['R_sum_avg']
    
    print(f"\n📈 CẢI THIỆN SO VỚI BASELINE:")
    for method, data in results.items():
        if method != baseline:
            improvement = ((data['R_sum_avg'] - baseline_r_sum) / baseline_r_sum) * 100
            print(f"   {method}: {improvement:+.2f}%")

def main():
    """Hàm chính"""
    print("🚀 SO SÁNH NHANH HIỆU QUẢ NOMA SECURITY")
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("P_A = 1W (100mW) - Small Cell Scenario")
    
    # Chạy mô phỏng
    execution_times = run_quick_simulations()
    
    # Phân tích kết quả
    results = analyze_quick_results()
    
    # Tạo biểu đồ
    if results:
        create_comparison_plot(results)
    
    # Tạo báo cáo
    if results and execution_times:
        generate_quick_report(results, execution_times)
    
    print(f"\n🎉 HOÀN THÀNH!")

if __name__ == "__main__":
    main() 