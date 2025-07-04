# Phân bổ công suất động trong hệ thống NOMA với nhiễu nhân tạo

## Cơ sở lý thuyết phân bổ công suất động (Dynamic Power Allocation)

Phân bổ công suất động (Dynamic Power Allocation - DPA) trong hệ thống **NOMA (Non-Orthogonal Multiple Access)** nhằm tối ưu hóa hiệu suất hệ thống bằng cách điều chỉnh các hệ số công suất ($\alpha_1$, $\alpha_2$) cho các người dùng hợp pháp (Bob1, Bob2) dựa trên các yếu tố như khoảng cách của kẻ nghe lén (Eve - $d_E$), tỷ số tín hiệu trên nhiễu (SNR) của Bob và Eve, và mục tiêu tối ưu hóa các chỉ số bảo mật như tốc độ bí mật ($R_{s1}$, $R_{s2}$), xác suất gián đoạn bí mật (SOP), xác suất chặn (IP), và hiệu quả bí mật ($\eta_{s1}$, $\eta_{s2}$). Trong bối cảnh sử dụng nhiễu nhân tạo (Artificial Noise - AN), DPA cần cân bằng giữa việc đảm bảo chất lượng tín hiệu cho người dùng hợp pháp và làm giảm khả năng giải mã của Eve.

### Nguyên lý
Trong hệ thống NOMA, tín hiệu của Bob1 và Bob2 được truyền đồng thời với các hệ số công suất $\alpha_1$ và $\alpha_2$ thỏa mãn $\alpha_1 + \alpha_2 = 1 - \phi$, trong đó $\phi$ là tỷ lệ công suất dành cho AN. Mục tiêu tối ưu hóa là tối đa hóa $\min(R_{s1}, R_{s2})$ để đảm bảo hiệu suất bảo mật công bằng giữa các người dùng hợp pháp, đồng thời giảm SOP, IP và tăng $\eta_{s}$.

Các chỉ số bảo mật được định nghĩa như sau:
- **Tốc độ bí mật**:
  \[
  R_{s_i} = \max \left( C_{B_i} - C_E, 0 \right), \quad i \in \{1, 2\}
  \]
  Trong đó:
  \[
  C_{B_i} = B \log_2 \left(1 + \text{SINR}_{B_i}\right), \quad C_E = B \log_2 \left(1 + \text{SINR}_E\right)
  \]
  Với SINR (Signal-to-Interference-plus-Noise Ratio) của Bob1, Bob2, và Eve được tính:
  \[
  \text{SINR}_{B1} = \frac{P_A \alpha_1 |h_{B1}|^2}{P_A \alpha_2 |h_{B1}|^2 \epsilon + N_0 + \phi P_A |h_{B1}|^2}
  \]
  \[
  \text{SINR}_{B2} = \frac{P_A \alpha_2 |h_{B2}|^2}{N_0 + \phi P_A |h_{B2}|^2}
  \]
  \[
  \text{SINR}_E = \frac{P_A \alpha_i |h_E|^2}{N_0 + \phi P_A |h_E|^2}, \quad i \in \{1, 2\}
  \]
  Trong đó:
  - $P_A = 1$ W: Công suất truyền.
  - $N_0 = 10^{-15}$ W: Nhiễu nền.
  - $B = 10$ MHz: Băng thông.
  - $|h_i|^2 = d_i^{-\alpha}$: Hệ số kênh, với $\alpha = 3$ (suy hao kênh).
  - $\epsilon = 0.005$: Tỷ lệ lỗi SIC.
  - $\phi = 0.3$ (hoặc $0.2$): Tỷ lệ công suất AN.

- **Mục tiêu tối ưu hóa**:
  Tối đa hóa $\min(R_{s1}, R_{s2})$ với ràng buộc:
  \[
  \alpha_1 + \alpha_2 = 1 - \phi, \quad \alpha_1, \alpha_2 \geq 0
  \]
  Điều này đảm bảo công bằng giữa Bob1 và Bob2, đồng thời giảm $C_E$ để tăng $R_{s_i}$.

- **Các yếu tố ảnh hưởng**:
  - **Khoảng cách Eve ($d_E$)**: Khi $d_E$ tăng, $|h_E|^2$ giảm, làm giảm $C_E$ và tăng $R_{s_i}$.
  - **SNR Bob và SNR Eve**: SNR cao của Eve làm tăng $C_E$, đòi hỏi điều chỉnh $\alpha_1$, $\alpha_2$ và $\phi$ để giảm tác động của Eve.
  - **Nhiễu nhân tạo ($\phi$)**: Tăng $\phi$ làm giảm $C_E$ nhưng có thể ảnh hưởng đến $\text{SINR}_{B_i}$, cần tối ưu hóa để cân bằng.

### Các chỉ số bảo mật liên quan
1. **Xác suất gián đoạn bí mật (SOP)**:
   \[
   \text{SOP}_i = P \left( R_{s_i} < R_{\text{th}} \right)
   \]
   Tối ưu hóa $\alpha_1$, $\alpha_2$ nhằm giảm SOP bằng cách tăng $R_{s_i}$.

2. **Xác suất chặn (IP)**:
   \[
   \text{IP}_i = P \left( C_E \geq C_{B_i} \right)
   \]
   Giảm IP bằng cách tăng $\text{SINR}_{B_i}$ và giảm $\text{SINR}_E$.

3. **Hiệu quả bí mật ($\eta_s$)**:
   \[
   \eta_{s_i} = \frac{R_{s_i}}{P_A}
   \]
   Tăng $\eta_{s_i}$ bằng cách tối ưu hóa $R_{s_i}$ với công suất cố định.

## Phương hướng và thuật toán trong các nghiên cứu hiện tại

Các nghiên cứu hiện tại về DPA trong NOMA với AN tập trung vào các phương pháp tối ưu hóa để điều chỉnh $\alpha_1$, $\alpha_2$ dựa trên $d_E$, SNR Bob, và SNR Eve. Dưới đây là các phương hướng chính và các thuật toán phổ biến:

### 1. Phương hướng nghiên cứu
- **Tối ưu hóa dựa trên tối đa hóa tốc độ bí mật**:
  Nhiều nghiên cứu tập trung vào việc tối đa hóa $\min(R_{s1}, R_{s2})$ hoặc tổng tốc độ bí mật ($R_{s1} + R_{s2}$) bằng cách sử dụng các thuật toán tối ưu hóa phi tuyến. Điều này thường đi kèm với việc sử dụng AN để làm giảm $C_E$.
- **Tối ưu hóa công bằng (Fairness)**:
  Đảm bảo công bằng giữa các người dùng bằng cách tối ưu hóa $\min(R_{s1}, R_{s2})$ thay vì ưu tiên một người dùng. Điều này đặc biệt quan trọng trong NOMA, nơi người dùng có kênh yếu (Bob2) dễ bị ảnh hưởng bởi nhiễu lẫn nhau.
- **Kết hợp với nhiễu nhân tạo**:
  AN được thiết kế để nằm trong không gian vô hiệu của kênh Bob, sử dụng kỹ thuật beamforming trong hệ thống MIMO. Các nghiên cứu đề xuất điều chỉnh $\phi$ đồng thời với $\alpha_1$, $\alpha_2$ để tối ưu hóa hiệu quả bảo mật.
- **Tối ưu hóa dựa trên điều kiện kênh**:
  Sử dụng thông tin trạng thái kênh (CSI) của Bob và Eve để điều chỉnh động các tham số công suất. Khi CSI của Eve không hoàn hảo, các phương pháp ước lượng kênh được áp dụng.
- **Học máy và học sâu**:
  Một số nghiên cứu gần đây sử dụng học máy (ví dụ: Reinforcement Learning) để học chiến lược phân bổ công suất tối ưu dựa trên $d_E$, SNR, và các chỉ số bảo mật.

### 2. Các thuật toán phổ biến
Dưới đây là các thuật toán được sử dụng trong các nghiên cứu hiện tại:

#### a. Thuật toán Gradient Descent
- **Mô tả**: Sử dụng gradient descent để tối ưu hóa hàm mục tiêu $\min(R_{s1}, R_{s2})$ bằng cách điều chỉnh $\alpha_1$, $\alpha_2$ với ràng buộc $\alpha_1 + \alpha_2 = 1 - \phi$.
- **Pseudocode**:
  ```
  Algorithm: Gradient_Descent_DPA
  Input: P_A, N_0, B, phi, d_B1, d_B2, d_E, SNR_Bob, SNR_Eve, epsilon, alpha, N
  Output: alpha_1, alpha_2 optimal
  Begin:
    1. Initialize alpha_1 = 0.3, alpha_2 = 0.7 - phi
    2. Set learning_rate = 0.01, max_iterations = 1000
    3. For iteration = 1 to max_iterations:
        a. Compute SINR_B1, SINR_B2, SINR_E
        b. Compute C_B1, C_B2, C_E
        c. Compute R_s1 = max(C_B1 - C_E, 0), R_s2 = max(C_B2 - C_E, 0)
        d. Compute objective = min(R_s1, R_s2)
        e. Compute gradients d_objective/d_alpha_1, d_objective/d_alpha_2
        f. Update alpha_1 = alpha_1 + learning_rate * d_objective/d_alpha_1
        g. Update alpha_2 = 1 - phi - alpha_1
        h. If |objective_new - objective_old| < threshold, break
    4. Return alpha_1, alpha_2
  End
  ```
- **Ưu điểm**: Đơn giản, dễ triển khai.
- **Nhược điểm**: Có thể rơi vào cực trị cục bộ, tốc độ hội tụ chậm với hàm mục tiêu phức tạp.

#### b. Thuật toán Convex Optimization
- **Mô tả**: Chuyển bài toán tối ưu hóa $\min(R_{s1}, R_{s2})$ thành bài toán lồi bằng cách xấp xỉ hoặc biến đổi hàm mục tiêu. Các công cụ như CVX hoặc MOSEK được sử dụng.
- **Công thức**:
  \[
  \max_{\alpha_1, \alpha_2} \min(R_{s1}, R_{s2}) \quad \text{s.t.} \quad \alpha_1 + \alpha_2 = 1 - \phi, \quad \alpha_1, \alpha_2 \geq 0
  \]
- **Phương pháp**: Sử dụng phương pháp Lagrange hoặc nội điểm (interior-point method) để giải.
- **Ưu điểm**: Đảm bảo tìm được nghiệm tối ưu toàn cục nếu bài toán lồi.
- **Nhược điểm**: Phức tạp tính toán, yêu cầu CSI chính xác.

#### c. Thuật toán Heuristic
- **Mô tả**: Sử dụng các quy tắc đơn giản dựa trên điều kiện kênh, ví dụ: phân bổ công suất tỷ lệ nghịch với $|h_{B_i}|^2$ hoặc tỷ lệ thuận với $d_E$.
- **Pseudocode**:
  ```
  Algorithm: Heuristic_DPA
  Input: P_A, phi, d_B1, d_B2, d_E, SNR_Bob, SNR_Eve
  Output: alpha_1, alpha_2
  Begin:
    1. Compute channel gains |h_B1|^2, |h_B2|^2, |h_E|^2
    2. If d_E < d_B1:
        alpha_1 = (1 - phi) * |h_B2|^2 / (|h_B1|^2 + |h_B2|^2)
        alpha_2 = (1 - phi) - alpha_1
    3. Else:
        alpha_1 = (1 - phi) * SNR_Bob / (SNR_Bob + SNR_Eve)
        alpha_2 = (1 - phi) - alpha_1
    4. Return alpha_1, alpha_2
  End
  ```
- **Ưu điểm**: Đơn giản, tính toán nhanh.
- **Nhược điểm**: Không đảm bảo tối ưu toàn cục.

#### d. Reinforcement Learning (RL)
- **Mô tả**: Sử dụng RL (ví dụ: Q-learning hoặc Deep Q-Network) để học chính sách phân bổ công suất dựa trên trạng thái ($d_E$, SNR Bob, SNR Eve) và phần thưởng là $\min(R_{s1}, R_{s2})$.
- **Quy trình**:
  - **Trạng thái**: ($d_E$, SNR_Bob, SNR_Eve, $|h_{B1}|^2$, $|h_{B2}|^2$, $|h_E|^2$).
  - **Hành động**: Điều chỉnh $\alpha_1$, $\alpha_2$.
  - **Phần thưởng**: $\min(R_{s1}, R_s2) - \lambda (\text{SOP}_1 + \text{SOP}_2)$, với $\lambda$ là trọng số.
- **Ưu điểm**: Thích nghi tốt với môi trường động, không cần CSI hoàn hảo.
- **Nhược điểm**: Yêu cầu thời gian huấn luyện dài, phức tạp triển khai.

### So sánh các phương pháp
| Phương pháp          | Ưu điểm                              | Nhược điểm                           | Phù hợp với kịch bản                   |
|----------------------|--------------------------------------|--------------------------------------|----------------------------------------|
| Gradient Descent     | Đơn giản, dễ triển khai             | Chậm hội tụ, có thể rơi vào cực trị cục bộ | Kịch bản đơn giản, CSI ổn định         |
| Convex Optimization  | Tối ưu toàn cục (nếu lồi)           | Phức tạp, yêu cầu CSI chính xác      | Hệ thống yêu cầu bảo mật cao           |
| Heuristic            | Nhanh, dễ thực hiện                 | Không đảm bảo tối ưu                 | Hệ thống hạn chế tài nguyên tính toán  |
| Reinforcement Learning | Thích nghi môi trường động         | Phức tạp, cần huấn luyện lâu         | Hệ thống với CSI không hoàn hảo       |

### Đề xuất áp dụng
Dựa trên yêu cầu tối ưu hóa $\min(R_{s1}, R_{s2})$ trong hệ thống NOMA với AN, đề xuất sử dụng **Convex Optimization** khi CSI của Bob và Eve được biết chính xác, vì nó đảm bảo nghiệm tối ưu. Nếu CSI không hoàn hảo hoặc hệ thống cần thích nghi động, **Reinforcement Learning** là lựa chọn phù hợp. Trong trường hợp tài nguyên tính toán hạn chế, phương pháp **Heuristic** có thể được áp dụng để đạt hiệu quả nhanh chóng.