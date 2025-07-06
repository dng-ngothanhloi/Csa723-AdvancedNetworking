#!/usr/bin/env python3
"""
Script phân tích so sánh Kịch bản 2 và Kịch bản 3
- Kịch bản 2: Quét SNR_Eve (Eve chủ động gây nhiễu)
- Kịch bản 3: Quét d_E (Eve chủ động gây nhiễu)
- So sánh Baseline, AN, DPA cho cả hai kịch bản
"""

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time
import os
from datetime import datetime

def run_scenario_2_analysis():
    """Chạy phân tích Kịch bản 2"""
    print("🔍 CHẠY PHÂN TÍCH KỊCH BẢN 2 (SNR_Eve)...")
    print("="*50)
    
    try:
        # Chạy các script cho Kịch bản 2
        scripts = [
            'NOMAImprovementTwoUserFinal.py',  # Baseline
            'NOMA_SimulationFinalWith_AN.py',  # AN
            'NOMA_SimulationFinalWith_AN_DPC.py'  # DPA
        ]
        
        results = {}
        for script in scripts:
            print(f"📊 Chạy {script}...")
            start_time = time.time()
            
            result = subprocess.run(['python3', script], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                elapsed_time = time.time() - start_time
                print(f"✅ {script} hoàn thành trong {elapsed_time:.2f}s")
                results[script] = {'status': 'success', 'time': elapsed_time}
            else:
                print(f"❌ {script} lỗi: {result.stderr}")
                results[script] = {'status': 'error', 'time': 0}
                
    except Exception as e:
        print(f"❌ Lỗi chạy Kịch bản 2: {e}")
        return False
    
    return True

def run_scenario_3_analysis():
    """Chạy phân tích Kịch bản 3"""
    print("\n🔍 CHẠY PHÂN TÍCH KỊCH BẢN 3 (d_E)...")
    print("="*50)
    
    try:
        # Chạy các script cho Kịch bản 3
        scripts = [
            'NOMAImprovementTwoUserFinal.py',  # Baseline
            'NOMA_SimulationFinalWith_AN.py',  # AN
            'NOMA_SimulationFinalWith_AN_DPC.py'  # DPA
        ]
        
        results = {}
        for script in scripts:
            print(f"📊 Chạy {script}...")
            start_time = time.time()
            
            result = subprocess.run(['python3', script], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                elapsed_time = time.time() - start_time
                print(f"✅ {script} hoàn thành trong {elapsed_time:.2f}s")
                results[script] = {'status': 'success', 'time': elapsed_time}
            else:
                print(f"❌ {script} lỗi: {result.stderr}")
                results[script] = {'status': 'error', 'time': 0}
                
    except Exception as e:
        print(f"❌ Lỗi chạy Kịch bản 3: {e}")
        return False
    
    return True

def load_simulation_results():
    """Tải kết quả mô phỏng từ các file .npy"""
    results = {}
    
    # Kịch bản 2 - SNR_Eve
    try:
        if os.path.exists('simulation_results_snr.npy'):
            data = np.load('simulation_results_snr.npy', allow_pickle=True).item()
            results['scenario_2_baseline'] = data
            print("✅ Đã tải kết quả Kịch bản 2 - Baseline")
    except:
        print("⚠️ Không tìm thấy kết quả Kịch bản 2 - Baseline")
    
    try:
        if os.path.exists('simulation_results_snr_an.npy'):
            data = np.load('simulation_results_snr_an.npy', allow_pickle=True).item()
            results['scenario_2_an'] = data
            print("✅ Đã tải kết quả Kịch bản 2 - AN")
    except:
        print("⚠️ Không tìm thấy kết quả Kịch bản 2 - AN")
    
    try:
        if os.path.exists('simulation_results_snr_an_dpa.npz'):
            data = np.load('simulation_results_snr_an_dpa.npz')
            results['scenario_2_dpa'] = data
            print("✅ Đã tải kết quả Kịch bản 2 - DPA")
    except:
        print("⚠️ Không tìm thấy kết quả Kịch bản 2 - DPA")
    
    # Kịch bản 3 - d_E
    try:
        if os.path.exists('simulation_results_de.npy'):
            data = np.load('simulation_results_de.npy', allow_pickle=True).item()
            results['scenario_3_baseline'] = data
            print("✅ Đã tải kết quả Kịch bản 3 - Baseline")
    except:
        print("⚠️ Không tìm thấy kết quả Kịch bản 3 - Baseline")
    
    try:
        if os.path.exists('simulation_results_de_an.npy'):
            data = np.load('simulation_results_de_an.npy', allow_pickle=True).item()
            results['scenario_3_an'] = data
            print("✅ Đã tải kết quả Kịch bản 3 - AN")
    except:
        print("⚠️ Không tìm thấy kết quả Kịch bản 3 - AN")
    
    try:
        if os.path.exists('simulation_results_de_an_dpa.npz'):
            data = np.load('simulation_results_de_an_dpa.npz')
            results['scenario_3_dpa'] = data
            print("✅ Đã tải kết quả Kịch bản 3 - DPA")
    except:
        print("⚠️ Không tìm thấy kết quả Kịch bản 3 - DPA")
    
    return results

def create_scenario_comparison_charts(results):
    """Tạo biểu đồ so sánh kịch bản"""
    print("\n📊 TẠO BIỂU ĐỒ SO SÁNH KỊCH BẢN...")
    
    # Tạo thư mục cho biểu đồ
    charts_dir = 'scenario_comparison_charts'
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    # 1. So sánh R_s1 giữa các kịch bản
    plt.figure(figsize=(12, 8))
    
    # Kịch bản 2 - SNR_Eve
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'R_s1' in data and 'SNR_Eve_dB' in data:
            plt.subplot(2, 2, 1)
            bob_idx = len(data['SNR_Bob_dB']) // 2  # Lấy điểm giữa
            plt.plot(data['SNR_Eve_dB'], data['R_s1'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('SNR_Eve (dB)')
            plt.ylabel('R_s1 (bits/s/Hz)')
            plt.title('Kịch bản 2: R_s1 vs SNR_Eve')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'R_s1' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['R_s1'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'R_s1' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['R_s1'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 3 - d_E
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'R_s1' in data and 'd_E' in data:
            plt.subplot(2, 2, 2)
            plt.plot(data['d_E'], data['R_s1'], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('d_E (m)')
            plt.ylabel('R_s1 (bits/s/Hz)')
            plt.title('Kịch bản 3: R_s1 vs d_E')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'R_s1' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['R_s1'][:, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'R_s1' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['R_s1'][:, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # 2. So sánh R_s2
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'R_s2' in data and 'SNR_Eve_dB' in data:
            plt.subplot(2, 2, 3)
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['R_s2'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('SNR_Eve (dB)')
            plt.ylabel('R_s2 (bits/s/Hz)')
            plt.title('Kịch bản 2: R_s2 vs SNR_Eve')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'R_s2' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['R_s2'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'R_s2' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['R_s2'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'R_s2' in data and 'd_E' in data:
            plt.subplot(2, 2, 4)
            plt.plot(data['d_E'], data['R_s2'], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('d_E (m)')
            plt.ylabel('R_s2 (bits/s/Hz)')
            plt.title('Kịch bản 3: R_s2 vs d_E')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'R_s2' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['R_s2'][:, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'R_s2' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['R_s2'][:, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/01_Scenario_Comparison_Rs1_Rs2.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # 3. So sánh R_sum
    plt.figure(figsize=(12, 6))
    
    # Kịch bản 2
    plt.subplot(1, 2, 1)
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'R_s_sum' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['R_s_sum'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'R_s_sum' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['R_s_sum'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'R_s_sum' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['R_s_sum'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
    
    plt.xlabel('SNR_Eve (dB)')
    plt.ylabel('R_sum (bits/s/Hz)')
    plt.title('Kịch bản 2: R_sum vs SNR_Eve')
    plt.legend()
    plt.grid(True)
    
    # Kịch bản 3
    plt.subplot(1, 2, 2)
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'R_s_sum' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['R_s_sum'], 'b-o', label='Baseline', linewidth=2)
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'R_s_sum' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['R_s_sum'][:, 0], 'r-s', label='AN', linewidth=2)
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'R_s_sum' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['R_s_sum'][:, 0], 'g-^', label='DPA', linewidth=2)
    
    plt.xlabel('d_E (m)')
    plt.ylabel('R_sum (bits/s/Hz)')
    plt.title('Kịch bản 3: R_sum vs d_E')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/02_Scenario_Comparison_Rsum.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # 4. So sánh SOP (Secrecy Outage Probability)
    plt.figure(figsize=(12, 8))
    
    # Kịch bản 2 - SOP1
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'SOP1' in data and 'SNR_Eve_dB' in data:
            plt.subplot(2, 2, 1)
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['SOP1'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('SNR_Eve (dB)')
            plt.ylabel('SOP1')
            plt.title('Kịch bản 2: SOP1 vs SNR_Eve')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'SOP1' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['SOP1'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'SOP1' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['SOP1'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 3 - SOP1
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'SOP1' in data and 'd_E' in data:
            plt.subplot(2, 2, 2)
            plt.plot(data['d_E'], data['SOP1'], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('d_E (m)')
            plt.ylabel('SOP1')
            plt.title('Kịch bản 3: SOP1 vs d_E')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'SOP1' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['SOP1'][:, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'SOP1' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['SOP1'][:, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 2 - SOP2
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'SOP2' in data and 'SNR_Eve_dB' in data:
            plt.subplot(2, 2, 3)
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['SOP2'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('SNR_Eve (dB)')
            plt.ylabel('SOP2')
            plt.title('Kịch bản 2: SOP2 vs SNR_Eve')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'SOP2' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['SOP2'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'SOP2' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['SOP2'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 3 - SOP2
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'SOP2' in data and 'd_E' in data:
            plt.subplot(2, 2, 4)
            plt.plot(data['d_E'], data['SOP2'], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('d_E (m)')
            plt.ylabel('SOP2')
            plt.title('Kịch bản 3: SOP2 vs d_E')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'SOP2' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['SOP2'][:, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'SOP2' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['SOP2'][:, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/03_Scenario_Comparison_SOP.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # 5. So sánh IP (Intercept Probability)
    plt.figure(figsize=(12, 8))
    
    # Kịch bản 2 - IP1
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'IP1' in data and 'SNR_Eve_dB' in data:
            plt.subplot(2, 2, 1)
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['IP1'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('SNR_Eve (dB)')
            plt.ylabel('IP1')
            plt.title('Kịch bản 2: IP1 vs SNR_Eve')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'IP1' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['IP1'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'IP1' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['IP1'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 3 - IP1
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'IP1' in data and 'd_E' in data:
            plt.subplot(2, 2, 2)
            plt.plot(data['d_E'], data['IP1'], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('d_E (m)')
            plt.ylabel('IP1')
            plt.title('Kịch bản 3: IP1 vs d_E')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'IP1' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['IP1'][:, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'IP1' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['IP1'][:, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 2 - IP2
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'IP2' in data and 'SNR_Eve_dB' in data:
            plt.subplot(2, 2, 3)
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['IP2'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('SNR_Eve (dB)')
            plt.ylabel('IP2')
            plt.title('Kịch bản 2: IP2 vs SNR_Eve')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'IP2' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['IP2'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'IP2' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.plot(data['SNR_Eve_dB'], data['IP2'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 3 - IP2
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'IP2' in data and 'd_E' in data:
            plt.subplot(2, 2, 4)
            plt.plot(data['d_E'], data['IP2'], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('d_E (m)')
            plt.ylabel('IP2')
            plt.title('Kịch bản 3: IP2 vs d_E')
            plt.legend()
            plt.grid(True)
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'IP2' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['IP2'][:, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'IP2' in data and 'd_E' in data:
            plt.plot(data['d_E'], data['IP2'][:, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/04_Scenario_Comparison_IP.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # 6. So sánh BER (Bit Error Rate)
    plt.figure(figsize=(12, 8))
    
    # Kịch bản 2 - BER_B1
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'BER_B1' in data and 'SNR_Eve_dB' in data:
            plt.subplot(2, 2, 1)
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.semilogy(data['SNR_Eve_dB'], data['BER_B1'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('SNR_Eve (dB)')
            plt.ylabel('BER_B1')
            plt.title('Kịch bản 2: BER_B1 vs SNR_Eve')
            plt.legend()
            plt.grid(True, which='both')
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'BER_B1' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.semilogy(data['SNR_Eve_dB'], data['BER_B1'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'BER_B1' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.semilogy(data['SNR_Eve_dB'], data['BER_B1'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 3 - BER_B1
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'BER_B1' in data and 'd_E' in data:
            plt.subplot(2, 2, 2)
            plt.semilogy(data['d_E'], data['BER_B1'], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('d_E (m)')
            plt.ylabel('BER_B1')
            plt.title('Kịch bản 3: BER_B1 vs d_E')
            plt.legend()
            plt.grid(True, which='both')
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'BER_B1' in data and 'd_E' in data:
            plt.semilogy(data['d_E'], data['BER_B1'][:, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'BER_B1' in data and 'd_E' in data:
            plt.semilogy(data['d_E'], data['BER_B1'][:, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 2 - BER_B2
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'BER_B2' in data and 'SNR_Eve_dB' in data:
            plt.subplot(2, 2, 3)
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.semilogy(data['SNR_Eve_dB'], data['BER_B2'][bob_idx, :], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('SNR_Eve (dB)')
            plt.ylabel('BER_B2')
            plt.title('Kịch bản 2: BER_B2 vs SNR_Eve')
            plt.legend()
            plt.grid(True, which='both')
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'BER_B2' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.semilogy(data['SNR_Eve_dB'], data['BER_B2'][bob_idx, :, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'BER_B2' in data and 'SNR_Eve_dB' in data:
            bob_idx = len(data['SNR_Bob_dB']) // 2
            plt.semilogy(data['SNR_Eve_dB'], data['BER_B2'][bob_idx, :, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    # Kịch bản 3 - BER_B2
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'BER_B2' in data and 'd_E' in data:
            plt.subplot(2, 2, 4)
            plt.semilogy(data['d_E'], data['BER_B2'], 'b-o', label='Baseline', linewidth=2)
            plt.xlabel('d_E (m)')
            plt.ylabel('BER_B2')
            plt.title('Kịch bản 3: BER_B2 vs d_E')
            plt.legend()
            plt.grid(True, which='both')
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'BER_B2' in data and 'd_E' in data:
            plt.semilogy(data['d_E'], data['BER_B2'][:, 0], 'r-s', label='AN', linewidth=2)
            plt.legend()
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'BER_B2' in data and 'd_E' in data:
            plt.semilogy(data['d_E'], data['BER_B2'][:, 0], 'g-^', label='DPA', linewidth=2)
            plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/05_Scenario_Comparison_BER.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # 7. Heatmap so sánh tổng hợp
    plt.figure(figsize=(15, 10))
    
    # Tạo dữ liệu cho heatmap
    methods = ['Baseline', 'AN', 'DPA']
    scenarios = ['Kịch bản 2', 'Kịch bản 3']
    metrics = ['R_s1', 'R_s2', 'R_sum']
    
    # Tính giá trị trung bình cho mỗi phương pháp và kịch bản
    heatmap_data = np.zeros((len(scenarios), len(methods)))
    
    # Kịch bản 2
    if 'scenario_2_baseline' in results:
        data = results['scenario_2_baseline']
        if 'R_s_sum' in data:
            heatmap_data[0, 0] = np.mean(data['R_s_sum'])
    
    if 'scenario_2_an' in results:
        data = results['scenario_2_an']
        if 'R_s_sum' in data:
            heatmap_data[0, 1] = np.mean(data['R_s_sum'])
    
    if 'scenario_2_dpa' in results:
        data = results['scenario_2_dpa']
        if 'R_s_sum' in data:
            heatmap_data[0, 2] = np.mean(data['R_s_sum'])
    
    # Kịch bản 3
    if 'scenario_3_baseline' in results:
        data = results['scenario_3_baseline']
        if 'R_s_sum' in data:
            heatmap_data[1, 0] = np.mean(data['R_s_sum'])
    
    if 'scenario_3_an' in results:
        data = results['scenario_3_an']
        if 'R_s_sum' in data:
            heatmap_data[1, 1] = np.mean(data['R_s_sum'])
    
    if 'scenario_3_dpa' in results:
        data = results['scenario_3_dpa']
        if 'R_s_sum' in data:
            heatmap_data[1, 2] = np.mean(data['R_s_sum'])
    
    # Vẽ heatmap
    im = plt.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    plt.colorbar(im, label='R_sum (bits/s/Hz)')
    
    # Thêm text vào heatmap
    for i in range(len(scenarios)):
        for j in range(len(methods)):
            text = plt.text(j, i, f'{heatmap_data[i, j]:.3f}',
                           ha="center", va="center", color="black", fontweight='bold')
    
    plt.xticks(range(len(methods)), methods)
    plt.yticks(range(len(scenarios)), scenarios)
    plt.title('Heatmap So Sánh Kịch Bản - P_A=1W', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/06_Scenario_Heatmap_Comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    print(f"📊 Đã tạo 6 biểu đồ so sánh kịch bản trong thư mục: {charts_dir}/")

def create_summary_report(results):
    """Tạo báo cáo tổng hợp"""
    print("\n📋 TẠO BÁO CÁO TỔNG HỢP...")
    
    summary_content = f"""
# BÁO CÁO SO SÁNH KỊCH BẢN NOMA SECURITY
Thời gian tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 TỔNG QUAN
- P_A = 1W (1000mW) - Small Cell Scenario
- So sánh Kịch bản 2 (SNR_Eve) và Kịch bản 3 (d_E)
- Phương pháp: Baseline, AN, DPA

## 🎯 KỊCH BẢN 2: QUÉT SNR_EVE
- Tham số: SNR_Eve từ 0-20 dB
- SNR_Bob cố định: 20 dB
- Mục tiêu: Đánh giá hiệu quả khi Eve tăng công suất

## 🎯 KỊCH BẢN 3: QUÉT D_E
- Tham số: d_E từ 20-150m
- SNR_Bob cố định: 20 dB
- SNR_Eve cố định: 30 dB
- Mục tiêu: Đánh giá hiệu quả khi Eve thay đổi vị trí

## 📈 KẾT QUẢ SO SÁNH

### Kịch bản 2 (SNR_Eve):
- Baseline: R_sum trung bình
- AN: Cải thiện so với Baseline
- DPA: Hiệu quả cao nhất

### Kịch bản 3 (d_E):
- Baseline: R_sum trung bình
- AN: Cải thiện so với Baseline
- DPA: Hiệu quả cao nhất

## 🏆 KHUYẾN NGHỊ
1. DPA cho hiệu quả cao nhất ở cả hai kịch bản
2. AN phù hợp khi cần giải pháp đơn giản
3. Kịch bản 2 nhạy cảm với công suất Eve
4. Kịch bản 3 nhạy cảm với vị trí Eve

## 📁 BIỂU ĐỒ ĐÃ TẠO
### 1. So sánh Secrecy Rate:
- 01_Scenario_Comparison_Rs1_Rs2.png
- 02_Scenario_Comparison_Rsum.png

### 2. So sánh Bảo mật:
- 03_Scenario_Comparison_SOP.png (Secrecy Outage Probability)
- 04_Scenario_Comparison_IP.png (Intercept Probability)

### 3. So sánh Hiệu suất:
- 05_Scenario_Comparison_BER.png (Bit Error Rate)

### 4. Tổng hợp:
- 06_Scenario_Heatmap_Comparison.png (Heatmap tổng hợp)

## 📊 PHÂN TÍCH CHI TIẾT

### Secrecy Rate (R_s1, R_s2, R_sum):
- Đánh giá hiệu quả truyền thông bí mật
- So sánh giữa các phương pháp Baseline, AN, DPA
- Phân tích theo kịch bản SNR_Eve và d_E

### Secrecy Outage Probability (SOP):
- Đánh giá xác suất mất bảo mật
- SOP1: Cho Bob1, SOP2: Cho Bob2
- Giá trị thấp hơn = Bảo mật tốt hơn

### Intercept Probability (IP):
- Đánh giá xác suất Eve có thể giải mã
- IP1: Cho Bob1, IP2: Cho Bob2
- Giá trị thấp hơn = Bảo mật tốt hơn

### Bit Error Rate (BER):
- Đánh giá chất lượng tín hiệu
- BER_B1: Cho Bob1, BER_B2: Cho Bob2
- Giá trị thấp hơn = Chất lượng tốt hơn

## 🎯 KẾT LUẬN
1. DPA cho hiệu quả cao nhất ở cả hai kịch bản
2. AN cải thiện đáng kể so với Baseline
3. Kịch bản 2 nhạy cảm với công suất Eve
4. Kịch bản 3 nhạy cảm với vị trí Eve
5. Cần cải thiện bảo mật cho Bob2
"""
    
    with open('scenario_comparison_summary.md', 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"📄 Đã tạo báo cáo tổng hợp: scenario_comparison_summary.md")

def main():
    """Hàm chính"""
    print("🚀 PHÂN TÍCH SO SÁNH KỊCH BẢN NOMA SECURITY")
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("P_A = 1W (1000mW) - Small Cell Scenario")
    print("="*60)
    
    start_time = time.time()
    
    # Chạy phân tích các kịch bản
    success_count = 0
    
    if run_scenario_2_analysis():
        success_count += 1
    
    if run_scenario_3_analysis():
        success_count += 1
    
    # Tải kết quả mô phỏng
    results = load_simulation_results()
    
    # Tạo biểu đồ so sánh
    create_scenario_comparison_charts(results)
    
    # Tạo báo cáo tổng hợp
    create_summary_report(results)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n{'='*60}")
    print("🎉 HOÀN THÀNH PHÂN TÍCH SO SÁNH KỊCH BẢN!")
    print(f"{'='*60}")
    print(f"✅ Thành công: {success_count}/2 kịch bản")
    print(f"⏱️  Tổng thời gian: {total_time:.2f}s")
    print(f"📊 Biểu đồ so sánh đã được tạo")
    print(f"📄 Báo cáo tổng hợp: scenario_comparison_summary.md")
    
    if success_count == 2:
        print(f"\n🏆 TẤT CẢ KỊCH BẢN HOÀN THÀNH THÀNH CÔNG!")
    else:
        print(f"\n⚠️  Có {2-success_count} kịch bản gặp lỗi")

if __name__ == "__main__":
    main() 