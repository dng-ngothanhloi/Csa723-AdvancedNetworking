# Phân tích và đánh giá tham số bảo mật mạng NOMA

## 1. Phân tích dữ liệu từ kịch bản 2 (Eve_Change_SNR-Final.txt)

Kịch bản 2 tập trung vào việc thay đổi SNR của Eve (SNR_Eve) trong khi giữ SNR của Bob cố định ở các mức từ 0 dB đến 20 dB. Các tham số bảo mật chính được phân tích bao gồm:

- **SOP (Secrecy Outage Probability)**: Xác suất gián đoạn bảo mật, phản ánh khả năng Eve giải mã được thông tin bí mật của Bob.
- **R_s (Secrecy Rate)**: Dung lượng bí mật, biểu thị tốc độ truyền thông tin an toàn.
- **IP (Intercept Probability)**: Xác suất Eve chặn được tín hiệu.
- **eta_s**: Hiệu suất bảo mật, thường được định nghĩa là tỷ số giữa dung lượng bí mật và công suất tiêu thụ.

### Quan sát chính:

1. **SOP1 và SOP2**:
   - SOP1 (cho Bob1) tăng dần khi SNR_Eve tăng, đạt giá trị gần 1 (100%) khi SNR_Eve ≥ 10 dB ở hầu hết các mức SNR_Bob. Điều này cho thấy Eve có khả năng giải mã tín hiệu của Bob1 khi SNR_Eve tăng, làm giảm tính bảo mật.
   - SOP2 (cho Bob2) luôn bằng 1, cho thấy tín hiệu của Bob2 dễ bị Eve giải mã trong mọi trường hợp. Điều này có thể do phân bổ công suất không tối ưu (alpha2 = 0.889 lớn hơn nhiều so với alpha1 = 0.111), khiến tín hiệu của Bob2 mạnh hơn và dễ bị Eve chặn.

2. **R_s1 và R_s2**:
   - R_s1 (dung lượng bí mật của Bob1) giảm dần khi SNR_Eve tăng, từ khoảng 0.72 (SNR_Bob = 4 dB, SNR_Eve = 0 dB) xuống 0 khi SNR_Bob ≥ 14 dB. Điều này cho thấy khi Eve có SNR cao hơn, dung lượng bí mật của Bob1 giảm mạnh.
   - R_s2 (dung lượng bí mật của Bob2) luôn bằng 0, phản ánh rằng tín hiệu của Bob2 không có bảo mật trong kịch bản này.

3. **IP1 và IP2**:
   - IP1 (xác suất chặn của Bob1) tăng khi SNR_Eve tăng, đạt giá trị cao (gần 1) khi SNR_Bob ≥ 14 dB và SNR_Eve ≥ 10 dB. Điều này cho thấy Eve có khả năng chặn tín hiệu của Bob1 khi chất lượng kênh của Eve tốt hơn.
   - IP2 (xác suất chặn của Bob2) luôn bằng 1, cho thấy tín hiệu của Bob2 luôn bị Eve chặn.

4. **eta_s1 và eta_s2**:
   - Hiệu suất bảo mật eta_s1 giảm khi SNR_Eve tăng, từ khoảng 7.24e-08 (SNR_Bob = 2 dB, SNR_Eve = 0 dB) xuống 0 khi SNR_Bob ≥ 18 dB. Điều này cho thấy hiệu suất bảo mật của Bob1 giảm mạnh khi Eve có SNR cao.
   - eta_s2 rất thấp (thấp hơn eta_s1) và gần như không thay đổi, phản ánh hiệu suất bảo mật kém của Bob2.

5. **Dung lượng kênh (C_B1, C_B2, C_E)**:
   - Dung lượng kênh của Bob1 (C_B1) giảm khi SNR_Eve tăng, từ 36.62 Mbps (SNR_Bob = 20 dB, SNR_Eve = 0 dB) xuống 10.51 Mbps (SNR_Bob = 0 dB, SNR_Eve = 20 dB).
   - Dung lượng kênh của Bob2 (C_B2) tăng khi SNR_Bob tăng, đạt đỉnh 75.01 Mbps (SNR_Bob = 20 dB, SNR_Eve = 0 dB), nhưng không bị ảnh hưởng nhiều bởi SNR_Eve.
   - Dung lượng kênh của Eve (C_E) tăng đáng kể khi SNR_Bob và SNR_Eve tăng, đạt tối đa 89.47 Mbps (SNR_Bob = 20 dB, SNR_Eve = 20 dB), cho thấy Eve tận dụng được tín hiệu mạnh hơn.

6. **BER (Bit Error Rate)**:
   - BER của cả Bob1, Bob2 và Eve dao động quanh 0.5, cho thấy hiệu suất giải mã tín hiệu không được cải thiện đáng kể trong kịch bản này. Điều này có thể do nhiễu từ Eve hoặc lỗi SIC (Successive Interference Cancellation) với tỷ lệ epsilon = 0.01.

### Đánh giá:
- Hệ thống NOMA trong kịch bản 2 có hiệu suất bảo mật thấp, đặc biệt đối với Bob2 (SOP2 = 1, R_s2 = 0, IP2 = 1). Điều này cho thấy phân bổ công suất hiện tại (alpha1 = 0.111, alpha2 = 0.889) không hiệu quả trong việc bảo vệ tín hiệu của Bob2 trước Eve.
- Bob1 có hiệu suất bảo mật tốt hơn Bob2 ở các mức SNR_Bob thấp (0-4 dB), nhưng khi SNR_Eve tăng, bảo mật của Bob1 cũng suy giảm nghiêm trọng.
- Nhiễu chủ động từ Eve (với công suất nhiễu pilot = 0.2) làm giảm đáng kể dung lượng bí mật và tăng xác suất gián đoạn bảo mật.

---

## 2. Phân tích dữ liệu từ kịch bản 3 (Eve_Change_dE-Final.txt)

Kịch bản 3 thay đổi khoảng cách của Eve (d_E) từ 20 m đến 150 m, với SNR_Bob cố định ở 20 dB và SNR_Eve cố định ở 30 dB.

### Quan sát chính:

1. **SOP1 và SOP2**:
   - SOP1 = 1 trong toàn bộ khoảng d_E, cho thấy tín hiệu của Bob1 luôn bị Eve giải mã, bất kể khoảng cách.
   - SOP2 = 0 trong toàn bộ khoảng d_E, cho thấy tín hiệu của Bob2 có bảo mật hoàn hảo. Điều này trái ngược hoàn toàn với kịch bản 2, có thể do SNR_Eve cao (30 dB) và phân bổ công suất ưu tiên Bob2 (alpha2 = 0.889).

2. **R_s1 và R_s2**:
   - R_s1 = 0 trong toàn bộ khoảng d_E, cho thấy không có dung lượng bí mật cho Bob1.
   - R_s2 tăng từ 14.94 (d_E = 20 m) đến 20.32 (d_E = 90 m) rồi giảm xuống 16.46 (d_E = 150 m). Điều này cho thấy dung lượng bí mật của Bob2 cải thiện khi Eve ở gần (d_E nhỏ), nhưng giảm khi Eve ở xa hơn.

3. **IP1 và IP2**:
   - IP1 = 1 trong toàn bộ khoảng d_E, cho thấy Eve luôn chặn được tín hiệu của Bob1.
   - IP2 = 0 trong toàn bộ khoảng d_E, cho thấy tín hiệu của Bob2 không bị Eve chặn.

4. **eta_s1 và eta_s2**:
   - eta_s1 = 0 trong toàn bộ khoảng d_E, phản ánh hiệu suất bảo mật của Bob1 bằng 0.
   - eta_s2 tăng từ 1.49e-06 (d_E = 20 m) đến 2.03e-06 (d_E = 90 m) rồi giảm xuống 1.65e-06 (d_E = 150 m), cho thấy hiệu suất bảo mật của Bob2 tốt hơn khi Eve ở khoảng cách trung bình (90 m).

5. **Dung lượng kênh (C_B1, C_B2, C_E)**:
   - C_B1 ổn định ở mức 37.55 Mbps, ngoại trừ tại d_E = 50 m (0.01 Mbps, có thể là lỗi dữ liệu hoặc điều kiện đặc biệt).
   - C_B2 dao động từ 198.18 Mbps (d_E = 100 m) đến 337.38 Mbps (d_E = 20 m), cho thấy hiệu suất kênh của Bob2 giảm khi Eve ở xa hơn.
   - C_E giảm từ 187.97 Mbps (d_E = 20 m) xuống 152.42 Mbps (d_E = 70 m) rồi tăng nhẹ lên 185.15 Mbps (d_E = 150 m), phản ánh ảnh hưởng của khoảng cách đến khả năng giải mã của Eve.

6. **BER**:
   - BER của Bob1, Bob2 và Eve dao động quanh 0.5, tương tự kịch bản 2, cho thấy hiệu suất giải mã không cải thiện đáng kể.

### Đánh giá:
- Trong kịch bản 3, Bob2 có hiệu suất bảo mật vượt trội (SOP2 = 0, IP2 = 0, R_s2 > 0), trong khi Bob1 không có bảo mật (SOP1 = 1, IP1 = 1, R_s1 = 0). Điều này cho thấy phân bổ công suất hiện tại ưu tiên bảo mật cho Bob2 khi SNR_Eve cao (30 dB).
- Khoảng cách của Eve (d_E) ảnh hưởng đáng kể đến dung lượng bí mật của Bob2, với hiệu suất tốt nhất ở d_E = 90 m.
- Nhiễu chủ động từ Eve (SNR_Eve = 30 dB) làm giảm bảo mật của Bob1 nhưng không ảnh hưởng đến Bob2.

---

## 3. So sánh kịch bản 2 và kịch bản 3

- **Kịch bản 2 (thay đổi SNR_Eve)**:
  - Bob2 không có bảo mật (SOP2 = 1, R_s2 = 0, IP2 = 1).
  - Bob1 có bảo mật ở các mức SNR_Bob thấp, nhưng giảm mạnh khi SNR_Eve tăng.
  - Nhiễu từ Eve làm giảm dung lượng bí mật và tăng xác suất gián đoạn bảo mật.

- **Kịch bản 3 (thay đổi d_E)**:
  - Bob2 có bảo mật hoàn hảo (SOP2 = 0, IP2 = 0, R_s2 > 0).
  - Bob1 không có bảo mật trong mọi trường hợp.
  - Khoảng cách của Eve ảnh hưởng đến dung lượng bí mật của Bob2, nhưng không ảnh hưởng đến Bob1.

- **Nguyên nhân khác biệt**:
  - Phân bổ công suất (alpha1 = 0.111, alpha2 = 0.889) ưu tiên Bob2, dẫn đến tín hiệu của Bob2 mạnh hơn và khó bị Eve giải mã hơn trong kịch bản 3.
  - SNR_Eve cao (30 dB) trong kịch bản 3 làm tăng khả năng Eve chặn tín hiệu của Bob1, nhưng không ảnh hưởng đến Bob2 do phân bổ công suất và SIC.

---

## 4. Đề xuất hướng tiếp theo: AN và DPC

Để cải thiện hiệu suất bảo mật của hệ thống NOMA, đặc biệt trong các kịch bản có Eve chủ động gây nhiễu, các phương pháp sau có thể được áp dụng:

### 4.1. Artificial Noise (AN)
- **Mục tiêu**: Sử dụng nhiễu nhân tạo để làm giảm khả năng giải mã của Eve mà không ảnh hưởng đến tín hiệu của Bob1 và Bob2.
- **Đề xuất**:
  1. **Tích hợp AN vào tín hiệu truyền**:
     - Trạm gốc (BS) có thể thêm nhiễu nhân tạo vào không gian không (null space) của kênh Bob1 và Bob2, để nhiễu chỉ ảnh hưởng đến Eve. Với 16 anten, BS có đủ bậc tự do để tạo nhiễu định hướng.
     - Công suất nhiễu nhân tạo cần được tối ưu để cân bằng giữa việc làm giảm dung lượng kênh của Eve (C_E) và duy trì dung lượng kênh của Bob1 và Bob2 (C_B1, C_B2).
  2. **Tối ưu hóa phân bổ công suất nhiễu**:
     - Hiện tại, công suất nhiễu pilot là 0.2. Có thể tăng công suất nhiễu nhân tạo và điều chỉnh phân bổ công suất giữa tín hiệu và nhiễu để giảm C_E mà không làm tăng BER của Bob1 và Bob2.
     - Sử dụng thuật toán tối ưu hóa (ví dụ: gradient descent) để tìm tỷ lệ công suất nhiễu tối ưu dựa trên SNR_Eve và d_E.
  3. **Phân tích hiệu quả**:
     - Mô phỏng hiệu suất của AN với các mức SNR_Eve và d_E khác nhau để đánh giá tác động lên SOP, R_s, và IP.
     - Đánh giá hiệu quả của AN trong việc giảm eta_s của Eve mà không làm giảm eta_s1 và eta_s2.

### 4.2. Dirty Paper Coding (DPC)
- **Mục tiêu**: Loại bỏ nhiễu liên người dùng (inter-user interference) trong NOMA, từ đó tăng dung lượng bí mật và giảm SOP.
- **Đề xuất**:
  1. **Áp dụng DPC tại BS**:
     - DPC cho phép BS mã hóa tín hiệu của Bob1 và Bob2 sao cho nhiễu liên người dùng được triệt tiêu trước khi truyền. Điều này có thể cải thiện dung lượng kênh (C_B1, C_B2) và giảm BER.
     - Với thông tin kênh hoàn hảo (CSI), DPC có thể được áp dụng để mã hóa tín hiệu của Bob2 trước, sau đó mã hóa tín hiệu của Bob1 sao cho Bob2 không bị ảnh hưởng bởi tín hiệu của Bob1.
  2. **Kết hợp DPC với AN**:
     - Kết hợp DPC với nhiễu nhân tạo để vừa triệt tiêu nhiễu liên người dùng, vừa làm giảm khả năng giải mã của Eve. AN có thể được thiết kế để tập trung vào kênh của Eve, trong khi DPC đảm bảo tín hiệu của Bob1 và Bob2 được giải mã chính xác.
  3. **Tối ưu hóa phân bổ công suất**:
     - Tái phân bổ công suất (alpha1, alpha2) để cân bằng giữa dung lượng bí mật của Bob1 và Bob2. Hiện tại, alpha2 = 0.889 ưu tiên Bob2, dẫn đến bảo mật kém cho Bob1. Có thể thử các giá trị alpha1 và alpha2 khác (ví dụ: alpha1 = 0.3, alpha2 = 0.7) để cải thiện R_s1 và giảm SOP1.
  4. **Phân tích hiệu quả**:
     - Mô phỏng hiệu suất của DPC với các mức SNR_Bob, SNR_Eve và d_E để đánh giá tác động lên R_s, SOP, và IP.
     - So sánh hiệu suất của DPC với phương pháp SIC hiện tại (epsilon = 0.01) để xác định cải thiện về BER và dung lượng bí mật.

### 4.3. Các hướng nghiên cứu bổ sung
- **Tối ưu hóa số anten**: Với 16 anten, BS có khả năng định hướng chùm tia (beamforming) để tăng cường tín hiệu cho Bob1 và Bob2, đồng thời làm giảm tín hiệu đến Eve. Có thể thử nghiệm với số anten khác nhau để đánh giá tác động lên bảo mật.
- **Mô phỏng với nhiễu không đồng nhất**: Thay vì nhiễu nền cố định (N_0 = 1.00e-15 W), có thể mô phỏng với các mức nhiễu khác nhau để đánh giá độ bền của hệ thống.
- **Ứng dụng học máy**: Sử dụng các thuật toán học máy (ví dụ: reinforcement learning) để tối ưu hóa phân bổ công suất và nhiễu nhân tạo trong thời gian thực, dựa trên thông tin kênh của Bob và Eve.

---

## 5. Kết luận
- **Kịch bản 2**: Hiệu suất bảo mật của Bob2 rất kém, trong khi Bob1 có bảo mật ở các mức SNR thấp nhưng giảm mạnh khi SNR_Eve tăng. Nhiễu từ Eve là yếu tố chính làm giảm bảo mật.
- **Kịch bản 3**: Bob2 có bảo mật tốt, nhưng Bob1 không có bảo mật. Khoảng cách của Eve ảnh hưởng đáng kể đến dung lượng bí mật của Bob2.
- **Đề xuất**: Kết hợp AN và DPC để cải thiện dung lượng bí mật và giảm SOP. Tái phân bổ công suất và tối ưu hóa nhiễu nhân tạo là các hướng tiềm năng để tăng cường bảo mật cho cả Bob1 và Bob2.