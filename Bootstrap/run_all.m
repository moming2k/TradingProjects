clc;
clear;
format long

p = 8;
q = 8;
file_names = {'20160703_12m_updated.csv', '20160703_6m_updated.csv', '20160703_3m_updated.csv', '20160703_1m_updated.csv'};
results = [];
for i = 3:4
    disp(file_names{i})
    results = [zeros(2, 8); results];
    [ y, y_mean, y_std, max_mean_index, max_sharpe_index ] = load_file(p, q, file_names{i});
    disp([max_mean_index, max_sharpe_index])
    max_mean = y(:, max_mean_index);
    max_mean = max_mean + 1;
    max_mean = prod(max_mean);

    max_sharpe = y(:, max_sharpe_index);
    max_sharpe = max_sharpe + 1;
    max_sharpe = prod(max_sharpe);
    disp([max_mean; max_sharpe]);

    [~, reject_rate] = step_SPA_real(y, y_mean, y_std, max_mean_index, max_sharpe_index);
    results(1:2, 7) = reject_rate;
    [~, reject_rate] = step_SPA_real_diff(y, y_mean, y_std, max_mean_index, max_sharpe_index);
    results(1:2, 8) = reject_rate;
    [ ~, reject_rate_src, reject_rate_src_k, reject_rate_spa, reject_rate_spa_k ] = SPA_SRC_on_real_file(y, y_mean, y_std, max_mean_index, max_sharpe_index);
    results(1:2, 1) = reject_rate_src;
    results(1:2, 2) = reject_rate_src_k;
    results(1:2, 3) = reject_rate_spa;
    results(1:2, 4) = reject_rate_spa_k;
    
    [ ~, reject_rate_spa, reject_rate_spa_k ] = SPA_SRC_on_real_file_difference(y, y_mean, y_std, max_mean_index, max_sharpe_index);
    results(1:2, 5) = reject_rate_spa;
    results(1:2, 6) = reject_rate_spa_k;
    [sd,Fs] = audioread('Vivaldi - Spring.mp3');
    soundsc(sd, 2*Fs)
end

% for i = 1:4
%     y = load_file(1, 4);
% end
% max_mean = y(:, max_mean_index);
% max_mean = max_mean + 1;
% max_mean = prod(max_mean);
% 
% max_sharpe = y(:, max_sharpe_index);
% max_sharpe = max_sharpe + 1;
% max_sharpe = prod(max_sharpe);
% disp([max_mean; max_sharpe]);