
# BÁO CÁO SO SÁNH KỊCH BẢN NOMA SECURITY
Thời gian tạo: 2025-07-05 13:02:22

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
