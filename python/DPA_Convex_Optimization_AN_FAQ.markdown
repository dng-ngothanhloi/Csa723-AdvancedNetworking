# Trả lời các câu hỏi liên quan đến phân bổ công suất động (DPA) và nhiễu nhân tạo (AN) trong hệ thống NOMA

## 1. Kết luận: Convex Optimization điều chỉnh \(\phi\) cùng với \(\alpha_1\), \(\alpha_2\)

**Đúng**: Convex Optimization là một phương pháp hiệu quả để điều chỉnh đồng thời \(\phi\) (tỷ lệ công suất dành cho nhiễu nhân tạo - AN) và các hệ số công suất \(\alpha_1\), \(\alpha_2\) trong hệ thống NOMA nhằm tối ưu hóa mục tiêu như \(\min(R_{s1}, R_{s2})\).

### Ưu điểm
- **Đảm bảo nghiệm tối ưu toàn cục nếu bài toán lồi**: Khi hàm mục tiêu (ví dụ: \(\min(R_{s1}, R_{s2})\)) và các ràng buộc (\(\alpha_1 + \alpha_2 + \phi = 1\), \(\alpha_1, \alpha_2, \phi \geq 0\)) được định dạng dưới dạng lồi, các công cụ như CVX hoặc MOSEK có thể tìm ra nghiệm tối ưu toàn cục.
- **Tính linh hoạt**: Có thể tích hợp các chỉ số bảo mật khác như SOP, IP, hoặc \(\eta_{s_i}\) vào hàm mục tiêu.
- **Khả năng xử lý đa biến**: Có thể tối ưu hóa đồng thời \(\alpha_1\), \(\alpha_2\), và \(\phi\) dựa trên thông tin trạng thái kênh (CSI).

### Lưu ý
- Để đảm bảo bài toán lồi, hàm mục tiêu có thể cần được xấp xỉ hoặc chuyển đổi (ví dụ: sử dụng log hoặc các biến đổi lồi).
- Yêu cầu CSI chính xác của Bob1, Bob2 và, trong một số trường hợp, của Eve để tính toán chính xác \(R_{s_i}\).

## 2. Đồng ý: Quét \(d_E\), SNR_Bob, SNR_Eve phù hợp với kịch bản 2 và 3 trong NOMAImprovementTwoUserFinal_fixed.py

**Đúng**: Việc quét các tham số \(d_E\), SNR_Bob, SNR_Eve trong các kịch bản 2 và 3 của mã `NOMAImprovementTwoUserFinal_fixed.py` là cơ sở phù hợp để tích hợp DPA. Cụ thể:
- **Kịch bản 2 (Eve_Change_dE-AN_Pilot-With-Phi.txt)**: Quét khoảng cách của Eve (\(d_E\) từ 20m đến 150m) với \(\phi = 0.3\), SNR_Bob = 20 dB, SNR_Eve = 30 dB. Điều này giúp đánh giá tác động của vị trí Eve đến các chỉ số bảo mật (\(R_{s_i}\), SOP, IP, \(\eta_{s_i}\)).
- **Kịch bản 3 (Eve_Change_SNR-AN_Pilot-With-Phi.txt)**: Quét SNR_Bob và SNR_Eve từ 0 dB đến 20 dB với \(\phi = 0.2\). Điều này mô phỏng các điều kiện kênh khác nhau, đặc biệt khi Eve có kênh tốt (SNR cao).
- **Tích hợp DPA**: Các kịch bản này cung cấp dữ liệu để phát triển thuật toán DPA, vì \(\alpha_1\), \(\alpha_2\) có thể được điều chỉnh dựa trên các giá trị \(d_E\), SNR_Bob, SNR_Eve để tối ưu hóa \(\min(R_{s1}, R_{s2})\).

### Cách tích hợp DPA
- Sử dụng kết quả từ các kịch bản để xây dựng mô hình tối ưu hóa, trong đó \(\alpha_1\), \(\alpha_2\), và \(\phi\) được điều chỉnh dựa trên các giá trị \(d_E\), SNR_Bob, SNR_Eve.
- Áp dụng Convex Optimization để tìm nghiệm tối ưu cho mỗi bộ tham số \(d_E\), SNR_Bob, SNR_Eve, từ đó tạo bảng tra cứu (lookup table) hoặc mô hình học máy để áp dụng trong thời gian thực.

## 3. Bổ sung CSI trong môi trường mô phỏng để xử lý DPA

**Có thể bổ sung CSI trong môi trường mô phỏng** để hỗ trợ DPA, đặc biệt khi sử dụng Convex Optimization, vì phương pháp này yêu cầu thông tin CSI chính xác của Bob1, Bob2 (và lý tưởng nhất là của Eve) để tính toán các chỉ số như SINR, \(C_{B_i}\), \(C_E\), và \(R_{s_i}\).

### Cách bổ sung CSI trong mô phỏng
1. **Mô hình hóa CSI**:
   - CSI được biểu diễn thông qua hệ số kênh \(|h_{B1}|^2\), \(|h_{B2}|^2\), và \(|h_E|^2\), được tính dựa trên mô hình suy hao kênh:
     \[
     |h_i|^2 = d_i^{-\alpha}, \quad i \in \{B1, B2, E\}
     \]
     Trong đó \(d_i\) là khoảng cách (ví dụ: \(d_{B1} = 30\)m, \(d_{B2} = 70\)m, \(d_E\) từ 20m đến 150m), \(\alpha = 3\) là hệ số suy hao kênh.
   - Trong mô phỏng, CSI có thể được tạo ngẫu nhiên bằng cách thêm nhiễu Gaussian để mô phỏng sai số thực tế:
     \[
     h_i = \sqrt{d_i^{-\alpha}} \cdot (1 + \sigma \cdot \mathcal{N}(0, 1))
     \]
     Với \(\sigma\) là độ lệch chuẩn của nhiễu CSI.

2. **Tích hợp CSI vào DPA**:
   - **Thu thập CSI**: Trong mô phỏng, giả định BS nhận được CSI từ Bob1, Bob2 qua tín hiệu pilot. CSI của Eve có thể được giả định (trường hợp xấu nhất) hoặc ước lượng dựa trên mô hình thống kê.
   - **Tính toán SINR**: Sử dụng CSI để tính SINR cho Bob1, Bob2, và Eve:
     \[
     \text{SINR}_{B1} = \frac{P_A \alpha_1 |h_{B1}|^2}{P_A \alpha_2 |h_{B1}|^2 \epsilon + N_0 + \phi P_A |h_{B1}|^2}
     \]
     \[
     \text{SINR}_{B2} = \frac{P_A \alpha_2 |h_{B2}|^2}{N_0 + \phi P_A |h_{B2}|^2}
     \]
     \[
     \text{SINR}_E = \frac{P_A \alpha_i |h_E|^2}{N_0 + \phi P_A |h_E|^2}
     \]
   - **Tối ưu hóa**: Sử dụng Convex Optimization để tìm \(\alpha_1\), \(\alpha_2\), và \(\phi\) tối ưu dựa trên CSI:
     \[
     \max_{\alpha_1, \alpha_2, \phi} \min(R_{s1}, R_{s2}) \quad \text{s.t.} \quad \alpha_1 + \alpha_2 + \phi = 1, \quad \alpha_1, \alpha_2, \phi \geq 0
     \]

3. **Thực hiện trong mô phỏng**:
   - Trong mã như `NOMAImprovementTwoUserFinal_fixed.py`, CSI của Bob1, Bob2 đã được mô phỏng qua \(d_{B1}\), \(d_{B2}\). Có thể bổ sung:
     - Mô phỏng CSI của Eve bằng cách quét \(d_E\) hoặc thêm nhiễu vào \(|h_E|^2\).
     - Tích hợp Convex Optimization (sử dụng thư viện như CVXPY trong Python) để điều chỉnh \(\alpha_1\), \(\alpha_2\), \(\phi\) dựa trên CSI.
   - Ví dụ mã bổ sung CSI:
     ```python
     import numpy as np
     import cvxpy as cp

     # Tham số
     P_A = 1.0  # Công suất truyền
     N_0 = 1e-15  # Nhiễu nền
     B = 10e6  # Băng thông
     alpha = 3  # Hệ số suy hao
     epsilon = 0.005  # Lỗi SIC
     d_B1, d_B2, d_E = 30, 70, 50  # Khoảng cách
     sigma_csi = 0.1  # Nhiễu CSI

     # Tính CSI với nhiễu
     h_B1 = np.sqrt(d_B1**(-alpha) * (1 + sigma_csi * np.random.randn()))
     h_B2 = np.sqrt(d_B2**(-alpha) * (1 + sigma_csi * np.random.randn()))
     h_E = np.sqrt(d_E**(-alpha) * (1 + sigma_csi * np.random.randn()))

     # Tối ưu hóa Convex
     alpha_1 = cp.Variable()
     alpha_2 = cp.Variable()
     phi = cp.Variable()
     SINR_B1 = (P_A * alpha_1 * h_B1**2) / (P_A * alpha_2 * h_B1**2 * epsilon + N_0 + phi * P_A * h_B1**2)
     SINR_B2 = (P_A * alpha_2 * h_B2**2) / (N_0 + phi * P_A * h_B2**2)
     C_B1 = B * cp.log(1 + SINR_B1) / np.log(2)
     C_B2 = B * cp.log(1 + SINR_B2) / np.log(2)
     C_E = B * cp.log(1 + (P_A * alpha_1 * h_E**2) / (N_0 + phi * P_A * h_E**2)) / np.log(2)
     R_s1 = cp.maximum(C_B1 - C_E, 0)
     R_s2 = cp.maximum(C_B2 - C_E, 0)
     objective = cp.Maximize(cp.minimum(R_s1, R_s2))
     constraints = [alpha_1 + alpha_2 + phi == 1, alpha_1 >= 0, alpha_2 >= 0, phi >= 0]
     problem = cp.Problem(objective, constraints)
     problem.solve()
     print(f"Optimal alpha_1: {alpha_1.value}, alpha_2: {alpha_2.value}, phi: {phi.value}")
     ```

## 4. Kiểm tra mã NOMAImprovementTwoUserFinal_fixed.py: SNR có được thay bằng SINR khi áp dụng AN?

Để xác minh liệu mã `NOMAImprovementTwoUserFinal_fixed.py` có thay SNR bằng SINR (bao gồm ảnh hưởng của \(\phi\)) khi áp dụng AN hay không, cần kiểm tra cách tính toán dung lượng kênh (\(C_{B1}\), \(C_{B2}\), \(C_E\)) trong mã.

### Phân tích
- Trong hệ thống NOMA với AN, SINR phải bao gồm ảnh hưởng của nhiễu nhân tạo (\(\phi\)). Công thức SINR đúng như sau:
  \[
  \text{SINR}_{B1} = \frac{P_A \alpha_1 |h_{B1}|^2}{P_A \alpha_2 |h_{B1}|^2 \epsilon + N_0 + \phi P_A |h_{B1}|^2}
  \]
  \[
  \text{SINR}_{B2} = \frac{P_A \alpha_2 |h_{B2}|^2}{N_0 + \phi P_A |h_{B2}|^2}
  \]
  \[
  \text{SINR}_E = \frac{P_A \alpha_i |h_E|^2}{N_0 + \phi P_A |h_E|^2}, \quad i \in \{1, 2\}
  \]
- Dung lượng kênh được tính bằng:
  \[
  C_i = B \log_2(1 + \text{SINR}_i), \quad i \in \{B1, B2, E\}
  \]

### Kiểm tra mã
Giả sử mã `NOMAImprovementTwoUserFinal_fixed.py` được viết dựa trên các công thức trên, cần kiểm tra:
1. **Tính toán SINR**: Xác minh liệu các công thức SINR có bao gồm thành phần \(\phi P_A |h_i|^2\) trong mẫu số hay không.
2. **Áp dụng \(\phi\)**: Kiểm tra xem \(\phi\) (ví dụ: \(\phi = 0.3\) hoặc \(\phi = 0.2\)) được sử dụng trong các công thức SINR hay chỉ sử dụng SNR (không có nhiễu nhân tạo).

**Dự đoán**: Dựa trên mô tả của kịch bản 2 và 3 (có sử dụng \(\phi = 0.3\) và \(\phi = 0.2\)), mã có khả năng đã thay SNR bằng SINR, vì các file đầu ra (`Eve_Change_dE-AN_Pilot-With-Phi.txt`, `Eve_Change_SNR-AN_Pilot-With-Phi.txt`) cho thấy nhiễu nhân tạo được áp dụng. Cụ thể:
- Dung lượng kênh của Eve (\(C_E\)) giảm khi \(\phi > 0\), điều này chỉ xảy ra nếu SINR_E bao gồm \(\phi P_A |h_E|^2\) trong mẫu số.
- Các chỉ số như \(R_{s_i}\), SOP, IP được tính dựa trên \(C_{B_i} - C_E\), cho thấy \(\phi\) ảnh hưởng đến \(C_E\).

### Ví dụ đoạn mã kiểm tra
Dưới đây là một đoạn mã giả định trong `NOMAImprovementTwoUserFinal_fixed.py` để tính SINR và dung lượng kênh:
```python
# Tham số
P_A = 1.0
N_0 = 1e-15
B = 10e6
phi = 0.3
alpha_1 = 0.3
alpha_2 = 0.7
epsilon = 0.005
d_B1, d_B2, d_E = 30, 70, 50
alpha = 3

# Tính hệ số kênh
h_B1 = d_B1**(-alpha/2)
h_B2 = d_B2**(-alpha/2)
h_E = d_E**(-alpha/2)

# Tính SINR
SINR_B1 = (P_A * alpha_1 * h_B1**2) / (P_A * alpha_2 * h_B1**2 * epsilon + N_0 + phi * P_A * h_B1**2)
SINR_B2 = (P_A * alpha_2 * h_B2**2) / (N_0 + phi * P_A * h_B2**2)
SINR_E = (P_A * alpha_1 * h_E**2) / (N_0 + phi * P_A * h_E**2)

# Tính dung lượng kênh
C_B1 = B * np.log2(1 + SINR_B1)
C_B2 = B * np.log2(1 + SINR_B2)
C_E = B * np.log2(1 + SINR_E)
```

### Kết luận kiểm tra
- Nếu mã sử dụng công thức SINR như trên, thì **SNR đã được thay bằng SINR**, bao gồm ảnh hưởng của \(\phi\). Điều này phù hợp với các kịch bản có AN (\(\phi > 0\)).
- **Xác nhận**: Cần kiểm tra trực tiếp mã `NOMAImprovementTwoUserFinal_fixed.py` để đảm bảo rằng \(\phi P_A |h_i|^2\) được thêm vào mẫu số của SINR. Nếu mã chỉ sử dụng SNR (không có \(\phi\)), thì cần sửa để tích hợp AN đúng cách.

### Đề xuất
- Nếu mã chưa tích hợp \(\phi\) vào SINR, cần cập nhật công thức SINR như trên.
- Thêm kiểm tra đầu ra của \(C_E\) để xác nhận rằng dung lượng kênh của Eve giảm khi \(\phi\) tăng, chứng minh AN được áp dụng đúng.