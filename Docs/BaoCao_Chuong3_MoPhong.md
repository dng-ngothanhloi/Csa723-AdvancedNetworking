# Chương 3: Xây Dựng Mô Hình Mô Phỏng

## 3.1 Giới Thiệu
Mô phỏng đóng vai trò quan trọng trong nghiên cứu hiệu năng bảo mật tầng vật lý (Physical Layer Security - PLS) của mạng NOMA (Non-Orthogonal Multiple Access). Việc sử dụng các công cụ mô phỏng, như MATLAB hoặc Python, cho phép đánh giá hiệu quả của các giải pháp bảo mật trong các kịch bản thực tế mà không cần triển khai thực tế tốn kém. Mô phỏng giúp:

- **Đánh giá hiệu năng:** Phân tích các chỉ số như dung lượng bí mật (\( C_s \)), xác suất chặn bí mật (SOP), xác suất chặn (IP), và tỷ lệ lỗi bit (BER) trong các điều kiện kênh khác nhau.
- **So sánh các giải pháp:** So sánh hiệu năng của hệ thống baseline (không có giải pháp nâng cao như nhiễu nhân tạo - AN hoặc mã hóa trước - DPC) với các giải pháp cải tiến.
- **Tối ưu hóa hệ thống:** Cung cấp dữ liệu để tối ưu hóa các tham số như phân bổ công suất, số anten, hoặc chiến lược chống nghe lén.
- **Kiểm tra tính khả thi:** Đánh giá khả năng triển khai các giải pháp bảo mật trong các hệ thống thực tế như 5G hoặc IoT.

Trong nghiên cứu này, mô phỏng được thực hiện bằng Python với thư viện NumPy và Matplotlib, sử dụng phương pháp Monte Carlo để mô phỏng kênh fading Rayleigh và đánh giá hiệu năng bảo mật trong hai kịch bản nghe lén chủ động.

## 3.2 Phân Tích Chiến Lược Nghe Lén Chủ Động

Chiến lược nghe lén chủ động (active eavesdropping) xảy ra khi kẻ nghe lén (Eve) không chỉ thu nhận tín hiệu mà còn gây nhiễu để làm suy giảm chất lượng kênh của người dùng hợp pháp (Bob1 và Bob2). Hai kịch bản mô phỏng được xây dựng để đánh giá ảnh hưởng của nghe lén chủ động trong mạng NOMA:

### 3.2.1 Kịch Bản 2: Quét SNR của Eve (\( \text{SNR}_{\text{Eve}} \))
- **Mô tả:** Trong kịch bản này, SNR của Eve (\( \text{SNR}_{\text{Eve}} \)) được thay đổi từ 0 đến 20 dB, trong khi các thông số khác được giữ cố định, bao gồm khoảng cách của Eve (\( d_E = 70 \, \text{m} \)), khoảng cách của Bob1 (\( d_{B1} = 50 \, \text{m} \)), và Bob2 (\( d_{B2} = 100 \, \text{m} \)). SNR của Bob được quét từ 0 đến 20 dB, với phân tích tập trung vào trường hợp \( \text{SNR}_{\text{Bob}} = 20 \, \text{dB} \).
- **Kết quả phân tích:**
  - **Dung lượng bí mật (\( R_{s1}, R_{s2}, R_{s,\text{sum}} \)):**
    \[
    R_{s1} = \max(0, R_1 - R_{e1}), \quad R_{s2} = \max(0, R_2 - R_{e2}), \quad R_{s,\text{sum}} = R_{s1} + R_{s2}
    \]
    Khi \( \text{SNR}_{\text{Eve}} \) tăng, \( R_{s1} \) (Bob1) và \( R_{s2} \) (Bob2) giảm do dung lượng kênh của Eve (\( R_{e1}, R_{e2} \)) tăng, làm giảm chênh lệch \( R_1 - R_{e1} \) và \( R_2 - R_{e2} \). \( R_{s1} > R_{s2} \) vì Bob1 có điều kiện kênh tốt hơn. \( R_{s,\text{sum}} \) giảm tuyến tính, cho thấy hệ thống dễ bị tổn thương khi Eve tăng công suất nhiễu.
  - **Xác suất chặn bí mật (\( \text{SOP1}, \text{SOP2} \)):**
    \[
    \text{SOP1} = P(R_{s1} < R_{\text{th}}), \quad \text{SOP2} = P(R_{s2} < R_{\text{th}})
    \]
    Với \( R_{\text{th}} = 1.0 \, \text{bits/s/Hz} \), SOP1 và SOP2 tăng khi \( \text{SNR}_{\text{Eve}} \) tăng, với SOP2 > SOP1 do Bob2 có kênh yếu hơn. Tại \( \text{SNR}_{\text{Eve}} = 20 \, \text{dB} \), SOP2 gần 1, cho thấy Bob2 mất khả năng duy trì bảo mật.
  - **Xác suất chặn (\( \text{IP1}, \text{IP2} \)):**
    \[
    \text{IP1} = P(R_{e1} \geq R_1), \quad \text{IP2} = P(R_{e2} \geq R_2)
    \]
    IP2 > IP1, đặc biệt tại \( \text{SNR}_{\text{Eve}} \) cao, do Bob2 dễ bị nghe lén hơn.
  - **Tỷ lệ lỗi bit (BER):** BER của Bob1 và Bob2 tăng nhẹ, trong khi BER của Eve giảm khi \( \text{SNR}_{\text{Eve}} \) tăng, cho thấy Eve có lợi thế giải mã.
  - **Hiệu suất phổ bí mật (\( \eta_{s1}, \eta_{s2} \)):**
    \[
    \eta_{s1} = \frac{R_{s1}}{B}, \quad \eta_{s2} = \frac{R_{s2}}{B}
    \]
    Giảm mạnh khi \( \text{SNR}_{\text{Eve}} \) tăng, với \( \eta_{s1} > \eta_{s2} \).
- **Ý nghĩa:** Kịch bản này cho thấy hệ thống NOMA baseline không hiệu quả trong việc chống lại nghe lén chủ động khi Eve có SNR cao, đặc biệt ảnh hưởng đến Bob2.

### 3.2.2 Kịch Bản 3: Quét Khoảng Cách của Eve (\( d_E \))
- **Mô tả:** Khoảng cách của Eve (\( d_E \)) được quét từ 20m đến 150m, với \( \text{SNR}_{\text{Bob}} = 20 \, \text{dB} \) và \( \text{SNR}_{\text{Eve}} = 30 \, \text{dB} \) cố định. Các thông số khác tương tự Kịch bản 2.
- **Kết quả phân tích:**
  - **Dung lượng bí mật:** \( R_{s1}, R_{s2} \) tăng khi \( d_E \) tăng, do suy hao kênh của Eve (\( d_E^\alpha \)) tăng, làm giảm \( \text{SNR}_{E1}, \text{SNR}_{E2} \). \( R_{s1} > R_{s2} \), và \( R_{s,\text{sum}} \) tăng đáng kể khi \( d_E > 100 \, \text{m} \).
  - **Xác suất chặn bí mật:** SOP1 và SOP2 giảm khi \( d_E \) tăng, với SOP2 > SOP1. Tại \( d_E = 20 \, \text{m} \), SOP2 gần 1, cho thấy Bob2 dễ bị chặn bí mật khi Eve ở gần.
  - **Xác suất chặn:** IP1 và IP2 giảm khi \( d_E \) tăng, với IP2 > IP1.
  - **Tỷ lệ lỗi bit:** BER_B1 và BER_B2 giảm nhẹ, trong khi BER_E tăng khi \( d_E \) tăng, cho thấy Eve khó giải mã hơn khi ở xa.
  - **Hiệu suất phổ bí mật:** \( \eta_{s1}, \eta_{s2} \) tăng khi \( d_E \) tăng, nhưng vẫn thấp với Bob2 khi \( d_E \) nhỏ.
- **Ý nghĩa:** Khoảng cách của Eve có tác động lớn đến hiệu năng bảo mật, với hiệu quả bảo mật tăng khi Eve ở xa trạm gốc.

### 3.2.3 Ý Nghĩa của Hai Kịch Bản
- **Kịch bản 2 (Quét SNR_Eve):** Giúp đánh giá tác động của công suất nhiễu từ Eve đến hiệu năng bảo mật. Kết quả chỉ ra rằng hệ thống NOMA baseline dễ bị tổn thương khi Eve có công suất cao, đặc biệt với người dùng xa (Bob2). Điều này nhấn mạnh sự cần thiết của các kỹ thuật như nhiễu nhân tạo (AN) hoặc mã hóa trước (DPC) để cải thiện bảo mật.
- **Kịch bản 3 (Quét \( d_E \)):** Đánh giá ảnh hưởng của vị trí địa lý của Eve. Khi Eve ở gần trạm gốc, hiệu năng bảo mật giảm mạnh, đặc biệt với Bob2. Kịch bản này cung cấp thông tin về phạm vi nguy hiểm của Eve và cần thiết phải tối ưu hóa hệ thống để chống lại nghe lén ở khoảng cách gần.
- **Tổng thể:** Hai kịch bản cung cấp cái nhìn toàn diện về hiệu năng bảo mật của hệ thống NOMA baseline, làm cơ sở để so sánh với các giải pháp cải tiến trong các bước nghiên cứu tiếp theo.

## 3.3 Tham Số Mô Hình Mô Phỏng
Các tham số mô phỏng được thiết lập dựa trên hệ thống NOMA với hai người dùng hợp pháp (Bob1, Bob2) và một kẻ nghe lén chủ động (Eve), sử dụng mô hình kênh fading Rayleigh và Massive MIMO. Các tham số chính bao gồm:

- **Công suất truyền tổng (\( P_A \)):** \( 1 \, \text{W} \) (~30 dBm).
- **Nhiễu nền (\( N_0 \)):** \( 10^{-15} \, \text{W} \).
- **Hệ số suy hao kênh (\( \alpha \)):** 3.
- **Băng thông (\( B \)):** \( 10 \, \text{MHz} \).
- **Số anten tại trạm gốc (\( N_{\text{ant}} \)):** 16 (Massive MIMO).
- **Khoảng cách:**
  - Bob1: \( d_{B1} = 50 \, \text{m} \).
  - Bob2: \( d_{B2} = 100 \, \text{m} \).
  - Eve: \( d_E = 70 \, \text{m} \) (Kịch bản 2), quét từ 20m đến 150m (Kịch bản 3).
- **Phân bổ công suất:**
  \[
  \alpha_1 = \frac{d_{B1}^\alpha}{d_{B1}^\alpha + d_{B2}^\alpha}, \quad \alpha_2 = \frac{d_{B2}^\alpha}{d_{B1}^\alpha + d_{B2}^\alpha}
  \]
  Với \( \alpha_1 + \alpha_2 = 1 \). Dựa trên \( d_{B1}, d_{B2} \), ta có \( \alpha_1 \approx 0.125 \), \( \alpha_2 \approx 0.875 \).
- **Tỷ lệ lỗi SIC (\( \epsilon \)):** 0.01.
- **Công suất nhiễu pilot:** 0.2.
- **Ngưỡng bảo mật (\( R_{\text{th}} \)):** \( 1.0 \, \text{bits/s/Hz} \).
- **Số lần mô phỏng Monte Carlo:** \( 10^4 \) (Kịch bản 2), \( 10^5 \) (Kịch bản 3).

Các tham số này được chọn để mô phỏng hệ thống NOMA thực tế, phản ánh các điều kiện kênh không dây và ảnh hưởng của nhiễu từ Eve.

## 3.4 Các Thuật Toán Mô Phỏng
Dưới đây là các thuật toán mô phỏng cho hai kịch bản, được xây dựng dựa trên mã nguồn `NOMAImprovementTwoUserFinal.py`. Các thuật toán sử dụng phương pháp Monte Carlo để mô phỏng kênh fading và tính toán các metric bảo mật.

### 3.4.1 Thuật Toán Mô Phỏng Kịch Bản 2: Quét SNR_Eve
```plaintext
BẮT ĐẦU
1. Khởi tạo tham số hệ thống:
   - Công suất truyền \( P_A = 1 \, \text{W} \), nhiễu nền \( N_0 = 10^{-15} \, \text{W} \).
   - \( \alpha = 3 \), \( B = 10 \, \text{MHz} \), \( N_{\text{ant}} = 16 \).
   - \( d_{B1} = 50 \, \text{m} \), \( d_{B2} = 100 \, \text{m} \), \( d_E = 70 \, \text{m} \).
   - \( \epsilon = 0.01 \), công suất nhiễu pilot = 0.2, \( R_{\text{th}} = 1.0 \, \text{bits/s/Hz} \).
   - Tính \( \alpha_1, \alpha_2 \) dựa trên suy hao kênh.
2. Tạo dải \( \text{SNR}_{\text{Bob}} \) từ 0 đến 20 dB và \( \text{SNR}_{\text{Eve}} \) từ 0 đến 20 dB.
3. Vòng lặp qua các giá trị \( \text{SNR}_{\text{Bob}} \):
   - Tính công suất hiệu quả \( P_{A,\text{eff}} = \text{SNR}_{\text{Bob}} \cdot d_{B1}^\alpha \cdot N_0 \).
   - Vòng lặp qua các giá trị \( \text{SNR}_{\text{Eve}} \):
     - Tính công suất nhiễu của Eve \( P_E = \text{SNR}_{\text{Eve}} \cdot d_E^\alpha \cdot N_0 \).
     - Tạo kênh fading Rayleigh cho Bob1 (\( h_{B1} \)), Bob2 (\( h_{B2} \)), Eve (\( h_E \)), và nhiễu từ Eve (\( h_{EB1}, h_{EB2} \)).
     - Thêm nhiễu pilot vào \( h_{B1}, h_{B2} \).
     - Tính khoảng cách nhiễu \( d_{EB1} = |d_E - d_{B1}| + 10^{-3} \), \( d_{EB2} = |d_E - d_{B2}| + 10^{-3} \).
     - Tính SNR:
       \[
       \text{SNR}_{B1} = \frac{P_{A,\text{eff}} \cdot \alpha_1 \cdot \|\mathbf{h}_{B1}\|^2}{d_{B1}^\alpha \cdot N_0 + \epsilon \cdot P_{A,\text{eff}} \cdot \alpha_2 \cdot \|\mathbf{h}_{B1}\|^2 + P_E \cdot \|\mathbf{h}_{EB1}\|^2 / d_{EB1}^\alpha}
       \]
       \[
       \text{SNR}_{B2} = \frac{P_{A,\text{eff}} \cdot \alpha_2 \cdot \|\mathbf{h}_{B2}\|^2}{d_{B2}^\alpha \cdot N_0 + P_E \cdot \|\mathbf{h}_{EB2}\|^2 / d_{EB2}^\alpha}
       \]
       \[
       \text{SNR}_{E1} = \frac{P_{A,\text{eff}} \cdot \alpha_1 \cdot \|\mathbf{h}_E\|^2}{d_E^\alpha \cdot N_0 + P_{A,\text{eff}} \cdot \|\mathbf{h}_E\|^2}
       \]
       \[
       \text{SNR}_{E2} = \frac{P_{A,\text{eff}} \cdot \alpha_2 \cdot \|\mathbf{h}_E\|^2}{d_E^\alpha \cdot N_0 + P_{A,\text{eff}} \cdot \|\mathbf{h}_{EB2}\|^2 / d_{EB2}^\alpha}
       \]
     - Tính dung lượng kênh: \( R_1 = \log_2(1 + \text{SNR}_{B1}) \), \( R_2 = \log_2(1 + \text{SNR}_{B2}) \), \( R_{e1} = \log_2(1 + \text{SNR}_{E1}) \), \( R_{e2} = \log_2(1 + \text{SNR}_{E2}) \).
     - Tính dung lượng bí mật: \( R_{s1} = \max(0, R_1 - R_{e1}) \), \( R_{s2} = \max(0, R_2 - R_{e2}) \), \( R_{s,\text{sum}} = R_{s1} + R_{s2} \).
     - Tính SOP: \( \text{SOP1} = P(R_{s1} < R_{\text{th}}) \), \( \text{SOP2} = P(R_{s2} < R_{\text{th}}) \).
     - Tính IP: \( \text{IP1} = P(R_{e1} \geq R_1) \), \( \text{IP2} = P(R_{e2} \geq R_2) \).
     - Tính BER (BPSK): Mô phỏng tín hiệu truyền và nhận, tính tỷ lệ lỗi bit cho Bob1, Bob2, và Eve.
     - Tính hiệu suất phổ bí mật: \( \eta_{s1} = R_{s1} / B \), \( \eta_{s2} = R_{s2} / B \).
     - Lưu kết quả trung bình qua \( 10^4 \) lần mô phỏng Monte Carlo.
4. Vẽ biểu đồ: \( R_{s1}, R_{s2}, R_{s,\text{sum}} \), SOP, IP, BER, và \( \eta_{s1}, \eta_{s2} \) theo \( \text{SNR}_{\text{Eve}} \) tại \( \text{SNR}_{\text{Bob}} = 20 \, \text{dB} \).
5. Lưu kết quả vào tệp `simulation_results_snr.npy`.
KẾT THÚC
```

### 3.4.2 Thuật Toán Mô Phỏng Kịch Bản 3: Quét \( d_E \)
```plaintext
BẮT ĐẦU
1. Khởi tạo tham số hệ thống:
   - Công suất truyền \( P_A = 1 \, \text{W} \), nhiễu nền \( N_0 = 10^{-15} \, \text{W} \).
   - \( \alpha = 3 \), \( B = 10 \, \text{MHz} \), \( N_{\text{ant}} = 16 \).
   - \( d_{B1} = 50 \, \text{m} \), \( d_{B2} = 100 \, \text{m} \).
   - \( \epsilon = 0.01 \), công suất nhiễu pilot = 0.2, \( R_{\text{th}} = 1.0 \, \text{bits/s/Hz} \).
   - \( \text{SNR}_{\text{Bob}} = 20 \, \text{dB} \), \( \text{SNR}_{\text{Eve}} = 30 \, \text{dB} \).
   - Tính \( \alpha_1, \alpha_2 \) dựa trên suy hao kênh.
2. Tạo dải \( d_E \) từ 20m đến 150m (bước 10m).
3. Vòng lặp qua các giá trị \( d_E \):
   - Tính công suất hiệu quả \( P_{A,\text{eff}} = \text{SNR}_{\text{Bob}} \cdot d_{B1}^\alpha \cdot N_0 \).
   - Tính công suất nhiễu của Eve \( P_E = \text{SNR}_{\text{Eve}} \cdot d_E^\alpha \cdot N_0 \).
   - Tạo kênh fading Rayleigh cho Bob1 (\( h_{B1} \)), Bob2 (\( h_{B2} \)), Eve (\( h_E \)), và nhiễu từ Eve (\( h_{EB1}, h_{EB2} \)).
   - Thêm nhiễu pilot vào \( h_{B1}, h_{B2} \).
   - Tính khoảng cách nhiễu \( d_{EB1} = |d_E - d_{B1}| + 10^{-3} \), \( d_{EB2} = \max(|d_E - d_{B2}|, 1) \).
   - Tính SNR:
     \[
     \text{SNR}_{B1} = \frac{P_{A,\text{eff}} \cdot \alpha_1 \cdot \|\mathbf{h}_{B1}\|^2}{d_{B1}^\alpha \cdot N_0 + \epsilon \cdot P_{A,\text{eff}} \cdot \alpha_2 \cdot \|\mathbf{h}_{B1}\|^2 + P_E \cdot \|\mathbf{h}_{EB1}\|^2 / d_{EB1}^\alpha}
     \]
     \[
     \text{SNR}_{B2} = \frac{P_{A,\text{eff}} \cdot \alpha_2 \cdot \|\mathbf{h}_{B2}\|^2}{d_{B2}^\alpha \cdot N_0 + P_E \cdot \|\mathbf{h}_{EB2}\|^2 / d_{EB2}^\alpha}
     \]
     \[
     \text{SNR}_{E1} = \frac{P_{A,\text{eff}} \cdot \alpha_1 \cdot \|\mathbf{h}_E\|^2}{d_E^\alpha \cdot N_0 + P_{A,\text{eff}} \cdot \|\mathbf{h}_E\|^2}
     \]
     \[
     \text{SNR}_{E2} = \frac{P_{A,\text{eff}} \cdot \alpha_2 \cdot \|\mathbf{h}_E\|^2}{d_E^\alpha \cdot N_0 + P_{A,\text{eff}} \cdot \|\mathbf{h}_{EB2}\|^2 / d_{EB2}^\alpha}
     \]
   - Tính dung lượng kênh: \( R_1 = \log_2(1 + \text{SNR}_{B1}) \), \( R_2 = \log_2(1 + \text{SNR}_{B2}) \), \( R_{e1} = \log_2(1 + \text{SNR}_{E1}) \), \( R_{e2} = \log_2(1 + \text{SNR}_{E2}) \).
   - Tính dung lượng bí mật: \( R_{s1} = \max(0, R_1 - R_{e1}) \), \( R_{s2} = \max(0, R_2 - R_{e2}) \), \( R_{s,\text{sum}} = R_{s1} + R_{s2} \).
   - Tính SOP: \( \text{SOP1} = P(R_{s1} < R_{\text{th}}) \), \( \text{SOP2} = P(R_{s2} < R_{\text{th}}) \).
   - Tính IP: \( \text{IP1} = P(R_{e1} \geq R_1) \), \( \text{IP2} = P(R_{e2} \geq R_2) \).
   - Tính BER (BPSK): Mô phỏng tín hiệu truyền và nhận, tính tỷ lệ lỗi bit cho Bob1, Bob2, và Eve.
   - Tính hiệu suất phổ bí mật: \( \eta_{s1} = R_{s1} / B \), \( \eta_{s2} = R_{s2} / B \).
   - Lưu kết quả trung bình qua \( 10^5 \) lần mô phỏng Monte Carlo.
4. Vẽ biểu đồ: \( R_{s1}, R_{s2}, R_{s,\text{sum}} \), SOP, IP, BER, và \( \eta_{s1}, \eta_{s2} \) theo \( d_E \).
5. Lưu kết quả vào tệp `simulation_results_de.npy`.
KẾT THÚC
```