# Đánh giá và So sánh các giải pháp mô phỏng bảo mật vật lý NOMA

## 1. Đánh giá tổng quát các tham số hệ thống mô phỏng

### A. Tham số vật lý & hệ thống

| Tham số                  | Ý nghĩa / Vai trò                                         | Giá trị điển hình / Khoảng giá trị      |
|--------------------------|----------------------------------------------------------|-----------------------------------------|
| Số người dùng (N_users)  | Số user hợp pháp trong hệ thống NOMA                     | 2-4                                     |
| Số anten tại BS (N_ant)  | Độ đa dạng không gian, ảnh hưởng đến bảo mật              | 16-64 (Massive MIMO)                    |
| Công suất phát BS (P_BS) | Năng lượng truyền, ảnh hưởng SNR                         | 20-40 dBm (hoặc normalized = 1)         |
| SNR (SNR_dB)             | Tỉ số tín hiệu trên nhiễu, quyết định chất lượng kênh    | -10 dB đến 20 dB                        |
| Băng thông (B)           | Dải tần truyền dẫn                                       | 10 MHz                                  |
| Số lần lặp (N_iter)      | Độ chính xác thống kê (Monte Carlo)                      | 1000-10000                              |
| Khoảng cách              | Vị trí user/kẻ nghe lén, ảnh hưởng fading                | 10-100m                                 |
| Loại fading              | Mô hình kênh truyền                                      | Rayleigh hoặc Rician                    |

### B. Tham số bảo mật

| Tham số                  | Ý nghĩa / Vai trò                                         | Giá trị điển hình / Khoảng giá trị      |
|--------------------------|----------------------------------------------------------|-----------------------------------------|
| Ngưỡng secrecy (R_th)    | Ngưỡng đánh giá xác suất rò rỉ thông tin (SOP)           | 0.5-2 bit/s/Hz                          |
| Loại tấn công            | Kịch bản nghe lén chủ động (giả mạo, ô nhiễm định vị)    | Chọn theo mục tiêu mô phỏng             |

### C. Tham số mô phỏng nâng cao (khi mở rộng)
- Số lượng kẻ nghe lén
- Số lượng cell, cell edge user
- Loại giải pháp bảo mật (Artificial Noise - AN, Dynamic Power Control - DPC, Beamforming, ...)
- Mô hình mạng đa cell, đa người dùng, đa anten

## 1. Cơ sở lý thuyết và công thức tính toán

### 1.1. Các tham số hệ thống mô phỏng
- **Công suất phát (P_A):** Công suất truyền của Alice (Watt)
- **Nhiễu nền (N_0):** Công suất nhiễu nền (Watt)
- **Hệ số suy hao (\(\alpha\)):** Đặc trưng cho môi trường truyền sóng
- **Khoảng cách (d_B, d_E):** Khoảng cách từ Alice đến Bob/Eve (m)
- **Băng thông (B):** Băng thông hệ thống (Hz)
- **Số lượng mẫu mô phỏng (num_samples):** Số lần lặp Monte Carlo
- **Số lượng anten:** Có thể mở rộng cho MIMO
- **SNR:** Có thể thay đổi để đánh giá ảnh hưởng

### 1.2. Công thức tính toán

- **SNR tại Bob và Eve:**
  $SNR_{Bob} = \frac{P_A |h_B|^2}{d_B^\alpha N_0}$
  
  $SNR_{Eve} = \frac{P_A |h_E|^2}{d_E^\alpha N_0}$
  
  Nếu Eve chủ động: $SNR_{Eve} \leftarrow SNR_{Eve} + \frac{|noise_{eve}|^2}{N_0}$

- **Dung lượng kênh (Shannon):**
  $C_{AB} = B \cdot \log_2(1 + SNR_{Bob})$
  
  $C_{AE} = B \cdot \log_2(1 + SNR_{Eve})$

- **Secrecy Capacity:**
  $C_S = \max(0, C_{AB} - C_{AE})$

- **Secrecy Outage Probability:**
  $O_S = P(C_S < \epsilon_S \cdot B)$

- **Secrecy Rate:**
  $R_s = \max(0, mean(C_{AB}) - mean(C_{AE}))$

- **Secrecy Spectral Efficiency:**
  $\eta_s = \frac{R_s}{B}$

### 1.3. Đánh giá tổng quát các tham số hệ thống mô phỏng
- Thay đổi các tham số như SNR, vị trí Bob/Eve, số lượng anten, băng thông để đánh giá ảnh hưởng đến các chỉ số bảo mật.
- Có thể mô phỏng nhiều kịch bản thực tế: IoT, mạng di động, MIMO, v.v.

### 1.4. Tính toán các chỉ số bảo mật
- Tính toán các chỉ số bảo mật (O_S, R_s, \(\eta_s\)) cho từng bộ tham số hệ thống.
- So sánh kết quả giữa các kịch bản để rút ra nhận xét về hiệu quả bảo mật.

### 1.5. Thuật toán mô phỏng tổng quát
1. **Khởi tạo các tham số hệ thống:** P_A, N_0, alpha, B, d_B, d_E, num_samples, số lượng anten, v.v.
2. **Lặp qua các giá trị SNR, vị trí, số lượng anten, v.v.:**
   - Sinh ngẫu nhiên fading (Rayleigh, Rician, ...)
   - Tính SNR cho Bob/Eve
   - Nếu Eve chủ động, cộng thêm nhiễu giả mạo
   - Tính dung lượng kênh, Secrecy Capacity
   - Tính các chỉ số bảo mật (O_S, R_s, \(\eta_s\))
3. **Lưu kết quả, vẽ đồ thị, xuất số liệu**
4. **So sánh, đánh giá, rút ra kết luận**

**Ghi chú:**
- Có thể mở rộng mô phỏng cho nhiều người dùng, nhiều kẻ nghe lén, nhiều anten (MIMO), các mô hình fading khác nhau.
- Kết quả mô phỏng giúp đánh giá hiệu quả các giải pháp bảo mật vật lý trong nhiều kịch bản thực tế.

---

## 2. So sánh về mặt kỹ thuật

### NOMAStandard.py (Cải tiến 1)
- **Mô hình hóa kênh:** Rayleigh fading, tính đến suy hao đường truyền với khoảng cách và hệ số alpha.
- **Thông số thực tế:** Sử dụng công suất, nhiễu nền, khoảng cách, băng thông, ngưỡng bảo mật phù hợp với thực tế IoT nông nghiệp.
- **Tính toán hiệu năng:**
  - Tính SNR cho Bob và Eve.
  - Tính dung lượng kênh (Shannon) cho Bob và Eve.
  - Tính Secrecy Capacity \( C_S = \max(0, C_{AB} - C_{AE}) \).
  - Tính xác suất dừng bảo mật (Secrecy Outage Probability) \( O_S \).
- **Kịch bản mô phỏng:** 3 giá trị khoảng cách Bob (d_B), quét dọc d_E (khoảng cách Eve).
- **Đầu ra:** Đồ thị xác suất dừng bảo mật theo d_E, có vùng màu trực quan.

### NOMAImprovement.py (Cải tiến 2)
- **Kế thừa toàn bộ các đặc điểm của Cải tiến 1**, đồng thời bổ sung:
  - **Mô phỏng kẻ nghe lén chủ động:** Eve có thể phát nhiễu giả mạo (jamming/active eavesdropping), làm tăng SNR_Eve.
  - **Tính thêm các chỉ số bảo mật:**
    - Secrecy Rate \( R_s = \max(0, \text{mean}(C_{AB}) - \text{mean}(C_{AE})) \).
    - Secrecy Spectral Efficiency \( \eta_s = R_s / B \).
  - **Điều chỉnh ngưỡng bảo mật** phù hợp với băng thông lớn hơn (10 MHz).
  - **Tối ưu hóa tốc độ mô phỏng:** Giảm số mẫu, vector hóa.
- **Đầu ra:** Ngoài xác suất dừng bảo mật, còn có đồ thị Secrecy Rate và Secrecy Spectral Efficiency.

---

## 3. Đánh giá kết quả mô phỏng và số liệu thực tế

### 3.1. Kết quả mô phỏng với NOMAStandard.py (Eve thụ động)

#### Hình ảnh minh họa (đồ thị)
![Xác suất dừng bảo mật - NOMAStandard](Results/NOMAStandard-ProbabilityOfStopping.png)

#### Bảng số liệu xác suất dừng bảo mật (O_S) theo d_B, d_E

| d_B (m) | d_E (m) | O_S |
|---------|---------|------|
| 100     | 100.0   | 0.5466 |
| 100     | 108.2   | 0.4879 |
| 100     | 116.3   | 0.4348 |
| 100     | 124.5   | 0.3851 |
| 100     | 132.7   | 0.3446 |
| 100     | 255.1   | 0.0687 |
| 100     | 263.3   | 0.0621 |
| 100     | 271.4   | 0.0578 |
| 100     | 279.6   | 0.0523 |
| 100     | 287.8   | 0.0481 |
| 100     | 483.7   | 0.0111 |
| 100     | 491.8   | 0.0104 |
| 100     | 500.0   | 0.0108 |
| 50      | 100.0   | 0.1313 |
| 50      | 108.2   | 0.1092 |
| 50      | 116.3   | 0.0875 |
| 50      | 124.5   | 0.0703 |
| 50      | 132.7   | 0.0622 |
| 50      | 255.1   | 0.0094 |
| 50      | 263.3   | 0.0080 |
| 50      | 271.4   | 0.0076 |
| 50      | 279.6   | 0.0073 |
| 50      | 287.8   | 0.0066 |
| 50      | 483.7   | 0.0012 |
| 50      | 491.8   | 0.0013 |
| 50      | 500.0   | 0.0011 |
| 20      | 100.0   | 0.0097 |
| 20      | 108.2   | 0.0073 |
| 20      | 116.3   | 0.0061 |
| 20      | 124.5   | 0.0048 |
| 20      | 132.7   | 0.0041 |
| 20      | 255.1   | 0.0006 |
| 20      | 263.3   | 0.0004 |
| 20      | 271.4   | 0.0003 |
| 20      | 279.6   | 0.0003 |
| 20      | 287.8   | 0.0004 |
| 20      | 483.7   | 0.0001 |
| 20      | 491.8   | 0.0001 |
| 20      | 500.0   | 0.0001 |

---

### 3.2. Kết quả mô phỏng với NOMAImprovement.py (Eve chủ động phát nhiễu)

#### Hình ảnh minh họa (đồ thị)
![Xác suất dừng bảo mật - NOMAImprovement](Results/NOMAImproment-ProbabilityOfStopping.png)

![Secrecy Rate - NOMAImprovement](Results/NOMAImproment-SecrecyRate.png)

![Secrecy Spectral Efficiency - NOMAImprovement](Results/NOMAImproment-SecrecySpectralEfficecy.png)

#### Bảng số liệu xác suất dừng bảo mật (O_S), Secrecy Rate (R_s), Secrecy Spectral Efficiency (eta_s)

| d_B (m) | d_E (m) | O_S | R_s | eta_s |
|---------|---------|------|------|-------|
| 100     | 100.0   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 108.2   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 116.3   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 124.5   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 132.7   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 255.1   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 263.3   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 271.4   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 279.6   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 287.8   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 483.7   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 491.8   | 1.0000 | 0.0000 | 0.0000 |
| 100     | 500.0   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 100.0   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 108.2   | 0.9999 | 0.0001 | 0.0001 |
| 50      | 116.3   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 124.5   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 132.7   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 255.1   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 263.3   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 271.4   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 279.6   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 287.8   | 0.9999 | 0.0003 | 0.0003 |
| 50      | 483.7   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 491.8   | 1.0000 | 0.0000 | 0.0000 |
| 50      | 500.0   | 1.0000 | 0.0000 | 0.0000 |
| 20      | 100.0   | 0.9999 | 0.0001 | 0.0001 |
| 20      | 108.2   | 1.0000 | 0.0000 | 0.0000 |
| 20      | 116.3   | 0.9999 | 0.0002 | 0.0002 |
| 20      | 124.5   | 0.9996 | 0.0009 | 0.0009 |
| 20      | 132.7   | 0.9996 | 0.0007 | 0.0007 |
| 20      | 255.1   | 0.9999 | 0.0002 | 0.0002 |
| 20      | 263.3   | 0.9998 | 0.0004 | 0.0004 |
| 20      | 271.4   | 0.9999 | 0.0003 | 0.0003 |
| 20      | 279.6   | 1.0000 | 0.0001 | 0.0001 |
| 20      | 287.8   | 0.9998 | 0.0002 | 0.0002 |
| 20      | 483.7   | 0.9998 | 0.0002 | 0.0002 |
| 20      | 491.8   | 0.9995 | 0.0015 | 0.0015 |
| 20      | 500.0   | 0.9998 | 0.0003 | 0.0003 |

---

**Ghi chú:**
- Số liệu đầy đủ được lưu trong các file kết quả `.interactive`.
- Đồ thị minh họa được lưu trong thư mục Results và đã được chèn vào báo cáo. 