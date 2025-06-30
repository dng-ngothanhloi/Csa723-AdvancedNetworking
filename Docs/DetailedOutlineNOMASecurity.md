# Đề cương chi tiết: Đánh giá hiệu năng Các Giải Pháp Bảo Mật mạng NOMA có chiến lược chủ động nghe lén dựa trên mô phỏng MATLAB

## I. ĐẶT VẤN ĐỀ

### 1.1. Bối cảnh nghiên cứu
- Tổng quan về mạng 5G và vai trò của Đa truy cập phi trực giao (NOMA) trong việc tăng hiệu suất phổ và hỗ trợ kết nối mật độ cao.
- Thách thức bảo mật trong NOMA, đặc biệt với chiến lược nghe lén chủ động (active eavesdropping) như giả mạo tín hiệu, ô nhiễm định vị (pilot contamination), và can thiệp SIC.
- Tầm quan trọng của việc đánh giá hiệu năng bảo mật trong các ứng dụng thực tế của 5G (IoT, giao tiếp máy-máy, v.v.).

### 1.2. Mục tiêu nghiên cứu
- Đánh giá hiệu năng bảo mật của mạng NOMA dưới tác động của chiến lược nghe lén chủ động thông qua mô phỏng MATLAB.
- Phân tích hiệu quả của hai giải pháp bảo mật vật lý (Physical Layer Security - PLS):
  - Mã hóa nhiễu nhân tạo (Artificial Noise - AN).
  - Kiểm soát công suất động (Dynamic Power Control - DPC).
- Đề xuất hướng nghiên cứu tương lai dựa trên kết quả mô phỏng.

### 1.3. Phạm vi nghiên cứu
- Tập trung vào mạng NOMA trong môi trường 5G với kịch bản nghe lén chủ động.
- Sử dụng mô phỏng MATLAB để đánh giá các chỉ số bảo mật: tỷ lệ bí mật (Secrecy Rate), xác suất rò rỉ thông tin (Secrecy Outage Probability - SOP), và hiệu suất phổ bí mật (Secrecy Spectral Efficiency).
- So sánh hiệu quả của AN và DPC trong các kịch bản cụ thể.

### 1.4. Cấu trúc báo cáo
- Giới thiệu, cơ sở lý thuyết, phương pháp nghiên cứu, kết quả mô phỏng, phân tích và so sánh, kết luận và hướng nghiên cứu tương lai.

## II. Cơ sở lý thuyết

### 2.1. Tổng quan về NOMA trong mạng 5G
- Nguyên lý hoạt động: Superposition coding và SIC.
- Ưu điểm: Hiệu suất phổ cao, hỗ trợ nhiều người dùng.
- Thách thức bảo mật: Nguy cơ nghe lén do chia sẻ tài nguyên.

### 2.2. Chiến lược nghe lén chủ động
- Định nghĩa: Nghe lén chủ động bao gồm giả mạo tín hiệu, ô nhiễm định vị, và can thiệp SIC.
- Tác động: Giảm tỷ lệ bí mật, tăng SOP, làm suy giảm hiệu quả NOMA.

### 2.3. Giải pháp bảo mật vật lý
- **Mã hóa nhiễu nhân tạo (AN)**:
  - Cơ chế: Tạo nhiễu trong không gian rỗng của kênh hợp pháp để giảm SNR kẻ nghe lén.
  - Ưu điểm: Hiệu quả với Massive MIMO.
  - Hạn chế: Yêu cầu CSI chính xác, tăng độ phức tạp.
- **Kiểm soát công suất động (DPC)**:
  - Cơ chế: Tối ưu hóa công suất dựa trên CSI và QoS.
  - Ưu điểm: Linh hoạt, thích ứng với kênh thay đổi.
  - Hạn chế: Phụ thuộc vào thuật toán tối ưu hóa.

### 2.4. Chỉ số đánh giá hiệu năng
- Tỷ lệ bí mật: \( R_s = \left[ \log_2(1 + \text{SINR}_{\text{legitimate}}) - \log_2(1 + \text{SINR}_{\text{eavesdropper}}) \right]^+ \).
- Xác suất rò rỉ: \( P_{\text{SOP}} = \Pr(R_s < R_{\text{th}}) \).
- Hiệu suất phổ bí mật: \( \eta_s = \frac{R_s}{B} \).

## III. XÂY DỰNG MÔ HÌNH MÔ PHỎNG

### 3.1. Mô hình hệ thống
- Mô hình NOMA: BS phục vụ 2-4 người dùng, kẻ nghe lén chủ động can thiệp.
- Kênh truyền dẫn: Rayleigh hoặc Rician fading.
- Kịch bản: Kẻ nghe lén gần/xa BS, thực hiện ô nhiễm định vị hoặc giả mạo tín hiệu.

### 3.2. Thiết kế mô phỏng MATLAB
- **Môi trường**: MATLAB với Communication Toolbox, Optimization Toolbox.
- **Tham số**:
  - Công suất BS: 20-40 dBm.
  - SNR: -10 dB đến 20 dB.
  - Số anten: 16-64 (Massive MIMO).
  - Băng thông: 10 MHz.
- **Các bước**:
  1. Mô phỏng baseline (không AN/DPC).
  2. Áp dụng AN và DPC riêng lẻ.
  3. Tính toán \( R_s \), \( P_{\text{SOP}} \), \( \eta_s \).

### 3.3. Phân tích và so sánh
- So sánh \( R_s \), \( P_{\text{SOP}} \), \( \eta_s \) giữa baseline, AN, và DPC.
- Đánh giá tác động của CSI, công suất nhiễu, và vị trí kẻ nghe lén.

## IV. KẾT QUẢ MÔ PHỎNG VÀ PHÂN TÍCH

### 4.1. Kết quả mô phỏng
- Baseline: \( R_s \) thấp, \( P_{\text{SOP}} \) cao (>20%).
- AN: \( R_s \) tăng 15-20%, \( P_{\text{SOP}} \) giảm (<10%).
- DPC: \( R_s \) tăng 10-15%, \( P_{\text{SOP}} \) giảm (<15%).

### 4.2. Phân tích
- AN hiệu quả hơn trong kịch bản kẻ nghe lén gần BS.
- DPC phù hợp với kênh thay đổi nhanh.
- Hạn chế: Độ phức tạp và yêu cầu CSI.

## V. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Kết luận
- Xác định giải pháp hiệu quả nhất trong từng kịch bản nghe lén chủ động.
- Nhấn mạnh vai trò của mô phỏng MATLAB trong đánh giá bảo mật.

### 5.2. Hướng nghiên cứu tương lai
- Kết hợp AN với DPC hoặc tích hợp Beamforming/RIS.
- Tối ưu hóa bằng học máy.
- Nghiên cứu trong môi trường thực tế hơn.

## VI. Tài liệu tham khảo
[1]V. N. Vo et al., "Secondary Network Throughput Optimization of NOMA Cognitive Radio Networks Under Power and Secure Constraints," in IEEE Access, vol. 11, pp. 33826-33838, 2023, doi: 10.1109/ACCESS.2023.3263579.
[2] Tung Pham Huu, Van Vo Nhan, Hung Tran, Truong Quach Xuan and Viet Nguyen Dinh, "Proactive Eavesdropping via Jamming in NOMA Network", IEEE Access, vol. 9, pp.168121-168133, 2021
[3]NOMA and massive MIMO assisted physical layer security using artificial noise precoding
[4]Physical layer security methods against eavesdropping on the far user by the near user in NOMA networks – A comparison
[5]Secure Downlink Transmission Strategies against Active Eavesdropping in NOMA Systems: A Zero-Sum Game Approach
[6]Statistical-based detection of pilot contamination attack for NOMA in 5G networks
[7]Improving Physical Layer Security for Reconfigurable Intelligent Surface aided NOMA 6G Networks
[8]Design in Power-Domain NOMA: Eavesdropping Suppression in the Two-User Relay Network with Compensation for the Relay User
[9]Non-Orthogonal Multiple Access Techniques in Emerging Wireless Systems
[10]Non-Orthogonal Multiple Access - an overview