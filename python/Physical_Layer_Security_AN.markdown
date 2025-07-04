# 3.3 Bảo mật tầng vật lý với nhiễu nhân tạo (Artificial Noise) của BS

## 3.3.1 Nguyên lý/Cơ sở lý thuyết bảo mật tầng vật lý với nhiễu nhân tạo

Bảo mật tầng vật lý (Physical Layer Security - PLS) tận dụng các đặc tính của kênh truyền thông không dây để đảm bảo an toàn thông tin mà không phụ thuộc hoàn toàn vào mã hóa cấp cao. Trong hệ thống **NOMA (Non-Orthogonal Multiple Access)**, tín hiệu của nhiều người dùng được truyền đồng thời trên cùng một tài nguyên tần số, sử dụng phân bổ công suất khác nhau. Tuy nhiên, điều này làm tăng nguy cơ bị nghe lén bởi các thiết bị không mong muốn (Eve). Nhiễu nhân tạo (Artificial Noise - AN) được trạm gốc (BS) tạo ra và thêm vào tín hiệu truyền để làm suy giảm khả năng giải mã của Eve, đồng thời duy trì chất lượng tín hiệu cho người dùng hợp pháp (Bob).

### Nguyên lý hoạt động
Nhiễu nhân tạo được thiết kế để:
- **Tác động tối đa đến Eve**: AN được truyền cùng với tín hiệu dữ liệu, làm giảm tỷ số tín hiệu trên nhiễu (SNR) tại Eve.
- **Tác động tối thiểu đến Bob**: Sử dụng thông tin trạng thái kênh (CSI - Channel State Information) để định hướng AN vào không gian vô hiệu (null space) của kênh người dùng hợp pháp.
- **Tăng cường bảo mật**: Làm giảm dung lượng kênh của Eve ($C_E$), từ đó tăng tốc độ bí mật ($R_s$) của người dùng hợp pháp.

### Công thức toán học liên quan
1. **Dung lượng kênh**:
   Dung lượng kênh của người dùng hợp pháp (Bob) và kẻ nghe lén (Eve) được tính dựa trên công thức Shannon:
   \[
   C_i = B \log_2 \left(1 + \text{SINR}_i\right), \quad i \in \{B1, B2, E\}
   \]
   Trong đó:
   - $B$ là băng thông (10 MHz trong kịch bản).
   - $\text{SINR}_i$ là tỷ số tín hiệu trên nhiễu và can nhiễu (Signal-to-Interference-plus-Noise Ratio) của Bob1, Bob2 hoặc Eve.

   Với NOMA, SINR của Bob1 và Bob2 chịu ảnh hưởng của nhiễu lẫn nhau (do SIC - Successive Interference Cancellation) và nhiễu nhân tạo:
   \[
   \text{SINR}_{B1} = \frac{P_A \alpha_1 |h_{B1}|^2}{P_A \alpha_2 |h_{B1}|^2 \epsilon + N_0 + \phi P_A |h_{B1}|^2}
   \]
   \[
   \text{SINR}_{B2} = \frac{P_A \alpha_2 |h_{B2}|^2}{N_0 + \phi P_A |h_{B2}|^2}
   \]
   Với Eve:
   \[
   \text{SINR}_E = \frac{P_A \alpha_i |h_E|^2}{N_0 + \phi P_A |h_E|^2}, \quad i \in \{1, 2\}
   \]
   Trong đó:
   - $P_A = 1$ W: Công suất truyền của BS.
   - $\alpha_1 = 0.3$, $\alpha_2 = 0.7$: Hệ số phân bổ công suất cho Bob1 và Bob2.
   - $\phi = 0.3$ (hoặc $0.2$): Tỷ lệ công suất dành cho AN.
   - $h_{B1}$, $h_{B2}$, $h_E$: Hệ số kênh của Bob1, Bob2 và Eve, phụ thuộc vào khoảng cách và suy hao kênh ($\alpha = 3$).
   - $\epsilon = 0.005$: Tỷ lệ lỗi SIC.
   - $N_0 = 10^{-15}$ W: Nhiễu nền.

2. **Tốc độ bí mật ($R_s$)**:
   Tốc độ bí mật của người dùng $i$ được định nghĩa là:
   \[
   R_{s_i} = \max \left( C_{B_i} - C_E, 0 \right), \quad i \in \{1, 2\}
   \]
   Nếu $C_{B_i} \leq C_E$, thì $R_{s_i} = 0$, nghĩa là không có thông tin bí mật.

3. **Xác suất gián đoạn bí mật (SOP)**:
   SOP đo lường xác suất mà tốc độ bí mật nhỏ hơn một ngưỡng $R_{\text{th}}$:
   \[
   \text{SOP}_i = P \left( R_{s_i} < R_{\text{th}} \right)
   \]
   Trong kịch bản, $R_{\text{th}}$ được chọn dựa trên yêu cầu hệ thống.

4. **Xác suất chặn (IP)**:
   IP là xác suất Eve giải mã thành công tín hiệu của người dùng hợp pháp:
   \[
   \text{IP}_i = P \left( C_E \geq C_{B_i} \right)
   \]

5. **Hiệu quả bí mật ($\eta_s$)**:
   Hiệu quả bí mật được tính bằng tỷ số giữa tốc độ bí mật và công suất tiêu thụ:
   \[
   \eta_{s_i} = \frac{R_{s_i}}{P_A}
   \]

## 3.3.2 Thuật toán nhiễu nhân tạo AN tác động đến nghe lén chủ động

Dưới đây là thuật toán giả (pseudocode) mô tả việc áp dụng nhiễu nhân tạo trong hệ thống NOMA để đối phó với nghe lén chủ động:

```
Algorithm: Apply_Artificial_Noise_NOMA
Input:
  - P_A: Công suất truyền (1 W)
  - N_0: Nhiễu nền (10^-15 W)
  - B: Băng thông (10 MHz)
  - alpha_1, alpha_2: Hệ số phân bổ công suất (0.3, 0.7)
  - phi: Tỷ lệ công suất nhiễu nhân tạo (0.3 hoặc 0.2)
  - d_B1, d_B2: Khoảng cách của Bob1 và Bob2 (30m, 70m)
  - d_E: Khoảng cách của Eve (20m đến 150m, bước 10m)
  - SNR_Bob, SNR_Eve: Tỷ số tín hiệu trên nhiễu (0 dB đến 20 dB)
  - epsilon: Tỷ lệ lỗi SIC (0.005)
  - alpha: Hệ số suy hao kênh (3)
  - N: Số anten (16)

Output:
  - C_B1, C_B2, C_E: Dung lượng kênh của Bob1, Bob2, Eve
  - BER_B1, BER_B2, BER_E: Tỷ lệ lỗi bit
  - R_s1, R_s2: Tốc độ bí mật
  - SOP1, SOP2: Xác suất gián đoạn bí mật
  - IP1, IP2: Xác suất chặn
  - eta_s1, eta_s2: Hiệu quả bí mật

Begin:
  1. Initialize system parameters (P_A, N_0, B, alpha_1, alpha_2, phi, epsilon, alpha, N)
  2. For each d_E in [20, 150] with step 10m:
      a. Adjust d_E to satisfy min(|d_B1 - d_E|, |d_B2 - d_E|) >= 5m
      b. For each SNR_Bob, SNR_Eve in [0, 20] dB:
          i. Calculate channel gains h_B1, h_B2, h_E using path loss model: |h_i|^2 = d_i^(-alpha)
          ii. Compute SINR_B1, SINR_B2, SINR_E using formulas:
              SINR_B1 = (P_A * alpha_1 * |h_B1|^2) / (P_A * alpha_2 * |h_B1|^2 * epsilon + N_0 + phi * P_A * |h_B1|^2)
              SINR_B2 = (P_A * alpha_2 * |h_B2|^2) / (N_0 + phi * P_A * |h_B2|^2)
              SINR_E = (P_A * alpha_i * |h_E|^2) / (N_0 + phi * P_A * |h_E|^2)
          iii. Calculate channel capacities:
              C_B1 = B * log2(1 + SINR_B1)
              C_B2 = B * log2(1 + SINR_B2)
              C_E = B * log2(1 + SINR_E)
          iv. Calculate secrecy rates:
              R_s1 = max(C_B1 - C_E, 0)
              R_s2 = max(C_B2 - C_E, 0)
          v. Estimate BER_B1, BER_B2, BER_E using modulation model (e.g., QPSK)
          vi. Compute SOP1, SOP2 using Monte Carlo simulation for P(R_s_i < R_th)
          vii. Compute IP1, IP2 using P(C_E >= C_B_i)
          viii. Compute secrecy efficiencies:
              eta_s1 = R_s1 / P_A
              eta_s2 = R_s2 / P_A
      c. Store results for d_E, SNR_Bob, SNR_Eve
  3. Output results (C_B1, C_B2, C_E, BER_B1, BER_B2, BER_E, R_s1, R_s2, SOP1, SOP2, IP1, IP2, eta_s1, eta_s2)
End
```

Thuật toán trên được triển khai trong mã nguồn `NOMAImprovementTwoUserFinal_fixed.py`, mô phỏng hệ thống NOMA với nhiễu nhân tạo, tính toán các chỉ số hiệu suất dựa trên các tham số hệ thống đã cho.

## 3.3.3 Đánh giá hiệu quả bảo mật áp dụng AN

Dựa trên kết quả từ hai file đầu ra `Eve_Change_dE-AN_Pilot-With-Phi.txt` và `Eve_Change_SNR-AN_Pilot-With-Phi.txt`, hiệu quả bảo mật của nhiễu nhân tạo được phân tích chi tiết. Dưới đây là đánh giá các chỉ số bảo mật và so sánh với trường hợp không áp dụng AN.

### Kịch bản 1: Quét khoảng cách Eve ($d_E$)
**Thông số**: $\phi = 0.3$, SNR Bob = 20 dB, SNR Eve = 30 dB, $d_E$ từ 20m đến 150m.

#### Phân tích các chỉ số
1. **Dung lượng kênh ($C_{B1}$, $C_{B2}$, $C_E$)**:
   - Khi $d_E$ tăng từ 20m đến 150m, dung lượng kênh của Eve ($C_E$) giảm mạnh từ 110.08 Mbps xuống 28.29 Mbps do ảnh hưởng của suy hao kênh và nhiễu nhân tạo.
   - Dung lượng của Bob1 tăng từ 51.36 Mbps lên 57.90 Mbps, và Bob2 tăng từ 4.94 Mbps (tại $d_E = 75$ m) lên 55.49 Mbps (tại $d_E = 150$ m). Điều này cho thấy nhiễu nhân tạo ít ảnh hưởng đến người dùng hợp pháp khi $d_E$ lớn.
   - **So sánh không áp dụng AN**: Nếu không có AN ($\phi = 0$), $C_E$ sẽ cao hơn đáng kể vì không có nhiễu bổ sung, dẫn đến giảm tốc độ bí mật.

2. **Tốc độ bí mật ($R_{s1}$, $R_{s2}$)**:
   - $R_{s1}$ tăng từ 0.08 (tại $d_E = 60$ m) lên 3.93 (tại $d_E = 150$ m). $R_{s2}$ tăng từ 0.28 (tại $d_E = 100$ m) lên 2.72 (tại $d_E = 150$ m).
   - **So sánh không áp dụng AN**: Khi $\phi = 0$, $C_E$ lớn hơn dẫn đến $R_{s1}$ và $R_{s2}$ giảm đáng kể, thậm chí bằng 0 khi $C_E > C_{B_i}$, đặc biệt ở $d_E$ nhỏ.

3. **Xác suất gián đoạn bí mật (SOP)**:
   - SOP1 giảm từ 1.00 (tại $d_E = 20$ m) xuống 0.00 (tại $d_E \geq 100$ m). SOP2 giảm từ 1.00 xuống 0.00 (tại $d_E \geq 140$ m).
   - **So sánh không áp dụng AN**: Không có AN, SOP1 và SOP2 sẽ cao hơn (gần 1.00) ở mọi $d_E$, do $C_E$ lớn làm giảm $R_{s_i}$.

4. **Xác suất chặn (IP)**:
   - IP1 giảm từ 1.00 xuống 0.00 khi $d_E$ tăng từ 20m đến 100m. IP2 giảm từ 1.00 xuống 0.00 khi $d_E \geq 120$ m.
   - **So sánh không áp dụng AN**: IP sẽ cao hơn (gần 1.00) ở mọi $d_E$, vì Eve dễ dàng giải mã tín hiệu khi không có nhiễu.

5. **Hiệu quả bí mật ($\eta_{s1}$, $\eta_{s2}$)**:
   - $\eta_{s1}$ tăng từ $8.21 \times 10^{-9}$ lên $3.93 \times 10^{-7}$, $\eta_{s2}$ tăng từ 0 lên $2.72 \times 10^{-7}$ khi $d_E$ tăng.
   - **So sánh không áp dụng AN**: $\eta_{s_i}$ sẽ thấp hơn đáng kể vì $R_{s_i}$ giảm khi không có AN.

#### Kết luận kịch bản 1
Nhiễu nhân tạo với $\phi = 0.3$ hiệu quả trong việc giảm $C_E$, tăng $R_{s_i}$, giảm SOP và IP, đồng thời cải thiện $\eta_{s_i}$ khi $d_E$ tăng. So với trường hợp không áp dụng AN, các chỉ số bảo mật được cải thiện rõ rệt, đặc biệt khi Eve ở xa BS.

### Kịch bản 2: Quét SNR của Bob và Eve
**Thông số**: $\phi = 0.2$, SNR Bob từ 0 dB đến 20 dB, SNR Eve từ 0 dB đến 20 dB.

#### Phân tích các chỉ số
1. **Dung lượng kênh ($C_{B1}$, $C_{B2}$, $C_E$)**:
   - $C_{B1}$ tăng từ 15.26 Mbps (SNR Bob = 0 dB, SNR Eve = 20 dB) lên 52.96 Mbps (SNR Bob = 20 dB, SNR Eve = 0 dB). $C_{B2}$ tăng từ 7.24 Mbps lên 61.12 Mbps.
   - $C_E$ tăng từ 15.35 Mbps (SNR Eve = 0 dB) lên 74.98 Mbps (SNR Eve = 20 dB), cho thấy nhiễu nhân tạo với $\phi = 0.2$ không đủ mạnh để kiềm chế Eve khi SNR Eve cao.
   - **So sánh không áp dụng AN**: Không có AN, $C_E$ sẽ cao hơn, đặc biệt khi SNR Eve lớn, dẫn đến bảo mật kém hơn.

2. **Tốc độ bí mật ($R_{s1}$, $R_{s2}$)**:
   - $R_{s1}$ giảm từ 1.28 (SNR Bob = 0 dB, SNR Eve = 0 dB) xuống 0.00 (SNR Bob = 20 dB, SNR Eve $\geq 2$ dB). $R_{s2}$ hầu như bằng 0 trong mọi trường hợp.
   - **So sánh không áp dụng AN**: $R_{s_i}$ sẽ thấp hơn nữa vì $C_E$ tăng mạnh, đặc biệt khi SNR Eve cao.

3. **Xác suất gián đoạn bí mật (SOP)**:
   - SOP1 tăng từ 0.18 lên 1.00 khi SNR Eve tăng từ 0 dB đến 20 dB. SOP2 duy trì ở 1.00, cho thấy Bob2 dễ bị ảnh hưởng hơn.
   - **So sánh không áp dụng AN**: SOP sẽ cao hơn (gần 1.00) trong mọi trường hợp do $C_E$ lớn.

4. **Xác suất chặn (IP)**:
   - IP1 tăng từ 0.00 lên 1.00 khi SNR Eve tăng. IP2 duy trì ở 1.00.
   - **So sánh không áp dụng AN**: IP sẽ cao hơn, đặc biệt khi SNR Eve lớn, do Eve dễ dàng giải mã tín hiệu.

5. **Hiệu quả bí mật ($\eta_{s1}$, $\eta_{s2}$)**:
   - $\eta_{s1}$ giảm từ $1.28 \times 10^{-7}$ xuống $2.44 \times 10^{-11}$ khi SNR Eve tăng. $\eta_{s2}$ rất thấp, dao động quanh $10^{-11}$.
   - **So sánh không áp dụng AN**: $\eta_{s_i}$ sẽ thấp hơn do $R_{s_i}$ giảm.

#### Kết luận kịch bản 2
Nhiễu nhân tạo với $\phi = 0.2$ có hiệu quả hạn chế khi SNR Eve tăng cao. So với trường hợp không áp dụng AN, AN vẫn cải thiện các chỉ số bảo mật, nhưng hiệu quả giảm khi SNR Eve lớn, đòi hỏi tăng $\phi$ hoặc kết hợp các kỹ thuật bảo mật khác.

### Tổng kết
Nhiễu nhân tạo là công cụ hiệu quả để tăng cường bảo mật tầng vật lý trong hệ thống NOMA, đặc biệt khi Eve ở xa BS hoặc có SNR thấp. So với trường hợp không áp dụng AN, các chỉ số $R_{s_i}$, SOP, IP và $\eta_{s_i}$ được cải thiện rõ rệt. Tuy nhiên, khi SNR Eve cao, cần điều chỉnh $\phi$ hoặc áp dụng các chiến lược bổ sung như tối ưu hóa phân bổ công suất hoặc mã hóa nâng cao.