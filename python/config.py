# Tham số vật lý & hệ thống
N_USERS = 2
N_ANT_LIST = [1, 4, 16]  # Có thể thử nhiều cấu hình anten
P_BS = 1  # normalized power
SNR_DB_LIST = [0, 10, 20]  # dB, nhiều giá trị SNR
D_AE_RANGE = list(range(20, 501, 10))  # Khoảng cách từ 20m đến 500m
ALPHA = 3  # Hệ số suy hao đường truyền
D0 = 1     # Khoảng cách tham chiếu (m)
N_ITER = 1000

# Tham số bảo mật
R_TH = 0.5  # Ngưỡng secrecy rate (bit/s/Hz)
B = 10e6    # Băng thông (Hz) 