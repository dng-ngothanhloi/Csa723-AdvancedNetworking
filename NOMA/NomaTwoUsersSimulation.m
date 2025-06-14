% Simulate NOMA with SIC for two users with different power allocations
% Compare NOMA and OFDMA performance for near (UE1) and far (UE2) users

% Helper functions
function linear = db_to_linear(db_value)
    linear = 10^(db_value / 10);
end

function db = linear_to_db(linear_value)
    if linear_value <= 0
        db = -inf;
    else
        db = 10 * log10(linear_value);
    end
end

% Parameters
n_realizations = 100000;  % Number of Monte Carlo realizations
P_total = 1;  % Total transmit power (W)
N0_base = 1e-9;  % Base noise power (W)
N0_db = linear_to_db(N0_base);  % Noise power in dB

% User distances and path loss
d1 = 50;  % Distance of UE1 (near user) in meters
d2 = 150; % Distance of UE2 (far user) in meters
theta = 3.0;  % Path loss exponent

% Power allocation
alpha = 0.7;  % Power allocation factor for UE1
P1 = alpha * P_total; % Power allocated to UE1
P2 = (1 - alpha) * P_total; % Power allocated to UE2

% SINR thresholds
Gamma1_db = 5;  % SINR threshold for UE1 (dB)
Gamma2_db = 10; % SINR threshold for UE2 (dB)
Gamma1_linear = db_to_linear(Gamma1_db);
Gamma2_linear = db_to_linear(Gamma2_db);

% SNR range for analysis
snr_db_range = 0:5:30;  % SNR range from 0 to 30 dB in steps of 5 dB
throughput_stats = zeros(length(snr_db_range), 7);  % Preallocate array for statistics

% Analyze performance for different SNR values
for i = 1:length(snr_db_range)
    snr_db = snr_db_range(i);
    % Calculate noise power for current SNR
    snr_linear = db_to_linear(snr_db);
    N0_sim = P_total / snr_linear;
    
    % Generate channel gains with path loss
    % Note: Using the same path loss model as Python
    h1_sq = (d1^(-theta)) * exprnd(1.0, [1, n_realizations]);
    h2_sq = (d2^(-theta)) * exprnd(1.0, [1, n_realizations]);
    
    % Calculate SINRs
    sinr_ue1 = (P1 * h1_sq) ./ (P2 * h1_sq + N0_sim);
    sinr_ue2_to1 = (P1 * h2_sq) ./ (P2 * h2_sq + N0_sim);
    sinr_ue2_to2 = (P2 * h2_sq) ./ N0_sim;
    
    % Calculate throughputs (using the same formula as Python)
    throughput_ue1 = log2(1 + sinr_ue1);
    throughput_ue2 = log2(1 + sinr_ue2_to2);
    throughput_oma = 0.5 * (log2(1 + (P_total * h1_sq ./ N0_sim)) + ...
                           log2(1 + (P_total * h2_sq ./ N0_sim)));
    
    % Calculate statistics
    avg_throughput_ue1 = mean(throughput_ue1);
    avg_throughput_ue2 = mean(throughput_ue2);
    avg_throughput_noma = avg_throughput_ue1 + avg_throughput_ue2;
    avg_throughput_oma = mean(throughput_oma);
    
    % Calculate outage probabilities
    outage_ue1 = sum(sinr_ue1 < Gamma1_linear) / n_realizations;
    outage_ue2 = (sum(sinr_ue2_to1 < Gamma1_linear) + ...
                 sum((sinr_ue2_to1 >= Gamma1_linear) & (sinr_ue2_to2 < Gamma2_linear))) / n_realizations;
    
    % Store statistics
    throughput_stats(i,:) = [snr_db, avg_throughput_ue1, avg_throughput_ue2, ...
                            avg_throughput_noma, avg_throughput_oma, ...
                            outage_ue1, outage_ue2];
end

% Create table for better display
stats_table = array2table(throughput_stats, ...
    'VariableNames', {'SNR_dB', 'NOMA_UE1', 'NOMA_UE2', 'NOMA_Total', ...
                     'OFDMA', 'Outage_UE1', 'Outage_UE2'});

% Display detailed statistics
fprintf('\n==================================================\n');
fprintf('===== Detailed Throughput Statistics =====\n');
fprintf('==================================================\n\n');
fprintf('Throughput Statistics by SNR:\n');
disp(stats_table);

% Calculate summary statistics
[max_noma, max_noma_idx] = max(stats_table.NOMA_Total);
[max_ofdma, max_ofdma_idx] = max(stats_table.OFDMA);
avg_gain = mean(stats_table.NOMA_Total ./ stats_table.OFDMA - 1) * 100;

fprintf('\nSummary Statistics:\n');
fprintf('Maximum NOMA Throughput: %.4f bits/s/Hz at %.1f dB\n', ...
    max_noma, stats_table.SNR_dB(max_noma_idx));
fprintf('Maximum OFDMA Throughput: %.4f bits/s/Hz at %.1f dB\n', ...
    max_ofdma, stats_table.SNR_dB(max_ofdma_idx));
fprintf('Average Throughput Gain: %.2f%%\n', avg_gain);

% Plot results
figure('Position', [100, 100, 1200, 800]);

% Plot 1: Throughput vs SNR
subplot(2, 2, 1);
plot(stats_table.SNR_dB, stats_table.NOMA_UE1, 'b-', 'LineWidth', 2);
hold on;
plot(stats_table.SNR_dB, stats_table.NOMA_UE2, 'r-', 'LineWidth', 2);
plot(stats_table.SNR_dB, stats_table.NOMA_Total, 'g-', 'LineWidth', 2);
plot(stats_table.SNR_dB, stats_table.OFDMA, 'k--', 'LineWidth', 2);
xlabel('SNR (dB)');
ylabel('Throughput (bits/s/Hz)');
title('Throughput vs SNR');
legend('NOMA UE1 (Near)', 'NOMA UE2 (Far)', 'NOMA Total', 'OFDMA');
grid on;

% Plot 2: Outage Probability vs SNR
subplot(2, 2, 2);
semilogy(stats_table.SNR_dB, stats_table.Outage_UE1, 'b-', 'LineWidth', 2);
hold on;
semilogy(stats_table.SNR_dB, stats_table.Outage_UE2, 'r-', 'LineWidth', 2);
xlabel('SNR (dB)');
ylabel('Outage Probability');
title('Outage Probability vs SNR');
legend('UE1 (Near)', 'UE2 (Far)');
grid on;

% Plot 3: Throughput Gain vs SNR
subplot(2, 2, 3);
throughput_gain = (stats_table.NOMA_Total ./ stats_table.OFDMA - 1) * 100;
plot(stats_table.SNR_dB, throughput_gain, 'g-', 'LineWidth', 2);
xlabel('SNR (dB)');
ylabel('Throughput Gain (%)');
title('NOMA vs OFDMA Throughput Gain');
grid on;

% Plot 4: Throughput Distribution at Maximum SNR
subplot(2, 2, 4);
max_snr_idx = length(stats_table.SNR_dB);
throughput_data = [stats_table.NOMA_UE1(max_snr_idx), ...
                  stats_table.NOMA_UE2(max_snr_idx), ...
                  stats_table.OFDMA(max_snr_idx)];
bar(throughput_data);
set(gca, 'XTickLabel', {'NOMA UE1', 'NOMA UE2', 'OFDMA'});
ylabel('Throughput (bits/s/Hz)');
title(sprintf('Throughput Distribution at %.1f dB', stats_table.SNR_dB(max_snr_idx)));
grid on;

% Adjust figure properties
set(gcf, 'Color', 'white');
set(findall(gcf,'-property','FontSize'), 'FontSize', 12);

% Save statistics to CSV
writetable(stats_table, 'noma_throughput_statistics.csv');
fprintf('\nStatistics have been saved to ''noma_throughput_statistics.csv''\n'); 