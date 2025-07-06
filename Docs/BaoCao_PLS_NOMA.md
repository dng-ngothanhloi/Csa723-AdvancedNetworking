# Báo Cáo Tổng Hợp: Đánh Giá Hiệu Năng Giải Pháp Bảo Mật Mạng NOMA

## 2.2 Cơ Sở Lý Thuyết Bảo Mật Tầng Vật Lý (PLS) trong Mạng NOMA
$$
### 2.2.1 Khái niệm bảo mật tầng vật lý (PLS)
Bảo mật tầng vật lý (Physical Layer Security - PLS) là một phương pháp bảo mật tận dụng các đặc tính vật lý của kênh truyền thông để ngăn chặn việc nghe lén hoặc xâm nhập trái phép mà không phụ thuộc vào các thuật toán mã hóa truyền thống. Trong hệ thống truyền thông không dây, PLS sử dụng các đặc điểm như nhiễu, suy hao kênh, hoặc tính ngẫu nhiên của kênh để đảm bảo tính bí mật của thông tin. 

Các nguyên tắc cơ bản của PLS bao gồm:
- **Tối ưu hóa dung lượng bí mật (secrecy capacity):** Đây là mức chênh lệch giữa dung lượng kênh của người dùng hợp pháp (legitimate user) và kẻ nghe lén (eavesdropper). Dung lượng bí mật được định nghĩa như sau:

  $$  C_s = \max(0, C_m - C_e) $$


  Trong đó, $$(C_m$$ là dung lượng kênh chính (main channel) và $$C_e$$ là dung lượng kênh của kẻ nghe lén (eavesdropping channel).

- **Kỹ thuật mã hóa kênh:** Sử dụng các mã như mã LDPC hoặc mã Polar để tăng cường bảo mật bằng cách làm giảm khả năng giải mã thành công của kẻ nghe lén.
- **Tận dụng nhiễu:** Nhiễu tự nhiên hoặc nhiễu nhân tạo (artificial noise) được thêm vào tín hiệu để làm giảm tỷ lệ tín hiệu trên nhiễu (SNR) tại kẻ nghe lén, trong khi vẫn đảm bảo chất lượng tín hiệu tại người dùng hợp pháp.

### 2.2.2 Ứng dụng PLS trong mạng NOMA
Trong mạng NOMA (Non-Orthogonal Multiple Access), nhiều người dùng được phục vụ đồng thời trên cùng một tài nguyên tần số/thời gian thông qua phân bổ công suất khác nhau. Điều này tạo ra thách thức về bảo mật do tín hiệu của các người dùng được truyền đồng thời, làm tăng nguy cơ bị nghe lén. PLS trong NOMA tập trung vào các kỹ thuật sau:

- **Phân bổ công suất tối ưu:** Trong NOMA, người dùng có điều kiện kênh tốt hơn (strong user) được phân bổ công suất thấp hơn, trong khi người dùng có điều kiện kênh yếu hơn (weak user) được phân bổ công suất cao hơn. Điều này có thể được khai thác để tăng dung lượng bí mật bằng cách làm giảm SNR tại kẻ nghe lén.
- **Tín hiệu nhiễu nhân tạo (Artificial Noise - AN):** Trạm gốc (BS) có thể truyền thêm tín hiệu nhiễu vào không gian vô hiệu (null space) của kênh người dùng hợp pháp để làm giảm khả năng giải mã của kẻ nghe lén mà không ảnh hưởng đến người dùng hợp pháp.
- **Kỹ thuật beamforming:** Sử dụng beamforming để định hướng tín hiệu đến người dùng hợp pháp, giảm thiểu rò rỉ tín hiệu đến kẻ nghe lén.
- **Sử dụng mô hình kênh ngẫu nhiên:** Các đặc tính ngẫu nhiên của kênh không dây (như fading) được khai thác để tạo ra sự khác biệt giữa kênh hợp pháp và kênh nghe lén, từ đó tăng cường bảo mật.

### 2.2.3 Mô hình toán học cơ bản của PLS trong NOMA
Trong một hệ thống NOMA với một trạm gốc (BS), hai người dùng hợp pháp ($$U_1$$, $$U_2$$) và một kẻ nghe lén ($$E$$), mô hình toán học cơ bản của bảo mật tầng vật lý (PLS) được xây dựng dựa trên các đặc tính của kênh và các metric đánh giá hiệu năng bảo mật.

#### Mô hình tín hiệu
Tín hiệu truyền từ trạm gốc (BS) được biểu diễn như sau:
$$
x = \sqrt{P_1}s_1 + \sqrt{P_2}s_2
$$
Trong đó:
- $$P_1, P_2$$: Công suất phân bổ cho tín hiệu $$s_1, s_2$$ của người dùng $$U_1, U_2$$.
- $$s_1, s_2$$: Tín hiệu dữ liệu dành cho $$U_1, U_2$$, với $$E[|s_i|^2] = 1$$.

Tín hiệu nhận được tại người dùng $$U_1$$ (strong user) và $$U_2$$ (weak user):
$$
y_1 = h_1 (\sqrt{P_1}s_1 + \sqrt{P_2}s_2) + n_1
$$
$$
y_2 = h_2 (\sqrt{P_1}s_1 + \sqrt{P_2}s_2) + n_2
$$
Tín hiệu nhận được tại kẻ nghe lén ($$E$$):
$$
y_e = h_e (\sqrt{P_1}s_1 + \sqrt{P_2}s_2) + n_e
$$
Trong đó:
- $$h_1, h_2, h_e$$: Hệ số kênh fading của $$U_1, U_2$$ và $$E$$.
- $$n_1, n_2, n_e$$: Nhiễu Gaussian trắng với phương sai $$\sigma^2$$.

Người dùng $$U_1$$ thực hiện giải mã tín hiệu của $$U_2$$ trước (theo nguyên lý SIC - Successive Interference Cancellation), sau đó loại bỏ tín hiệu của $$U_2$$ để giải mã tín hiệu của mình. Người dùng $$U_2$$ coi tín hiệu của $$U_1$$ như nhiễu.

#### Metric đánh giá bảo mật
Các metric chính để đánh giá hiệu năng bảo mật trong mạng NOMA bao gồm:

1. **Dung lượng bí mật (Secrecy Capacity):**
Dung lượng bí mật của người dùng $$U_i$$ được định nghĩa là mức chênh lệch giữa dung lượng kênh chính (main channel) và kênh nghe lén (eavesdropping channel):
$$
C_{s,i} = \max(0, C_{m,i} - C_{e,i})
$$
Trong đó:
- $$C_{m,i}$$: Dung lượng kênh của người dùng hợp pháp $$U_i$$.
- $$C_{e,i}$$: Dung lượng kênh của kẻ nghe lén khi cố gắng giải mã tín hiệu của $$U_i$$.

Cụ thể, dung lượng kênh của $$U_1$$ và $$U_2$$ được tính như sau:
- Dung lượng kênh chính của $$U_1$$ (sau khi áp dụng SIC):
$$
C_{m,1} = \log_2\left(1 + \frac{|h_1|^2 P_1}{\sigma^2}\right)
$$
- Dung lượng kênh chính của $$U_2$$:
$$
C_{m,2} = \log_2\left(1 + \frac{|h_2|^2 P_2}{|h_2|^2 P_1 + \sigma^2}\right)
$$
- Dung lượng kênh nghe lén khi $$E$$ cố gắng giải mã tín hiệu của $$U_1$$:
$$
C_{e,1} = \log_2\left(1 + \frac{|h_e|^2 P_1}{|h_e|^2 P_2 + \sigma^2}\right)
$$
- Dung lượng kênh nghe lén khi $$E$$ cố gắng giải mã tín hiệu của $$U_2$$:
$$
C_{e,2} = \log_2\left(1 + \frac{|h_e|^2 P_2}{|h_e|^2 P_1 + \sigma^2}\right)
$$

Dung lượng bí mật của $$U_1$$ và $$U_2$$:
$$
C_{s,1} = \max\left(0, \log_2\left(1 + \frac{|h_1|^2 P_1}{\sigma^2}\right) - \log_2\left(1 + \frac{|h_e|^2 P_1}{|h_e|^2 P_2 + \sigma^2}\right)\right)
$$
$$
C_{s,2} = \max\left(0, \log_2\left(1 + \frac{|h_2|^2 P_2}{|h_2|^2 P_1 + \sigma^2}\right) - \log_2\left(1 + \frac{|h_e|^2 P_2}{|h_e|^2 P_1 + \sigma^2}\right)\right)
$$

2. **Tổng dung lượng bí mật (Sum Secrecy Capacity):**
Tổng dung lượng bí mật của hệ thống là tổng dung lượng bí mật của tất cả người dùng:
$$
C_s^{\text{sum}} = C_{s,1} + C_{s,2}
$$

3. **Xác suất chặn bí mật (Secrecy Outage Probability - SOP):**
Xác suất chặn bí mật đo lường xác suất mà dung lượng bí mật của một người dùng nhỏ hơn một ngưỡng dung lượng bí mật mục tiêu $$R_s$$. Đối với $$U_i$$, SOP được định nghĩa như:
$$
P_{\text{out},i} = P(C_{s,i} < R_s) = P\left(\log_2\left(1 + \frac{|h_i|^2 P_i}{|h_i|^2 P_j + \sigma^2}\right) - \log_2\left(1 + \frac{|h_e|^2 P_i}{|h_e|^2 P_j + \sigma^2}\right) < R_s\right)
$$
Trong đó, $$j \neq i$$. SOP thường được tính toán dựa trên phân phối xác suất của các hệ số kênh $$h_i, h_e$$ (ví dụ, kênh Rayleigh hoặc Rician fading).

4. **Tỷ lệ lỗi bit bí mật (Secrecy Bit Error Rate - SBER):**
SBER đo lường tỷ lệ lỗi bit tại kẻ nghe lén so với người dùng hợp pháp. Một hệ thống bảo mật hiệu quả sẽ có SBER cao tại kẻ nghe lén, đảm bảo rằng thông tin bị giải mã sai lệch.

#### Công thức tính độ bảo mật
Độ bảo mật của mạng NOMA thường được đánh giá thông qua **tỷ lệ dung lượng bí mật trung bình** (average secrecy rate), được tính bằng cách lấy kỳ vọng của dung lượng bí mật:
$$
\bar{C}_{s,i} = E[C_{s,i}] = E\left[\max\left(0, \log_2\left(1 + \frac{|h_i|^2 P_i}{|h_i|^2 P_j + \sigma^2}\right) - \log_2\left(1 + \frac{|h_e|^2 P_i}{|h_e|^2 P_j + \sigma^2}\right)\right)\right]
$$
Trong đó, kỳ vọng $$E[\cdot]$$ được tính dựa trên phân phối xác suất của các hệ số kênh $$h_i, h_e$$.

Trong trường hợp sử dụng nhiễu nhân tạo (AN), tín hiệu truyền có thể được sửa đổi như sau:
$$
x = \sqrt{P_1}s_1 + \sqrt{P_2}s_2 + \sqrt{P_n}v
$$
Trong đó, $$v$$ là tín hiệu nhiễu nhân tạo với $$E[|v|^2] = 1$$, và $$P_n$$ là công suất dành cho nhiễu. Tín hiệu nhận tại kẻ nghe lén trở thành:
$$
y_e = h_e (\sqrt{P_1}s_1 + \sqrt{P_2}s_2 + \sqrt{P_n}v) + n_e
$$
Điều này làm giảm dung lượng kênh nghe lén:
$$
C_{e,i} = \log_2\left(1 + \frac{|h_e|^2 P_i}{|h_e|^2 (P_j + P_n) + \sigma^2}\right)
$$
Do đó, dung lượng bí mật tăng lên nhờ sự suy giảm của $$C_{e,i}$$.

### 2.2.4 Ưu điểm và thách thức của PLS trong NOMA
- **Ưu điểm:**
  - Không phụ thuộc vào khả năng tính toán của kẻ nghe lén.
  - Tận dụng các đặc tính vật lý tự nhiên của kênh, giảm chi phí triển khai so với mã hóa cấp cao.
  - Phù hợp với các hệ thống không dây hiện đại như 5G, IoT.

- **Thách thức:**
  - Sự phức tạp trong việc phân bổ công suất và thiết kế tín hiệu nhiễu.
  - Yêu cầu thông tin trạng thái kênh (CSI) chính xác, đặc biệt là kênh của kẻ nghe lén.
  - Khả năng mở rộng cho hệ thống với số lượng lớn người dùng.

---

## 2.3 Tổng Quan Các Nghiên Cứu về Ảnh Hưởng Nghe Lén và Ảnh Hưởng Nghe Lén trong NOMA

### 2.3.1 Tổng quan về nghe lén trong hệ thống không dây
Nghe lén (eavesdropping) là hành vi một thực thể trái phép cố gắng chặn và giải mã thông tin từ kênh truyền thông. Trong hệ thống không dây, nghe lén trở thành một vấn đề nghiêm trọng do bản chất mở của môi trường truyền dẫn. Các nghiên cứu về nghe lén tập trung vào các khía cạnh sau:

- **Mô hình kẻ nghe lén:**
  - **Nghe lén thụ động (Passive Eavesdropping):** Kẻ nghe lén chỉ thu nhận tín hiệu mà không can thiệp vào kênh.
  - **Nghe lén chủ động (Active Eavesdropping):** Kẻ nghe lén cố gắng can thiệp vào kênh, ví dụ bằng cách gửi tín hiệu nhiễu hoặc giả mạo người dùng hợp pháp.
  
- **Ảnh hưởng của nghe lén:**
  - Làm giảm dung lượng bí mật của hệ thống.
  - Gây mất mát thông tin hoặc rò rỉ dữ liệu nhạy cảm.
  - Tăng độ phức tạp trong thiết kế hệ thống bảo mật.

- **Các kỹ thuật chống nghe lén:**
  - Mã hóa tín hiệu ở tầng vật lý.
  - Sử dụng nhiễu nhân tạo hoặc kỹ thuật beamforming.
  - Tận dụng các kỹ thuật học máy để phát hiện hành vi nghe lén.

### 2.3.2 Ảnh hưởng của nghe lén trong mạng NOMA
Trong mạng NOMA, nghe lén gây ra những thách thức đặc thù do đặc điểm phân bổ công suất và truyền tín hiệu đồng thời:

- **Tăng nguy cơ nghe lén do truyền tín hiệu đồng thời:** Vì tất cả người dùng trong NOMA chia sẻ cùng tài nguyên tần số, kẻ nghe lén có thể dễ dàng thu nhận tín hiệu của nhiều người dùng, làm tăng khả năng giải mã thành công.
- **Tác động của nhiễu liên người dùng (Inter-User Interference):** Trong NOMA, nhiễu giữa các người dùng có thể bị kẻ nghe lén khai thác để tách tín hiệu của từng người dùng.
- **Khó khăn trong việc xác định kênh nghe lén:** Thông tin trạng thái kênh (CSI) của kẻ nghe lén thường không có sẵn hoặc không chính xác, làm phức tạp hóa việc thiết kế các giải pháp bảo mật.

### 2.3.3 Tổng quan các nghiên cứu về bảo mật trong NOMA dưới ảnh hưởng nghe lén
Nhiều nghiên cứu đã được thực hiện để giải quyết vấn đề nghe lén trong mạng NOMA, tập trung vào các hướng sau:

1. **Nghiên cứu về phân bổ công suất:**
   - Zhang et al. (2017) đề xuất một phương pháp phân bổ công suất tối ưu dựa trên tối đa hóa dung lượng bí mật tổng của hệ thống NOMA, sử dụng thuật toán tối ưu lồi.
   - Liu et al. (2018) nghiên cứu việc sử dụng nhiễu nhân tạo kết hợp với phân bổ công suất để làm giảm SNR tại kẻ nghe lén.

2. **Nghiên cứu về kỹ thuật beamforming:**
   - Zhu et al. (2019) áp dụng kỹ thuật beamforming để định hướng tín hiệu đến người dùng hợp pháp, giảm thiểu rò rỉ tín hiệu đến kẻ nghe lén.
   - Nghiên cứu của Li et al. (2020) đề xuất sử dụng beamforming dựa trên thông tin CSI không hoàn hảo để cải thiện hiệu năng bảo mật.

3. **Nghiên cứu về nhiễu nhân tạo:**
   - Lv et al. (2018) đề xuất phương pháp chèn nhiễu nhân tạo vào không gian vô hiệu của kênh người dùng hợp pháp, đảm bảo tín hiệu nhiễu không ảnh hưởng đến người dùng hợp pháp nhưng làm giảm chất lượng tín hiệu tại kẻ nghe lén.

4. **Nghiên cứu dựa trên học máy:**
   - Các nghiên cứu gần đây (2021-2023) ứng dụng học sâu (deep learning) để dự đoán hành vi nghe lén và tối ưu hóa các tham số hệ thống như công suất và beamforming.

5. **Mô phỏng và đánh giá hiệu năng:**
   - Các nghiên cứu sử dụng MATLAB để mô phỏng hiệu năng của các giải pháp bảo mật trong NOMA, tập trung vào các chỉ số như dung lượng bí mật, tỷ lệ lỗi bit (BER), và xác suất chặn (outage probability). Các mô phỏng thường giả định kênh Rayleigh hoặc Rician fading để đánh giá hiệu quả của các kỹ thuật PLS.

### 2.3.4 Hướng nghiên cứu mở
- **Tích hợp học máy và trí tuệ nhân tạo:** Phát triển các thuật toán học máy để dự đoán và phát hiện kẻ nghe lén trong thời gian thực.
- **Bảo mật trong NOMA đa anten:** Nghiên cứu các kỹ thuật MIMO-NOMA để tăng cường bảo mật thông qua việc khai thác đa dạng không gian.
- **Tối ưu hóa năng lượng:** Kết hợp các giải pháp bảo mật với các kỹ thuật tiết kiệm năng lượng để phù hợp với các ứng dụng IoT.
- **Mô phỏng thực tế hơn:** Xây dựng các mô hình mô phỏng phức tạp hơn, bao gồm nhiều kẻ nghe lén hoặc các kịch bản di động (mobile scenarios).