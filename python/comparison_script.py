#!/usr/bin/env python3
"""
Script so sánh hiệu quả các phương pháp bảo mật NOMA
- Baseline: NOMA không có AN
- AN: NOMA với Artificial Noise
- DPA: NOMA với Dynamic Power Allocation
"""

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time
import os
from datetime import datetime

def run_simulation(script_name, description):
    """Chạy mô phỏng và trả về thời gian thực thi"""
    print(f"\n{'='*60}")
    print(f"CHẠY MÔ PHỎNG: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Chạy script
        result = subprocess.run(['python3', script_name], 
                              capture_output=True, text=True, timeout=300)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Thành công! Thời gian thực thi: {execution_time:.2f} giây")
            return True, execution_time, result.stdout
        else:
            print(f"❌ Lỗi! Exit code: {result.returncode}")
            print(f"Error: {result.stderr}")
            return False, execution_time, result.stderr
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout! Script chạy quá 5 phút")
        return False, 300, "Timeout"
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False, 0, str(e)

def analyze_results():
    """Phân tích kết quả từ các file .npy"""
    print(f"\n{'='*60}")
    print("PHÂN TÍCH KẾT QUẢ")
    print(f"{'='*60}")
    
    results = {}
    
    # Danh sách file kết quả
    files = [
        ('simulation_results_snr.npy', 'Baseline (không AN)'),
        ('simulation_results_snr_an.npy', 'Với AN'),
        ('simulation_results_snr_an_dpa.npz', 'Với AN + DPA'),
        ('simulation_results_de.npy', 'Baseline d_E'),
        ('simulation_results_de_an.npy', 'AN d_E'),
        ('simulation_results_de_an_dpa.npz', 'AN + DPA d_E')
    ]
    
    for filename, description in files:
        if os.path.exists(filename):
            try:
                if filename.endswith('.npz'):
                    data = np.load(filename)
                else:
                    data = np.load(filename, allow_pickle=True).item()
                
                # Trích xuất metrics chính
                if 'R_s1' in data:
                    r_s1_avg = np.mean(data['R_s1'])
                    r_s2_avg = np.mean(data['R_s2'])
                    r_sum_avg = np.mean(data['R_s_sum'])
                    
                    results[description] = {
                        'R_s1_avg': r_s1_avg,
                        'R_s2_avg': r_s2_avg,
                        'R_sum_avg': r_sum_avg,
                        'file': filename
                    }
                    
                    print(f"\n📊 {description}:")
                    print(f"   R_s1 trung bình: {r_s1_avg:.4f} bits/s/Hz")
                    print(f"   R_s2 trung bình: {r_s2_avg:.4f} bits/s/Hz")
                    print(f"   R_sum trung bình: {r_sum_avg:.4f} bits/s/Hz")
                    
            except Exception as e:
                print(f"❌ Lỗi đọc file {filename}: {e}")
        else:
            print(f"⚠️  File {filename} không tồn tại")
    
    return results

def create_comparison_plots(results):
    """Tạo biểu đồ so sánh với tên file dễ phân biệt"""
    print("\n📊 Tạo biểu đồ so sánh...")
    
    if not results:
        print("❌ Không có dữ liệu để vẽ")
        return
    
    # Tạo thư mục cho charts
    charts_dir = "comparison_results"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    methods = list(results.keys())
    
    # Biểu đồ 1: So sánh R_s1 (Bob1)
    fig, ax = plt.subplots(figsize=(12, 8))
    r_s1_values = [results[m]['R_s1_avg'] for m in methods]
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
    fig, ax = plt.subplots(figsize=(12, 8))
    r_s2_values = [results[m]['R_s2_avg'] for m in methods]
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
    fig, ax = plt.subplots(figsize=(12, 8))
    r_sum_values = [results[m]['R_sum_avg'] for m in methods]
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
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7))
    
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
    
    # Biểu đồ 5: Heatmap so sánh
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Chuẩn bị dữ liệu heatmap
    metrics = ['R_s1_avg', 'R_s2_avg', 'R_sum_avg']
    metric_labels = ['R_s1', 'R_s2', 'R_sum']
    
    heatmap_data = []
    for method in methods:
        row = [results[method][metric] for metric in metrics]
        heatmap_data.append(row)
    
    heatmap_data = np.array(heatmap_data)
    
    # Vẽ heatmap
    im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    
    # Thêm labels
    ax.set_xticks(range(len(metric_labels)))
    ax.set_yticks(range(len(methods)))
    ax.set_xticklabels(metric_labels)
    ax.set_yticklabels(methods)
    
    # Thêm giá trị trong cells
    for i in range(len(methods)):
        for j in range(len(metrics)):
            text = ax.text(j, i, f'{heatmap_data[i, j]:.3f}',
                          ha="center", va="center", color="black", fontweight='bold')
    
    ax.set_title('Heatmap Comparison - P_A=1W', fontsize=16, fontweight='bold', pad=20)
    plt.colorbar(im, ax=ax, label='Bits/s/Hz')
    plt.tight_layout()
    plt.savefig(f'{charts_dir}/05_Heatmap_Comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    
    print(f"📊 Đã tạo 5 biểu đồ trong thư mục: {charts_dir}/")
    print(f"   - 01_Rs1_Bob1_Comparison.png")
    print(f"   - 02_Rs2_Bob2_Comparison.png")
    print(f"   - 03_Rsum_Total_Comparison.png")
    print(f"   - 04_Combined_Comparison.png")
    print(f"   - 05_Heatmap_Comparison.png")

def generate_report(results, execution_times):
    """Tạo báo cáo tổng hợp"""
    print(f"\n{'='*60}")
    print("BÁO CÁO TỔNG HỢP")
    print(f"{'='*60}")
    
    # Tìm phương pháp tốt nhất
    best_r_s1 = max(results.items(), key=lambda x: x[1]['R_s1_avg'])
    best_r_s2 = max(results.items(), key=lambda x: x[1]['R_s2_avg'])
    best_r_sum = max(results.items(), key=lambda x: x[1]['R_sum_avg'])
    
    print(f"\n🏆 PHƯƠNG PHÁP TỐT NHẤT:")
    print(f"   R_s1 cao nhất: {best_r_s1[0]} ({best_r_s1[1]['R_s1_avg']:.4f} bits/s/Hz)")
    print(f"   R_s2 cao nhất: {best_r_s2[0]} ({best_r_s2[1]['R_s2_avg']:.4f} bits/s/Hz)")
    print(f"   R_sum cao nhất: {best_r_sum[0]} ({best_r_sum[1]['R_sum_avg']:.4f} bits/s/Hz)")
    
    print(f"\n⏱️  THỜI GIAN THỰC THI:")
    for method, time_taken in execution_times.items():
        print(f"   {method}: {time_taken:.2f} giây")
    
    # Tính cải thiện
    if len(results) >= 2:
        baseline = list(results.keys())[0]  # Giả sử phương pháp đầu tiên là baseline
        baseline_r_sum = results[baseline]['R_sum_avg']
        
        print(f"\n📈 CẢI THIỆN SO VỚI BASELINE ({baseline}):")
        for method, data in results.items():
            if method != baseline:
                improvement = ((data['R_sum_avg'] - baseline_r_sum) / baseline_r_sum) * 100
                print(f"   {method}: {improvement:+.2f}%")
    
    # Lưu báo cáo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"comparison_report_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("BÁO CÁO SO SÁNH HIỆU QUẢ NOMA SECURITY\n")
        f.write("="*50 + "\n\n")
        f.write(f"Thời gian tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("KẾT QUẢ CHI TIẾT:\n")
        for method, data in results.items():
            f.write(f"\n{method}:\n")
            f.write(f"  R_s1 trung bình: {data['R_s1_avg']:.4f} bits/s/Hz\n")
            f.write(f"  R_s2 trung bình: {data['R_s2_avg']:.4f} bits/s/Hz\n")
            f.write(f"  R_sum trung bình: {data['R_sum_avg']:.4f} bits/s/Hz\n")
        
        f.write(f"\nPHƯƠNG PHÁP TỐT NHẤT:\n")
        f.write(f"  R_s1: {best_r_s1[0]} ({best_r_s1[1]['R_s1_avg']:.4f})\n")
        f.write(f"  R_s2: {best_r_s2[0]} ({best_r_s2[1]['R_s2_avg']:.4f})\n")
        f.write(f"  R_sum: {best_r_sum[0]} ({best_r_sum[1]['R_sum_avg']:.4f})\n")
    
    print(f"\n💾 Báo cáo đã lưu: {report_filename}")

def main():
    """Hàm chính"""
    print("🚀 BẮT ĐẦU SO SÁNH HIỆU QUẢ NOMA SECURITY")
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Danh sách script cần chạy
    scripts = [
        ('NOMAImprovementTwoUserFinal.py', 'Baseline - NOMA không có AN'),
        ('NOMA_SimulationFinalWith_AN.py', 'NOMA với Artificial Noise'),
        ('NOMA_SimulationFinalWith_AN_DPC.py', 'NOMA với AN + Dynamic Power Allocation')
    ]
    
    execution_times = {}
    successful_runs = []
    
    # Chạy các script
    for script_name, description in scripts:
        if os.path.exists(script_name):
            success, time_taken, output = run_simulation(script_name, description)
            execution_times[description] = time_taken
            
            if success:
                successful_runs.append(description)
                print(f"✅ {description} hoàn thành")
            else:
                print(f"❌ {description} thất bại")
        else:
            print(f"⚠️  File {script_name} không tồn tại")
    
    # Phân tích kết quả
    results = analyze_results()
    
    # Tạo biểu đồ so sánh
    if results:
        create_comparison_plots(results)
    
    # Tạo báo cáo
    if results and execution_times:
        generate_report(results, execution_times)
    
    print(f"\n🎉 HOÀN THÀNH! {len(successful_runs)}/{len(scripts)} script chạy thành công")

if __name__ == "__main__":
    main() 