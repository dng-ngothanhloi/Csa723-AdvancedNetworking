# Trả lời các câu hỏi về phân bổ công suất động (DPA) trong hệ thống NOMA với nhiễu nhân tạo

## 1. Điều chỉnh \(\alpha_1\), \(\alpha_2\) được xử lý bởi BS hay thế nào?

### Lý thuyết
Trong hệ thống NOMA (Non-Orthogonal Multiple Access), các hệ số công suất \(\alpha_1\), \(\alpha_2\) được sử dụng để phân bổ công suất cho các người dùng hợp pháp (Bob1, Bob2). Việc điều chỉnh \(\alpha_1\), \(\alpha_2\) thường được thực hiện bởi **trạm gốc (Base Station - BS)**, vì BS có khả năng:
- Thu thập thông tin trạng thái kênh (CSI - Channel State Information) của Bob1, Bob2 và, trong một số trường hợp, của kẻ nghe lén (Eve).
- Tính toán và tối ưu hóa các hệ số công suất dựa trên các mục tiêu như tối đa hóa tốc độ bí mật (\(\min(R_{s1}, R_{s2})\)) hoặc giảm xác suất gián đoạn bí mật (SOP) và xác suất chặn (IP).
- Điều chỉnh tín hiệu truyền, bao gồm cả nhiễu nhân tạo (AN), dựa trên các thông số tối ưu.

Cụ thể, BS thực hiện các bước sau:
1. **Thu thập CSI**: BS nhận thông tin về hệ số kênh (\(|h_{B1}|^2\), \(|h_{B2}|^2\), và đôi khi \(|h_E|^2\)) thông qua các tín hiệu pilot từ người dùng.
2. **Tính toán tối ưu**: BS sử dụng các thuật toán tối ưu hóa (như Gradient Descent, Convex Optimization, hoặc Heuristic) để xác định \(\alpha_1\), \(\alpha_2\) sao cho đáp ứng mục tiêu (ví dụ: tối đa hóa \(\min(R_{s1}, R_{s2})\)).
3. **Phân bổ công suất**: BS áp dụng \(\alpha_1\), \(\alpha_2\) vào tín hiệu truyền, đồng thời kết hợp nhiễu nhân tạo với tỷ lệ \(\phi\).

### Thực tế
Trong thực tế, việc điều chỉnh \(\alpha_1\), \(\alpha_2\) được thực hiện bởi **bộ điều khiển tín hiệu số (Digital Signal Processor - DSP)** hoặc **bộ điều khiển trung tâm** tại BS, với các yếu tố sau:
- **Phần cứng**: BS được trang bị các bộ xử lý tín hiệu mạnh để tính toán thời gian thực, đặc biệt trong các hệ thống MIMO hoặc 5G/6G.
- **Phần mềm**: Các thuật toán tối ưu hóa được tích hợp trong phần mềm quản lý tài nguyên vô tuyến (Radio Resource Management - RRM) của BS.
- **Phản hồi từ người dùng**: Các thiết bị người dùng (UEs) gửi thông tin CSI qua kênh điều khiển ngược (uplink control channel), giúp BS cập nhật \(\alpha_1\), \(\alpha_2\) theo thời gian thực.
- **Tần suất điều chỉnh**: \(\alpha_1\), \(\alpha_2\) được cập nhật định kỳ (theo chu kỳ truyền tín hiệu hoặc khi CSI thay đổi đáng kể) để thích nghi với điều kiện kênh thay đổi.

Tuy nhiên, trong một số trường hợp đặc biệt (ví dụ: mạng phân tán hoặc mạng ad-hoc), các thiết bị người dùng có thể tham gia vào quá trình điều chỉnh công suất thông qua giao thức hợp tác, nhưng điều này ít phổ biến trong NOMA.

## 2. Làm sao để nhận biết \(d_E\), SNR_Bob, SNR_Eve trong môi trường mô phỏng và áp dụng DPA trong thực tế?

### Trong môi trường mô phỏng
Trong mô phỏng, các tham số như \(d_E\), SNR_Bob, SNR_Eve được giả định hoặc điều chỉnh để đánh giá hiệu suất hệ thống. Cách tiếp cận bao gồm:

1. **Khoảng cách Eve (\(d_E\))**:
   - **Cách xác định**: Trong mô phỏng, \(d_E\) được quét trong một phạm vi (ví dụ: 20m đến 150m) để mô phỏng vị trí khác nhau của Eve. Khoảng cách được giả định dựa trên mô hình suy hao kênh (path loss), ví dụ:
     \[
     |h_E|^2 = d_E^{-\alpha}, \quad \alpha = 3
     \]
   - **Công cụ**: Các phần mềm như MATLAB, Python (với thư viện NumPy hoặc SciPy) được sử dụng để tạo các giá trị \(d_E\) và tính toán hệ số kênh.

2. **SNR_Bob, SNR_Eve**:
   - **Cách xác định**: SNR được tính dựa trên công suất truyền (\(P_A\)), nhiễu nền (\(N_0\)), và hệ số kênh:
     \[
     \text{SNR}_{B_i} = \frac{P_A |h_{B_i}|^2}{N_0}, \quad \text{SNR}_E = \frac{P_A |h_E|^2}{N_0}
     \]
     Trong mô phỏng, SNR_Bob và SNR_Eve được quét trong khoảng (ví dụ: 0 dB đến 20 dB) để đánh giá hiệu suất dưới các điều kiện kênh khác nhau.
   - **Nhiễu nhân tạo**: Khi áp dụng AN, SNR được thay bằng SINR, bao gồm cả ảnh hưởng của \(\phi\):
     \[
     \text{SINR}_E = \frac{P_A \alpha_i |h_E|^2}{N_0 + \phi P_A |h_E|^2}
     \]

3. **Phương pháp mô phỏng**:
   - Sử dụng các kịch bản như trong file `NOMAImprovementTwoUserFinal_fixed.py`, nơi các tham số \(d_E\), SNR_Bob, SNR_Eve được quét để tính toán các chỉ số như \(C_{B_i}\), \(C_E\), \(R_{s_i}\), SOP, IP, \(\eta_{s_i}\).
   - Mô phỏng Monte Carlo được sử dụng để đánh giá xác suất (SOP, IP) bằng cách chạy nhiều lần với các giá trị ngẫu nhiên của kênh.

### Trong thực tế
Áp dụng DPA trong thực tế phức tạp hơn do khó xác định chính xác \(d_E\), SNR_Bob, SNR_Eve. Các phương pháp thực tế bao gồm:

1. **Xác định \(d_E\)**:
   - **Ước lượng**: BS không thể biết chính xác vị trí của Eve, nhưng có thể ước lượng dựa trên tín hiệu nhận được từ các thiết bị không xác định (nghi ngờ là Eve). Các kỹ thuật định vị vô tuyến (radio localization) như Time of Arrival (ToA) hoặc Received Signal Strength (RSS) được sử dụng.
   - **Giả định bảo mật**: Thường giả định Eve ở vị trí bất lợi nhất (gần BS hoặc có kênh tốt), dẫn đến việc tối ưu hóa cho trường hợp xấu nhất (worst-case scenario).
   - **Kịch bản động**: BS cập nhật ước lượng \(d_E\) dựa trên sự thay đổi của tín hiệu nhận được qua thời gian.

2. **Xác định SNR_Bob, SNR_Eve**:
   - **SNR_Bob**: BS thu thập CSI từ Bob1 và Bob2 qua tín hiệu pilot trên kênh ngược (uplink). SNR được tính dựa trên công suất tín hiệu nhận được so với nhiễu nền.
   - **SNR_Eve**: Nếu Eve là kẻ nghe lén thụ động, SNR_Eve khó xác định chính xác. Trong trường hợp này, BS có thể giả định SNR_Eve dựa trên mô hình thống kê hoặc sử dụng các kỹ thuật phát hiện kẻ nghe lén (eavesdropper detection) để ước lượng.
   - **Cảm biến môi trường**: Các hệ thống 5G/6G sử dụng cảm biến môi trường hoặc trí tuệ nhân tạo để phát hiện sự hiện diện của Eve và ước lượng SNR_Eve.

3. **Áp dụng DPA**:
   - **Thuật toán thời gian thực**: BS sử dụng các thuật toán tối ưu hóa (như Gradient Descent hoặc Heuristic) được tích hợp trong DSP để điều chỉnh \(\alpha_1\), \(\alpha_2\) dựa trên CSI của Bob và ước lượng của Eve.
   - **Cập nhật động**: \(\alpha_1\), \(\alpha_2\) được cập nhật theo chu kỳ truyền (thường vài mili giây trong 5G) để thích nghi với sự thay đổi của kênh.
   - **Kết hợp với AN**: BS đồng thời điều chỉnh \(\phi\) để tối ưu hóa hiệu quả bảo mật, sử dụng các thuật toán như Convex Optimization hoặc Reinforcement Learning.

4. **Thách thức thực tế**:
   - **CSI không hoàn hảo**: Sai số trong ước lượng CSI có thể làm giảm hiệu quả DPA.
   - **Tính toán phức tạp**: Các thuật toán như Convex Optimization đòi hỏi tài nguyên tính toán lớn, có thể không phù hợp với BS có năng lực hạn chế.
   - **Độ trễ**: Việc cập nhật \(\alpha_1\), \(\alpha_2\) cần được thực hiện nhanh để không làm gián đoạn liên kết.

## 3. Các thuật toán điều chỉnh hệ số \(\phi\) để đạt kết quả tối ưu

Trong bốn thuật toán đã đề cập (Gradient Descent, Convex Optimization, Heuristic, Reinforcement Learning), không phải tất cả đều trực tiếp điều chỉnh \(\phi\). Tuy nhiên, một số thuật toán có thể được mở rộng để tối ưu hóa đồng thời \(\alpha_1\), \(\alpha_2\), và \(\phi\). Dưới đây là phân tích:

1. **Gradient Descent**:
   - **Điều chỉnh \(\phi\)**: Có thể mở rộng để tối ưu hóa \(\phi\) bằng cách đưa \(\phi\) vào hàm mục tiêu, ví dụ:
     \[
     \max_{\alpha_1, \alpha_2, \phi} \min(R_{s1}, R_{s2}) \quad \text{s.t.} \quad \alpha_1 + \alpha_2 + \phi = 1, \quad \alpha_1, \alpha_2, \phi \geq 0
     \]
   - **Cách thực hiện**: Tính gradient của hàm mục tiêu theo \(\phi\) và cập nhật \(\phi\) cùng với \(\alpha_1\), \(\alpha_2\) trong mỗi vòng lặp.
   - **Ưu điểm**: Linh hoạt, có thể điều chỉnh cả \(\phi\) và \(\alpha_i\).
   - **Nhược điểm**: Tăng độ phức tạp tính toán, dễ rơi vào cực trị cục bộ.

2. **Convex Optimization**:
   - **Điều chỉnh \(\phi\)**: Đây là phương pháp phù hợp nhất để tối ưu hóa \(\phi\) cùng với \(\alpha_1\), \(\alpha_2\). Bài toán được định dạng lại:
     \[
     \max_{\alpha_1, \alpha_2, \phi} \min(R_{s1}, R_{s2}) \quad \text{s.t.} \quad \alpha_1 + \alpha_2 + \phi = 1, \quad \alpha_1, \alpha_2, \phi \geq 0
     \]
     Nếu hàm mục tiêu được xấp xỉ thành lồi, các công cụ như CVX có thể giải bài toán này hiệu quả.
   - **Ưu điểm**: Đảm bảo nghiệm tối ưu toàn cục nếu bài toán lồi.
   - **Nhược điểm**: Yêu cầu CSI chính xác và phức tạp tính toán.

3. **Heuristic**:
   - **Điều chỉnh \(\phi\)**: Có thể điều chỉnh \(\phi\) dựa trên quy tắc đơn giản, ví dụ: tăng \(\phi\) khi SNR_Eve cao hoặc \(d_E\) nhỏ để làm giảm \(C_E\). Ví dụ:
     \[
     \phi = \frac{\text{SNR}_E}{\text{SNR}_B + \text{SNR}_E} \cdot \phi_{\max}
     \]
   - **Ưu điểm**: Đơn giản, dễ triển khai.
   - **Nhược điểm**: Không đảm bảo tối ưu, phụ thuộc vào quy tắc được thiết kế.

4. **Reinforcement Learning (RL)**:
   - **Điều chỉnh \(\phi\)**: RL là phương pháp lý tưởng để điều chỉnh \(\phi\) trong môi trường động. Trạng thái bao gồm \(d_E\), SNR_Bob, SNR_Eve, và hành động bao gồm cả việc điều chỉnh \(\phi\).
   - **Cách thực hiện**:
     - **Trạng thái**: (\(d_E\), SNR_Bob, SNR_Eve, \(|h_{B1}|^2\), \(|h_{B2}|^2\), \(|h_E|^2\)).
     - **Hành động**: (\(\alpha_1\), \(\alpha_2\), \(\phi\)).
     - **Phần thưởng**: \(\min(R_{s1}, R_{s2}) - \lambda (\text{SOP}_1 + \text{SOP}_2)\).
   - **Ưu điểm**: Thích nghi tốt với CSI không hoàn hảo và môi trường động.
   - **Nhược điểm**: Cần thời gian huấn luyện và tài nguyên tính toán lớn.

### Đề xuất thuật toán điều chỉnh \(\phi\)
- **Convex Optimization** và **Reinforcement Learning** là hai phương pháp phù hợp nhất để điều chỉnh \(\phi\) cùng với \(\alpha_1\), \(\alpha_2\). Convex Optimization hiệu quả trong môi trường có CSI chính xác, trong khi RL phù hợp với các kịch bản động và CSI không hoàn hảo.
- **Pseudocode cho Convex Optimization với \(\phi\)**:
  ```
  Algorithm: Convex_Optimization_DPA_with_Phi
  Input: P_A, N_0, B, d_B1, d_B2, d_E, SNR_Bob, SNR_Eve, epsilon, alpha, N
  Output: alpha_1, alpha_2, phi optimal
  Begin:
    1. Define objective function: f = min(R_s1, R_s2)
    2. Define constraints: alpha_1 + alpha_2 + phi = 1, alpha_1, alpha_2, phi >= 0
    3. Use CVX to solve:
        maximize f
        subject to constraints
    4. Return alpha_1, alpha_2, phi
  End
  ```

### Tổng kết
- **Điều chỉnh \(\alpha_1\), \(\alpha_2\)** được thực hiện bởi BS thông qua DSP và RRM, dựa trên CSI từ người dùng.
- Trong mô phỏng, \(d_E\), SNR_Bob, SNR_Eve được giả định hoặc quét, còn trong thực tế, chúng được ước lượng qua tín hiệu pilot hoặc kỹ thuật định vị.
- Convex Optimization và Reinforcement Learning là các phương pháp tốt nhất để điều chỉnh đồng thời \(\alpha_1\), \(\alpha_2\), và \(\phi\), đảm bảo tối ưu hóa \(\min(R_{s1}, R_{s2})\) và các chỉ số bảo mật liên quan.