import matplotlib.pyplot as plt
import numpy as np

def plot_os_vs_distance(d_AE_range, O_S_matrix, labels, colors=None, regions=None, region_labels=None, R_th=0.5):
    plt.figure(figsize=(10,6))
    # Vẽ vùng màu nếu có
    if regions is not None:
        for i, (ymin, ymax, color) in enumerate(regions):
            plt.fill_between(d_AE_range, ymin, ymax, color=color, alpha=0.2)
            if region_labels and i < len(region_labels):
                plt.text(d_AE_range[-1]+5, (ymin+ymax)/2, region_labels[i], va='center')
    # Vẽ các đường O_S
    for i, O_S in enumerate(O_S_matrix):
        plt.plot(d_AE_range, O_S, label=labels[i], linewidth=2, color=None if colors is None else colors[i])
    # Đường ngưỡng R_th
    plt.axhline(R_th, color='k', linestyle='--')
    plt.text(d_AE_range[-1], R_th+0.01, f'$O_S = {R_th}$', va='bottom', ha='right')
    plt.xlabel('Khoảng cách từ A đến E ($d_{AE}$, m)')
    plt.ylabel('Xác suất dừng bảo mật $O_S$')
    plt.title('Biểu diễn xác suất dừng bảo mật theo khoảng cách')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show() 