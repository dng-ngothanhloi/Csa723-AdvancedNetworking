# Baseline Simulation for NOMA Security (Python)

## Mô tả
Mô phỏng baseline (không AN/DPC) cho hệ thống NOMA với kẻ nghe lén chủ động bằng Python. Có thể chạy trên local Jupyter Notebook hoặc Google Colab.

## Cách sử dụng

### 1. Chạy trên local (Jupyter Notebook)
```bash
pip install numpy matplotlib
jupyter notebook baseline_simulation.ipynb
```

### 2. Chạy trên Google Colab
- Upload file `baseline_simulation.ipynb` lên Google Drive hoặc GitHub.
- Truy cập [colab.research.google.com](https://colab.research.google.com)
- Chọn "File > Open notebook" và chọn từ Drive hoặc dán link GitHub.
- Chạy từng cell để xem kết quả.

### 3. Kết quả
- Biểu đồ Secrecy Rate baseline sẽ được hiển thị và lưu tại `results/baseline_results.png`.

## Mở rộng
- Có thể chỉnh sửa tham số mô phỏng, số user, số anten, số lần lặp, v.v.
- Có thể thêm các chỉ số khác như SOP, hiệu suất phổ bí mật, hoặc mô phỏng các giải pháp AN/DPC.

## Chia sẻ & làm việc nhóm
- Để làm việc nhóm, chỉ cần chia sẻ file notebook qua Google Drive hoặc GitHub.
- Mọi thành viên đều có thể mở, chỉnh sửa, chạy lại trên Google Colab.

## Lưu ý khi cài đặt Jupyter Notebook
Nếu bạn gặp lỗi `command not found: jupyter`, hãy cài đặt Jupyter Notebook như sau:

### Cài đặt bằng pip (khuyên dùng)
```bash
pip install notebook
```
Hoặc nếu dùng Python 3:
```bash
pip3 install notebook
```

Sau đó chạy lại:
```bash
jupyter notebook
```

### Cài đặt bằng Anaconda (nếu đã cài Anaconda/Miniconda)
```bash
conda install notebook
```

Nếu vẫn gặp lỗi, hãy kiểm tra biến PATH hoặc tham khảo thêm tài liệu chính thức của Jupyter: https://jupyter.org/install 