import numpy as np

def generate_rayleigh_channel(n_users, n_ant):
    return (np.random.randn(n_users, n_ant) + 1j*np.random.randn(n_users, n_ant)) / np.sqrt(2)

def generate_rician_channel(n_users, n_ant, K=10):
    LOS = np.ones((n_users, n_ant))
    NLOS = (np.random.randn(n_users, n_ant) + 1j*np.random.randn(n_users, n_ant)) / np.sqrt(2)
    return np.sqrt(K/(K+1))*LOS + np.sqrt(1/(K+1))*NLOS

def path_loss(d, d0=1, alpha=3):
    """
    d: khoảng cách (m)
    d0: khoảng cách tham chiếu (m)
    alpha: hệ số suy hao đường truyền
    """
    return (d / d0) ** (-alpha) 