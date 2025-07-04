# Tác động của nhiễu nhân tạo (AN) trong hệ thống NOMA

## Bảng so sánh các metric bảo mật với AN (beta = 0.2)

| **Metric**   | **Kịch bản 3 (d_E = 50 m)** | **Kịch bản 2 (SNR_Bob = 20 dB, SNR_Eve = 10 dB)** | **Tác động của AN** |
|--------------|-----------------------------|--------------------------------------------------|---------------------|
| **C_B1 (Mbps)** | 54.55                      | 52.83                                           | Giảm ~20% do công suất hữu ích giảm (P_s = 0.8 W). Vẫn đảm bảo QoS tốt (>50 Mbps). |
| **C_B2 (Mbps)** | 337.77                     | 61.06                                           | Giảm ~20%, ảnh hưởng nặng hơn ở Kịch bản 2 do SNR_Bob thấp. QoS tốt ở Kịch bản 3. |
| **C_E (Mbps)** | 19.25                      | 19.09                                           | Giảm ~20-30% so với không AN, làm suy giảm khả năng giải mã của Eve. |
| **BER_B1**   | 0.4986                     | 0.5085                                          | Tăng nhẹ (~0.49-0.51), không cải thiện do AN và nhiễu SIC. |
| **BER_B2**   | 0.4996                     | 0.5010                                          | Tăng nhẹ, tương tự BER_B1. Bob2 chịu ảnh hưởng SIC nhiều hơn. |
| **BER_E**    | 0.4999                     | 0.5027                                          | Cao (~0.50), gần ngẫu nhiên, AN làm giảm khả năng giải mã của Eve. |
| **R_s1 (bits/s/Hz)** | 4.32               | 4.16                                            | Tăng do C_E giảm, đảm bảo bảo mật tốt cho Bob1 (> R_th = 1.0). |
| **R_s2 (bits/s/Hz)** | 31.85              | 4.20                                            | Tăng đáng kể ở Kịch bản 3 do C_B2 cao, hạn chế ở Kịch bản 2 do SNR_Bob thấp. |
| **SOP1**     | 0.00                       | 0.00                                            | Bằng 0, AN đảm bảo tốc độ bảo mật của Bob1 trên ngưỡng R_th. |
| **SOP2**     | 0.00                       | 0.00                                            | Bằng 0 ở Kịch bản 3, cao ở SNR_Bob thấp trong Kịch bản 2. AN hiệu quả hơn ở SNR_Bob cao. |
| **IP1**      | 0.00                       | 0.00                                            | Bằng 0, AN ngăn Eve chặn tín hiệu Bob1 hoàn toàn. |
| **IP2**      | 0.00                       | 0.00                                            | Bằng 0 ở Kịch bản 3, cao ở SNR_Bob thấp trong Kịch bản 2. AN hiệu quả hơn ở SNR_Bob cao. |
| **eta_s1 (bits/s/Hz)** | 4.32e-07         | 4.16e-07                                        | Tăng tương ứng R_s1, cải thiện hiệu suất phổ bí mật cho Bob1. |
| **eta_s2 (bits/s/Hz)** | 3.19e-06         | 4.20e-07                                        | Tăng mạnh ở Kịch bản 3, hạn chế ở Kịch bản 2 do R_s2 thấp. |

## Phân tích tác động của AN
- **Tích cực**:
  - **Giảm C_E**: AN (beta = 0.2) giảm dung lượng kênh của Eve khoảng 20-30% (từ ~24-30 Mbps xuống ~19 Mbps), làm suy giảm khả năng giải mã của Eve.
  - **Tăng BER_E**: BER_E ~0.50, gần ngẫu nhiên, cho thấy AN làm tín hiệu tại Eve khó giải mã.
  - **Tăng R_s1, R_s2**: Tốc độ bảo mật tăng đáng kể (R_s1 ~4 bits/s/Hz, R_s2 ~4-32 bits/s/Hz), đặc biệt ở Kịch bản 3 do C_E thấp và C_B2 cao.
  - **Giảm SOP1, SOP2, IP1, IP2**: AN giữ SOP1, SOP2, IP1, IP2 bằng 0 ở Kịch bản 3 và SNR_Bob ≥ 10 dB trong Kịch bản 2, đảm bảo bảo mật cao.
  - **Tăng eta_s1, eta_s2**: Hiệu suất phổ bí mật được cải thiện, đặc biệt ở Kịch bản 3 (eta_s2 ~3e-06 bits/s/Hz).

- **Tiêu cực**:
  - **Giảm C_B1, C_B2**: AN làm giảm công suất hữu ích (~20%), dẫn đến C_B1, C_B2 thấp hơn so với không AN, đặc biệt ở SNR_Bob thấp (Kịch bản 2).
  - **Không cải thiện BER_B1, BER_B2**: AN và nhiễu SIC làm BER_B1, BER_B2 ~0.49-0.51, không đạt mức lý tưởng (<0.1).
  - **Hạn chế ở SNR_Bob thấp**: Ở Kịch bản 2 với SNR_Bob ≤ 6 dB, R_s2 ~0, SOP2 ~1, IP2 ~0.95-0.97, cho thấy bảo mật của Bob2 yếu do SNR thấp và nhiễu SIC.

## Kết luận
Nhiễu nhân tạo (AN) với beta = 0.2 hiệu quả trong việc tăng cường bảo mật cho Bob1 và Bob2, đặc biệt ở Kịch bản 3 (SNR_Bob cao, d_E thay đổi) và SNR_Bob ≥ 10 dB trong Kịch bản 2. AN làm giảm đáng kể C_E, tăng BER_E, R_s1, R_s2, eta_s1, eta_s2, và giữ SOP1, SOP2, IP1, IP2 ở mức rất thấp. Tuy nhiên, ở SNR_Bob thấp, bảo mật của Bob2 bị hạn chế do nhiễu SIC và khoảng cách xa. Để tối ưu, cần cân nhắc điều chỉnh beta hoặc áp dụng kỹ thuật giảm nhiễu SIC.