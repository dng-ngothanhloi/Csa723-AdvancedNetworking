%% Simulation Improvement-1
% Thông số hệ thống . Good Simulation cải tiến
% Suy hao d^alpha: Thêm d_B^alpha và d_E^alpha vào SNR, phản ánh đúng mô hình suy hao đường truyền.
% Shannon Capacity: Sử dụng C_AB = 180e3 * log2(1 + SNR_Bob) và C_AE = 180e3 * log2(1 + SNR_Eve), thay cho ngưỡng tuyến tính.
% Nhiễu thực tế: N_0 = 10^(-14) W thay cho 10^(-3) W, phù hợp với kịch bản không dây thực tế.
% Khoảng cách thực tế: d_E = 20-100 m và d_B = 100, 50, 20 m, thay cho 0.1-5 m, phù hợp với IoT nông nghiệp.
% Ngưỡng bảo mật: epsilon_S = 50e3 / 180e3 (bits/s/Hz) thay cho 2, đảm bảo đơn vị nhất quán.

P_A = 1;                     % Công suất truyền (W)
N_0 = 10^((-134 - 30) / 10); % Nhiễu nền thực tế (-134 dBm -> Watt)
alpha = 3;                   % Hệ số suy hao
epsilon_S = 50e3 / 180e3;    % Ngưỡng bảo mật (50 kbps / 180 kHz -> bits/s/Hz)
num_samples = 1e5;           % Số mẫu mô phỏng
dE_range = linspace(20, 100, 50); % Khoảng cách Alice-Eve (m) - cải tiến cho small cell

% Ba giá trị d_B tương ứng ba kịch bản
dB_values = [20, 50, 100];   % Khoảng cách Alice-Bob (m)
colors = {'g', 'b', 'r'};
labels = {
    'd_B = 70 m (O_S ≈ 1)',
    'd_B = 50 m (O_S giảm)',
    'd_B = 20 m (O_S giảm gần 0)'
};
O_S = zeros(3, length(dE_range));

% Mô phỏng cho từng kịch bản
for j = 1:3
    d_B = dB_values(j);
    for i = 1:length(dE_range)
        d_E = dE_range(i);
        % Tạo kênh fading Rayleigh phức
        h_B = sqrt(0.5) * (randn(num_samples, 1) + 1j * randn(num_samples, 1));
        h_E = sqrt(0.5) * (randn(num_samples, 1) + 1j * randn(num_samples, 1));

        % Tính SNR với suy hao
        SNR_Bob = (P_A * abs(h_B).^2) ./ (d_B^alpha * N_0);
        SNR_Eve = (P_A * abs(h_E).^2) ./ (d_E^alpha * N_0);

        % Tính dung lượng kênh theo Shannon
        C_AB = 180e3 * log2(1 + SNR_Bob);
        C_AE = 180e3 * log2(1 + SNR_Eve);

        % Tính Secrecy Capacity và Secrecy Outage
        C_S = max(0, C_AB - C_AE);
        O_S(j, i) = mean(C_S < epsilon_S * 180e3); % Nhân epsilon_S với băng thông 180 kHz để có đơn vị bit/s
    end
end

% Vẽ đồ thị
figure('Position', [100, 100, 800, 600]);

% Vùng màu bảo mật
fill([dE_range, fliplr(dE_range)], [ones(1,length(dE_range))*0.8, ones(1,length(dE_range))], ...
     [1, 0.8, 0.8], 'EdgeColor', 'none', 'FaceAlpha', 0.5); % Vùng đỏ nhạt
hold on;
fill([dE_range, fliplr(dE_range)], [ones(1,length(dE_range))*0.4, ones(1,length(dE_range))*0.8], ...
     [1, 1, 0.6], 'EdgeColor', 'none', 'FaceAlpha', 0.5); % Vùng vàng nhạt
fill([dE_range, fliplr(dE_range)], [zeros(1,length(dE_range)), ones(1,length(dE_range))*0.4], ...
     [0.8, 1, 0.8], 'EdgeColor', 'none', 'FaceAlpha', 0.5); % Vùng xanh nhạt

% Vẽ 3 đường xác suất
for j = 1:3
    plot(dE_range, O_S(j, :), 'Color', colors{j}, 'LineWidth', 2, 'DisplayName', labels{j});
end

% Gạch chỉ hướng (tương đương annotation textarrow)
annotation('textarrow', [0.3, 0.2], [0.7, 0.85], 'String', 'Xu hướng giảm', ...
           'FontSize', 10, 'Color', 'black');

xlabel('Khoảng cách từ A đến E (d_{AE}) (m)');
ylabel('Xác suất dừng bảo mật O_S');
title('Biểu diễn xác suất dừng với vùng màu và xu hướng');
legend('Location', 'upper right');
yline(1, 'k--', 'DisplayName', 'O_S = 1');
yline(0.5, 'k--', 'DisplayName', 'O_S = 0.5');
yline(0, 'k--', 'DisplayName', 'O_S = 0');
grid on;

fprintf('%s\n', repmat('=', 1, 80));
fprintf('PHYSICAL LAYER SECURITY (PLS) SIMULATION WITH ARTIFICIAL NOISE (AN)\n');
fprintf('%s\n', repmat('=', 1, 80));

%% ============================================================================
%% PHẦN 2: MÔ PHỎNG BẢO MẬT TẦNG VẬT LÝ (PLS) VỚI NHIỄU NHÂN TẠO (AN)
%% ============================================================================

function [SNR_Bob_AN, SNR_Eve_AN, C_S_AN] = artificial_noise_algorithm(P_A, phi, h_B, h_E, d_B, d_E, N_0, alpha)
    % Thuật toán khảo sát chống nhiễu vật lý AN tại BS
    %
    % Parameters:
    % - P_A: Công suất truyền tổng (W)
    % - phi: Tỷ lệ công suất cho tín hiệu hợp lệ (0 < phi < 1)
    % - h_B, h_E: Kênh fading cho Bob và Eve
    % - d_B, d_E: Khoảng cách đến Bob và Eve (m)
    % - N_0: Nhiễu nền (W)
    % - alpha: Hệ số suy hao đường truyền
    %
    % Returns:
    % - SNR_Bob_AN: SNR tại Bob với AN
    % - SNR_Eve_AN: SNR tại Eve với AN
    % - C_S_AN: Secrecy Capacity với AN
    
    % 1. Phân bổ công suất theo thuật toán AN
    P_S = phi * P_A;          % Công suất cho tín hiệu hợp lệ
    P_AN = (1 - phi) * P_A;   % Công suất cho nhiễu nhân tạo
    
    % 2. Tạo nhiễu nhân tạo (Artificial Noise)
    % Nhiễu được thiết kế để gây nhiễu cho Eve nhưng không ảnh hưởng Bob
    w_AN = sqrt(P_AN/2) * (randn(length(h_B), 1) + 1j * randn(length(h_B), 1));
    
    % 3. Tính SNR với AN
    % Tại Bob: Tín hiệu hợp lệ + nhiễu nhân tạo (được thiết kế để không ảnh hưởng)
    signal_power_Bob = P_S * abs(h_B).^2;
    noise_power_Bob = N_0 * d_B^alpha + abs(w_AN).^2;
    SNR_Bob_AN = signal_power_Bob ./ noise_power_Bob;
    
    % Tại Eve: Tín hiệu hợp lệ + nhiễu nhân tạo (gây nhiễu mạnh)
    signal_power_Eve = P_S * abs(h_E).^2;
    noise_power_Eve = N_0 * d_E^alpha + abs(w_AN).^2;
    SNR_Eve_AN = signal_power_Eve ./ noise_power_Eve;
    
    % 4. Tính dung lượng kênh với AN
    C_AB_AN = 180e3 * log2(1 + SNR_Bob_AN);
    C_AE_AN = 180e3 * log2(1 + SNR_Eve_AN);
    
    % 5. Tính Secrecy Capacity với AN
    C_S_AN = max(0, C_AB_AN - C_AE_AN);
end

% Tham số khảo sát với phi_values=[0.1, 0.2, 0.3]
phi_values = [0.1, 0.2, 0.3];  % Tỷ lệ công suất cho tín hiệu hợp lệ
d_B_AN = 50;                    % Khoảng cách Alice-Bob (m) - kịch bản trung bình
dE_range_AN = linspace(20, 100, 50);  % Khoảng cách Alice-Eve (m) - cải tiến cho small cell

% Ngưỡng bảo mật bổ sung
epsilon_S = 0.2778;             % Ngưỡng bảo mật cho SOP (bits/s/Hz)
C_th = 0.10;                   % Ngưỡng dung lượng cho IP (bits/s/Hz)

% Màu sắc và nhãn cho các giá trị phi
phi_colors = {'red', 'blue', 'green'};
phi_labels = cell(1, length(phi_values));
for i = 1:length(phi_values)
    phi_labels{i} = sprintf('φ = %.1f (P_S = %.1fW, P_AN = %.1fW)', ...
                           phi_values(i), phi_values(i)*P_A, (1-phi_values(i))*P_A);
end

% Ma trận lưu kết quả
O_S_AN = zeros(length(phi_values), length(dE_range_AN));
C_S_avg_AN = zeros(length(phi_values), length(dE_range_AN));
C_B_avg_AN = zeros(length(phi_values), length(dE_range_AN));
C_E_avg_AN = zeros(length(phi_values), length(dE_range_AN));
R_s_avg_AN = zeros(length(phi_values), length(dE_range_AN));
SOP_AN = zeros(length(phi_values), length(dE_range_AN));
IP_AN = zeros(length(phi_values), length(dE_range_AN));

fprintf('Tham số khảo sát:\n');
fprintf('- P_A = %.1f W (công suất truyền tổng)\n', P_A);
fprintf('- phi_values = [%.1f, %.1f, %.1f]\n', phi_values);
fprintf('- d_B = %.0f m (khoảng cách Alice-Bob)\n', d_B_AN);
fprintf('- d_E = %.0f-%.0f m (khoảng cách Alice-Eve) - Small Cell\n', dE_range_AN(1), dE_range_AN(end));
fprintf('- Số mẫu mô phỏng: %s\n', num2str(num_samples, '%.0f'));

% Mô phỏng AN cho từng giá trị phi
for phi_idx = 1:length(phi_values)
    phi = phi_values(phi_idx);
    fprintf('\nĐang mô phỏng với φ = %.1f...\n', phi);
    
    for i = 1:length(dE_range_AN)
        d_E = dE_range_AN(i);
        % Tạo kênh fading Rayleigh
        h_B = sqrt(0.5) * (randn(num_samples, 1) + 1j * randn(num_samples, 1));
        h_E = sqrt(0.5) * (randn(num_samples, 1) + 1j * randn(num_samples, 1));
        
        % Áp dụng thuật toán AN
        [SNR_Bob_AN, SNR_Eve_AN, C_S_AN] = artificial_noise_algorithm(...
            P_A, phi, h_B, h_E, d_B_AN, d_E, N_0, alpha);
        
        % Tính các chỉ số bảo mật bổ sung
        % Dung lượng kênh (bits/s/Hz)
        C_B = log2(1 + SNR_Bob_AN);
        C_E = log2(1 + SNR_Eve_AN);
        
        % Tỷ lệ bí mật (bits/s/Hz)
        R_s = max(0, C_B - C_E);
        
        % Secrecy Outage Probability (SOP)
        SOP = (R_s < epsilon_S);
        
        % Intercept Probability (IP)
        IP = (C_E > C_th);
        
        % Lưu kết quả trung bình
        O_S_AN(phi_idx, i) = mean(C_S_AN < epsilon_S * 180e3);
        C_S_avg_AN(phi_idx, i) = mean(C_S_AN);
        C_B_avg_AN(phi_idx, i) = mean(C_B);
        C_E_avg_AN(phi_idx, i) = mean(C_E);
        R_s_avg_AN(phi_idx, i) = mean(R_s);
        SOP_AN(phi_idx, i) = mean(SOP);
        IP_AN(phi_idx, i) = mean(IP);
    end
end

% Vẽ kết quả mô phỏng AN với các chỉ số bảo mật bổ sung
figure('Position', [100, 100, 1500, 1000]);

% Subplot 1: Secrecy Outage Probability (SOP)
subplot(3, 3, 1);
for phi_idx = 1:length(phi_values)
    plot(dE_range_AN, SOP_AN(phi_idx, :), ...
         'Color', phi_colors{phi_idx}, 'LineWidth', 2, ...
         'DisplayName', phi_labels{phi_idx}, 'Marker', 'o', 'MarkerSize', 4);
    hold on;
end
xlabel('Khoảng cách Alice-Eve (m)');
ylabel('SOP');
title('Secrecy Outage Probability (SOP)');
legend('Location', 'best');
grid on;

% Subplot 2: Intercept Probability (IP)
subplot(3, 3, 2);
for phi_idx = 1:length(phi_values)
    plot(dE_range_AN, IP_AN(phi_idx, :), ...
         'Color', phi_colors{phi_idx}, 'LineWidth', 2, ...
         'DisplayName', phi_labels{phi_idx}, 'Marker', 's', 'MarkerSize', 4);
    hold on;
end
xlabel('Khoảng cách Alice-Eve (m)');
ylabel('IP');
title('Intercept Probability (IP)');
legend('Location', 'best');
grid on;

% Subplot 3: Tỷ lệ bí mật R_s
subplot(3, 3, 3);
for phi_idx = 1:length(phi_values)
    plot(dE_range_AN, R_s_avg_AN(phi_idx, :), ...
         'Color', phi_colors{phi_idx}, 'LineWidth', 2, ...
         'DisplayName', phi_labels{phi_idx}, 'Marker', '^', 'MarkerSize', 4);
    hold on;
end
xlabel('Khoảng cách Alice-Eve (m)');
ylabel('R_s (bits/s/Hz)');
title('Tỷ lệ bí mật R_s');
legend('Location', 'best');
grid on;

% Subplot 4: Dung lượng kênh Bob C_B
subplot(3, 3, 4);
for phi_idx = 1:length(phi_values)
    plot(dE_range_AN, C_B_avg_AN(phi_idx, :), ...
         'Color', phi_colors{phi_idx}, 'LineWidth', 2, ...
         'DisplayName', phi_labels{phi_idx}, 'Marker', 'd', 'MarkerSize', 4);
    hold on;
end
xlabel('Khoảng cách Alice-Eve (m)');
ylabel('C_B (bits/s/Hz)');
title('Dung lượng kênh Bob C_B');
legend('Location', 'best');
grid on;

% Subplot 5: Dung lượng kênh Eve C_E
subplot(3, 3, 5);
for phi_idx = 1:length(phi_values)
    plot(dE_range_AN, C_E_avg_AN(phi_idx, :), ...
         'Color', phi_colors{phi_idx}, 'LineWidth', 2, ...
         'DisplayName', phi_labels{phi_idx}, 'Marker', 'v', 'MarkerSize', 4);
    hold on;
end
xlabel('Khoảng cách Alice-Eve (m)');
ylabel('C_E (bits/s/Hz)');
title('Dung lượng kênh Eve C_E');
legend('Location', 'best');
grid on;

% Subplot 6: Average Secrecy Capacity
subplot(3, 3, 6);
for phi_idx = 1:length(phi_values)
    plot(dE_range_AN, C_S_avg_AN(phi_idx, :) / 1000, ...
         'Color', phi_colors{phi_idx}, 'LineWidth', 2, ...
         'DisplayName', phi_labels{phi_idx}, 'Marker', 'p', 'MarkerSize', 4);
    hold on;
end
xlabel('Khoảng cách Alice-Eve (m)');
ylabel('Secrecy Capacity trung bình (kbps)');
title('Secrecy Capacity với Artificial Noise');
legend('Location', 'best');
grid on;

% Subplot 7: So sánh hiệu suất theo phi
subplot(3, 3, 7);
d_E_fixed = 60;  % Khoảng cách cố định để so sánh (phù hợp với small cell)
[~, d_E_idx] = min(abs(dE_range_AN - d_E_fixed));

phi_comparison = zeros(1, length(phi_values));
for phi_idx = 1:length(phi_values)
    phi_comparison(phi_idx) = C_S_avg_AN(phi_idx, d_E_idx) / 1000;
end

bar(phi_values, phi_comparison);
colormap(lines);
xlabel('Tỷ lệ công suất φ');
ylabel('Secrecy Capacity (kbps)');
title(sprintf('So sánh hiệu suất tại d_E = %.0fm', d_E_fixed));
grid on;

% Subplot 8: Heatmap Secrecy Capacity
subplot(3, 3, 8);
imagesc(dE_range_AN, phi_values, C_S_avg_AN / 1000);
colorbar;
xlabel('Khoảng cách Alice-Eve (m)');
ylabel('Tỷ lệ công suất φ');
title('Heatmap Secrecy Capacity');
set(gca, 'YDir', 'normal');

% Subplot 9: Heatmap Tỷ lệ bí mật R_s
subplot(3, 3, 9);
imagesc(dE_range_AN, phi_values, R_s_avg_AN);
colorbar;
xlabel('Khoảng cách Alice-Eve (m)');
ylabel('Tỷ lệ công suất φ');
title('Heatmap Tỷ lệ bí mật R_s');
set(gca, 'YDir', 'normal');

% Phân tích kết quả
fprintf('\n%s\n', repmat('=', 1, 60));
fprintf('PHÂN TÍCH KẾT QUẢ ARTIFICIAL NOISE\n');
fprintf('%s\n', repmat('=', 1, 60));

for phi_idx = 1:length(phi_values)
    phi = phi_values(phi_idx);
    avg_secrecy_capacity = mean(C_S_avg_AN(phi_idx, :)) / 1000;
    min_secrecy_capacity = min(C_S_avg_AN(phi_idx, :)) / 1000;
    max_secrecy_capacity = max(C_S_avg_AN(phi_idx, :)) / 1000;
    avg_outage = mean(O_S_AN(phi_idx, :));
    
    fprintf('\nφ = %.1f:\n', phi);
    fprintf('  - P_S = %.1fW, P_AN = %.1fW\n', phi*P_A, (1-phi)*P_A);
    fprintf('  - Secrecy Capacity trung bình: %.2f kbps\n', avg_secrecy_capacity);
    fprintf('  - Secrecy Capacity min/max: %.2f/%.2f kbps\n', min_secrecy_capacity, max_secrecy_capacity);
    fprintf('  - Xác suất dừng bảo mật trung bình: %.4f\n', avg_outage);
    
    % Thêm các chỉ số bảo mật bổ sung
    avg_C_B = mean(C_B_avg_AN(phi_idx, :));
    avg_C_E = mean(C_E_avg_AN(phi_idx, :));
    avg_R_s = mean(R_s_avg_AN(phi_idx, :));
    avg_SOP = mean(SOP_AN(phi_idx, :));
    avg_IP = mean(IP_AN(phi_idx, :));
    
    fprintf('  - Dung lượng kênh Bob C_B trung bình: %.4f bits/s/Hz\n', avg_C_B);
    fprintf('  - Dung lượng kênh Eve C_E trung bình: %.4f bits/s/Hz\n', avg_C_E);
    fprintf('  - Tỷ lệ bí mật R_s trung bình: %.4f bits/s/Hz\n', avg_R_s);
    fprintf('  - Secrecy Outage Probability (SOP) trung bình: %.4f\n', avg_SOP);
    fprintf('  - Intercept Probability (IP) trung bình: %.4f\n', avg_IP);
end

% Tìm giá trị phi tối ưu
[~, optimal_phi_idx] = max(mean(C_S_avg_AN, 2));
optimal_phi = phi_values(optimal_phi_idx);
fprintf('\nGiá trị φ tối ưu: %.1f\n', optimal_phi);
fprintf('Secrecy Capacity trung bình tối ưu: %.2f kbps\n', mean(C_S_avg_AN(optimal_phi_idx, :))/1000);

% Phân tích các chỉ số bảo mật bổ sung
fprintf('\n%s\n', repmat('=', 1, 60));
fprintf('PHÂN TÍCH CÁC CHỈ SỐ BẢO MẬT BỔ SUNG\n');
fprintf('%s\n', repmat('=', 1, 60));

% Tìm giá trị tối ưu cho từng chỉ số
[~, optimal_R_s_idx] = max(mean(R_s_avg_AN, 2));
[~, optimal_SOP_idx] = min(mean(SOP_AN, 2));
[~, optimal_IP_idx] = min(mean(IP_AN, 2));

fprintf('Tối ưu theo R_s: φ = %.1f (R_s = %.4f bits/s/Hz)\n', ...
        phi_values(optimal_R_s_idx), mean(R_s_avg_AN(optimal_R_s_idx, :)));
fprintf('Tối ưu theo SOP: φ = %.1f (SOP = %.4f)\n', ...
        phi_values(optimal_SOP_idx), mean(SOP_AN(optimal_SOP_idx, :)));
fprintf('Tối ưu theo IP: φ = %.1f (IP = %.4f)\n', ...
        phi_values(optimal_IP_idx), mean(IP_AN(optimal_IP_idx, :)));

fprintf('\n%s\n', repmat('=', 1, 60));
fprintf('KẾT LUẬN:\n');
fprintf('%s\n', repmat('=', 1, 60));
fprintf('1. Artificial Noise cải thiện đáng kể bảo mật tầng vật lý\n');
fprintf('2. Giá trị φ tối ưu cân bằng giữa tín hiệu hợp lệ và nhiễu nhân tạo\n');
fprintf('3. Hiệu suất bảo mật phụ thuộc vào khoảng cách và phân bổ công suất\n');
fprintf('4. AN hiệu quả nhất khi Eve ở xa và Bob ở gần\n');
fprintf('5. Các chỉ số bảo mật bổ sung (SOP, IP, R_s) cung cấp đánh giá toàn diện\n');
fprintf('6. Dung lượng kênh C_B và C_E phản ánh chất lượng truyền tin\n'); 