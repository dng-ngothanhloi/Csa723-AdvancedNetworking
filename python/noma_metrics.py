import numpy as np

def secrecy_rate(sinr_leg, sinr_eve):
    return max(0, np.log2(1 + sinr_leg) - np.log2(1 + sinr_eve))

def secrecy_outage_probability(Rs_list, R_th):
    Rs_arr = np.array(Rs_list)
    return np.mean(Rs_arr < R_th)

def secrecy_spectral_efficiency(Rs, B):
    return Rs / B 