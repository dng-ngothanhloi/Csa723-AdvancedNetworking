# Trình tự nghiên cứu mô hình, tham số mô hình, giải thuật, giải pháp triển khai: Đánh giá hiệu năng Các Giải Pháp Bảo Mật mạng NOMA có chiến lược chủ động nghe lén dựa trên mô phỏng MATLAB

## I. Trình tự nghiên cứu

### 1.1. Bước 1: Mô phỏng baseline (không có giải pháp AN hoặc DPC)
- **Mục đích**: Thiết lập mô hình cơ bản để đo lường hiệu năng bảo mật khi không áp dụng giải pháp.
- **Thực hiện**:
  - Xây dựng mô hình NOMA với SIC.
  - Mô phỏng chiến lược nghe lén chủ động (giả mạo tín hiệu, ô nhiễm định vị).
  - Tính toán \( R_s = \left[ \log_2(1 + \text{SINR}_{\text{legitimate}}) - \log_2(1 + \text{SINR}_{\text{eavesdropper}}) \right]^+ \), \( P_{\text{SOP}} = \Pr(R_s < R_{\text{th}}) \), \( \eta_s = \frac{R_s}{B} \).

### 1.2. Bước 2: Mô phỏng với giải pháp AN và DPC
- **Mục đích**: Đánh giá hiệu quả của từng giải pháp trong việc cải thiện bảo mật.
- **Thực hiện**:
  - Áp dụng AN: Thêm nhiễu nhân tạo trong không gian rỗng.
  - Áp dụng DPC: Tối ưu hóa công suất bằng thuật toán.
  - Tính toán lại \( R_s \), \( P_{\text{SOP}} \), \( \eta_s \).

### 1.3. Bước 3: So sánh và đánh giá
- **Mục đích**: So sánh hiệu quả giữa baseline, AN, và DPC.
- **Thực hiện**:
  - Vẽ biểu đồ so sánh \( R_s \), \( P_{\text{SOP}} \), \( \eta_s \).
  - Phân tích ưu điểm, hạn chế, và đề xuất cải tiến.

## II. Mô hình và tham số mô hình

### 2.1. Mô hình hệ thống
- **Mô hình NOMA**: BS với 2-4 người dùng, sử dụng SIC.
- **Kênh truyền dẫn**: Rayleigh fading (hoặc Rician fading).
- **Kẻ nghe lén**: Vị trí gần/xa BS, thực hiện ô nhiễm định vị hoặc giả mạo tín hiệu.

### 2.2. Tham số mô hình
- Công suất BS: 20-40 dBm.
- SNR: -10 dB đến 20 dB.
- Số anten: 16-64 (Massive MIMO).
- Băng thông: 10 MHz.
- Ngưỡng \( R_{\text{th}} \): 0.5-2 bit/s/Hz.
- Khoảng cách: 10-100m (người dùng và kẻ nghe lén).

## III. Giải thuật và giải pháp triển khai

### 3.1. Giải thuật cho AN
- **Mô tả**: Tạo nhiễu nhân tạo trong không gian rỗng của kênh hợp pháp.
- **Bước triển khai**:
  1. Phân tích SVD để xác định không gian rỗng (sử dụng `svd` trong MATLAB).
  2. Tạo nhiễu với công suất \( 0.1 \cdot P_{\text{BS}} \) đến \( 0.3 \cdot P_{\text{BS}} \).
  3. Cập nhật \( \text{SINR}_{\text{eavesdropper}} \).
- **Công cụ**: MATLAB (hàm `randn`, `svd`).

### 3.2. Giải thuật cho DPC
- **Mô tả**: Tối ưu hóa công suất dựa trên CSI và QoS.
- **Bước triển khai**:
  1. Thu thập CSI từ kênh hợp pháp.
  2. Sử dụng thuật toán tối ưu hóa lồi (CVX toolbox).
  3. Phân bổ công suất \( P_i \) cho từng người dùng với \( \sum P_i \leq P_{\text{BS}} \).
- **Công cụ**: MATLAB với CVX.

### 3.3. Giải pháp triển khai trong MATLAB
- **Khởi tạo**:
  ```matlab
  P_BS = 30; SNR_range = -10:2:20; N_users = 2; N_ant = 16;
  h_leg = sqrt(1/2)*(randn(N_users,N_ant)+1j*randn(N_users,N_ant));
  h_eve = sqrt(1/2)*(randn(1,N_ant)+1j*randn(1,N_ant));
  ```
- **Tính \( \text{SINR} \) và \( R_s \)**:
  ```matlab
  SINR_leg = ...; SINR_eve = ...;
  R_s = max(0, log2(1 + SINR_leg) - log2(1 + SINR_eve));
  ```
- **Áp dụng AN**:
  ```matlab
  [U,~,~] = svd(h_leg); noise = U(:,N_users+1:end)*sqrt(0.2*P_BS)*randn;
  ```
- **Áp dụng DPC**:
  ```matlab
  cvx_begin; variable P(N_users); maximize(sum(log2(1 + SINR_leg)));
  subject to sum(P) <= P_BS; P >= 0; cvx_end
  ```
- **Vẽ biểu đồ**:
  ```matlab
  plot(SNR_range, R_s_baseline, 'b-', SNR_range, R_s_AN, 'r-', SNR_range, R_s_DPC, 'g-');
  legend('Baseline', 'AN', 'DPC');
  ```

## IV. Kết quả mong đợi
- Baseline: \( R_s \) thấp, \( P_{\text{SOP}} \) cao.
- AN: Tăng \( R_s \) 15-20%, giảm \( P_{\text{SOP}} \) <10%.
- DPC: Tăng \( R_s \) 10-15%, giảm \( P_{\text{SOP}} \) <15%.
- So sánh: AN vượt trội trong kịch bản kẻ nghe lén mạnh, DPC hiệu quả trong kênh động.