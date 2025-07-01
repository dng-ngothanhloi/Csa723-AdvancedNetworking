# Phân tích Dữ liệu Mô phỏng NOMA: Kịch bản 2 và 3

## Kịch bản 2: Quét SNR_Eve

### Thông số hệ thống
- Công suất truyền: P_A = 1 W
- Nhiễu nền: N_0 = 1.00e-15 W
- Hệ số suy hao: alpha = 3
- Băng thông: 10 MHz
- Số anten: 16
- Khoảng cách: Bob1 = 50 m, Bob2 = 100 m, Eve = 70 m
- Phân bổ công suất: alpha1 = 0.111, alpha2 = 0.889
- Tỷ lệ lỗi SIC: epsilon = 0.01
- Công suất nhiễu pilot: 0.2

### Phân tích
1. **Dung lượng kênh (C):**
   - **Bob1 (C_B1):** Giảm khi SNR_Eve tăng (ví dụ: từ 13.61 Mbps xuống 10.54 Mbps tại SNR_Bob = 0 dB).
   - **Bob2 (C_B2):** Ổn định, ít bị ảnh hưởng bởi SNR_Eve, tăng mạnh khi SNR_Bob tăng (từ ~14.8 Mbps lên ~74.9 Mbps).
   - **Eve (C_E):** Tăng khi SNR_Bob tăng (từ ~25.9 Mbps lên ~89.4 Mbps), nhưng ít thay đổi theo SNR_Eve.
2. **Tỷ lệ lỗi bit (BER):** Dao động ~0.49–0.51, không cải thiện đáng kể, do nhiễu từ Eve và lỗi SIC.
3. **Tốc độ bí mật (R_s):**
   - **R_s1:** Giảm khi SNR_Eve tăng, gần bằng 0 khi SNR_Bob ≥ 14 dB.
   - **R_s2:** Bằng 0 trên toàn bộ phạm vi.
4. **Xác suất gián đoạn bí mật (SOP):**
   - **SOP1:** Tăng lên 1.0 khi SNR_Bob ≥ 10 dB.
   - **SOP2:** Luôn bằng 1.0.
5. **Xác suất chặn (IP):**
   - **IP1:** Tăng khi SNR_Eve tăng, đạt 1.0 tại SNR_Bob = 20 dB.
   - **IP2:** Luôn bằng 1.0.
6. **Hiệu quả bí mật (eta_s):**
   - **eta_s1:** Giảm khi SNR_Eve tăng, xuống 0.0 tại SNR_Bob = 20 dB.
   - **eta_s2:** Rất thấp (~10^-11 đến 10^-12).

### Kết luận
- Nhiễu từ Eve làm suy giảm hiệu suất của Bob1, trong khi Bob2 duy trì dung lượng ổn định nhưng không đạt tốc độ bí mật.
- Hệ thống bị ảnh hưởng mạnh bởi nhiễu và lỗi SIC.

## Kịch bản 3: Quét d_E

### Thông số hệ thống
- Tương tự Kịch bản 2, nhưng:
  - Khoảng cách Eve: d_E = 20–150 m (bước 10 m)
  - SNR_Bob: 20 dB
  - SNR_Eve: 30 dB

### Phân tích
1. **Dung lượng kênh (C):**
   - **Bob1 (C_B1):** ~37.55 Mbps, ngoại trừ điểm bất thường tại d_E = 50 m (0.01 Mbps).
   - **Bob2 (C_B2):** Giảm từ 337.40 Mbps (d_E = 20 m) xuống 198.18 Mbps (d_E = 100 m), sau đó tăng lên 332.24 Mbps (d_E = 150 m).
   - **Eve (C_E):** Giảm từ 187.94 Mbps (d_E = 20 m) xuống 152.42 Mbps (d_E = 70 m), sau đó tăng lên 185.15 Mbps (d_E = 150 m).
2. **Tỷ lệ lỗi bit (BER):** ~0.49–0.51, tương tự Kịch bản 2.
3. **Tốc độ bí mật (R_s):**
   - **R_s1:** Bằng 0 trên toàn bộ phạm vi.
   - **R_s2:** Tăng từ 14.95 (d_E = 20 m) lên 20.31 (d_E = 90 m), sau đó giảm xuống 16.46 (d_E = 150 m).
4. **Xác suất gián đoạn bí mật (SOP):**
   - **SOP1:** Luôn bằng 1.0.
   - **SOP2:** Bằng 0.0, cho thấy Bob2 không bị gián đoạn.
5. **Xác suất chặn (IP):**
   - **IP1:** Luôn bằng 1.0.
   - **IP2:** Bằng 0.0, cho thấy Eve không chặn được Bob2.
6. **Hiệu quả bí mật (eta_s):**
   - **eta_s1:** Bằng 0.0.
   - **eta_s2:** Tăng từ 1.49e-06 lên 2.03e-06, sau đó giảm xuống 1.65e-06.

### Kết luận
- Khoảng cách của Eve ảnh hưởng lớn đến Bob2, với tốc độ bí mật cao khi Eve ở xa.
- Bob1 không đạt tốc độ bí mật do SNR_Eve cao.
- Nhiễu và lỗi SIC tiếp tục làm giảm hiệu suất.

## Đề xuất
- Giảm tỷ lệ lỗi SIC để cải thiện BER.
- Tối ưu hóa phân bổ công suất để cân bằng hiệu suất giữa Bob1 và Bob2.
- Kiểm tra điểm bất thường tại d_E = 50 m.
- Cung cấp biểu đồ để trực quan hóa xu hướng.