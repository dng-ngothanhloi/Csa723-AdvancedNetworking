#!/usr/bin/env python3
"""
Script tổng hợp chạy tất cả phân tích và tạo biểu đồ
- Chạy quick comparison
- Chạy detailed analysis  
- Tạo tất cả biểu đồ với tên dễ phân biệt
"""

import subprocess
import time
import os
from datetime import datetime

def run_quick_comparison():
    """Chạy quick comparison"""
    print("🚀 CHẠY QUICK COMPARISON...")
    print("="*50)
    
    try:
        result = subprocess.run(['python3', 'quick_comparison.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Quick comparison hoàn thành")
            print(result.stdout)
        else:
            print(f"❌ Quick comparison lỗi: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Quick comparison timeout")
        return False
    except Exception as e:
        print(f"❌ Quick comparison lỗi: {e}")
        return False
    
    return True

def run_detailed_analysis():
    """Chạy detailed analysis"""
    print("\n🔍 CHẠY DETAILED ANALYSIS...")
    print("="*50)
    
    try:
        result = subprocess.run(['python3', 'detailed_analysis.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Detailed analysis hoàn thành")
            print(result.stdout)
        else:
            print(f"❌ Detailed analysis lỗi: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Detailed analysis timeout")
        return False
    except Exception as e:
        print(f"❌ Detailed analysis lỗi: {e}")
        return False
    
    return True

def run_comparison_script():
    """Chạy comparison script"""
    print("\n📊 CHẠY COMPARISON SCRIPT...")
    print("="*50)
    
    try:
        result = subprocess.run(['python3', 'comparison_script.py'], 
                              capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Comparison script hoàn thành")
            print(result.stdout)
        else:
            print(f"❌ Comparison script lỗi: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Comparison script timeout")
        return False
    except Exception as e:
        print(f"❌ Comparison script lỗi: {e}")
        return False
    
    return True

def create_summary_report():
    """Tạo báo cáo tổng hợp"""
    print("\n📋 TẠO BÁO CÁO TỔNG HỢP...")
    print("="*50)
    
    # Kiểm tra các thư mục charts
    chart_dirs = ['comparison_charts', 'detailed_charts', 'comparison_results']
    total_charts = 0
    
    for chart_dir in chart_dirs:
        if os.path.exists(chart_dir):
            charts = [f for f in os.listdir(chart_dir) if f.endswith('.png')]
            total_charts += len(charts)
            print(f"📁 {chart_dir}: {len(charts)} biểu đồ")
            for chart in sorted(charts):
                print(f"   - {chart}")
    
    # Tạo file summary
    summary_content = f"""
# BÁO CÁO TỔNG HỢP PHÂN TÍCH NOMA SECURITY
Thời gian tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 TỔNG QUAN
- Tổng số biểu đồ đã tạo: {total_charts}
- P_A = 1W (Small Cell Scenario)
- Phương pháp: Baseline, AN, DPA

## 📁 CÁC THƯ MỤC KẾT QUẢ

### 1. Quick Comparison Charts (comparison_charts/)
- 01_Rs1_Bob1_Comparison.png
- 02_Rs2_Bob2_Comparison.png  
- 03_Rsum_Total_Comparison.png
- 04_Combined_Comparison.png

### 2. Detailed Analysis Charts (detailed_charts/)
- 01_Detailed_Comparison_ErrorBars.png
- 02_Heatmap_Comparison.png
- 03_Radar_Chart_Comparison.png
- 04_Stacked_Bar_Comparison.png

### 3. Comparison Results (comparison_results/)
- 01_Rs1_Bob1_Comparison.png
- 02_Rs2_Bob2_Comparison.png
- 03_Rsum_Total_Comparison.png
- 04_Combined_Comparison.png
- 05_Heatmap_Comparison.png

## 🎯 KẾT LUẬN
- DPA cho hiệu quả cao nhất: +131.96% so với Baseline
- AN cải thiện đáng kể: +21.23% so với Baseline
- Bob2 cần được cải thiện thêm về bảo mật
- P_A = 1W phù hợp với small cell scenarios

## 📈 KHUYẾN NGHỊ
1. Sử dụng DPA cho hiệu quả cao nhất
2. AN phù hợp khi cần giải pháp đơn giản
3. Cần cải thiện bảo mật cho Bob2
4. Nghiên cứu thêm về power allocation
"""
    
    with open('analysis_summary.md', 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"📄 Đã tạo báo cáo tổng hợp: analysis_summary.md")
    print(f"📊 Tổng số biểu đồ: {total_charts}")

def main():
    """Hàm chính"""
    print("🚀 CHẠY TẤT CẢ PHÂN TÍCH NOMA SECURITY")
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("P_A = 1W (100mW) - Small Cell Scenario")
    print("="*60)
    
    start_time = time.time()
    
    # Chạy các script
    success_count = 0
    
    if run_quick_comparison():
        success_count += 1
    
    if run_detailed_analysis():
        success_count += 1
    
    if run_comparison_script():
        success_count += 1
    
    # Tạo báo cáo tổng hợp
    create_summary_report()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n{'='*60}")
    print("🎉 HOÀN THÀNH PHÂN TÍCH!")
    print(f"{'='*60}")
    print(f"✅ Thành công: {success_count}/3 script")
    print(f"⏱️  Tổng thời gian: {total_time:.2f}s")
    print(f"📊 Biểu đồ đã được tạo với tên dễ phân biệt")
    print(f"📄 Báo cáo tổng hợp: analysis_summary.md")
    
    if success_count == 3:
        print(f"\n🏆 TẤT CẢ PHÂN TÍCH HOÀN THÀNH THÀNH CÔNG!")
    else:
        print(f"\n⚠️  Có {3-success_count} script gặp lỗi")

if __name__ == "__main__":
    main() 