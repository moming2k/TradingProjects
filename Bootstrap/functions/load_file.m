function [ y, y_mean, y_std, max_mean_index, max_sharpe_index ] = load_file(p, q, file_name)
%LOAD_FILE Summary of this function goes here
%   Detailed explanation goes here

    if nargin < 2
        p = 1;
        q = 4;
    end
    
    if nargin < 3
        file_name = '20160703_1m_updated.csv';
    end

    y=csvread(file_name, 1, 1);   % load the data matrix y

    [n, ~]=size(y);          % n is the sample size of data matrix y
                             % m is the number of models of data matrix y
    start_index = int16((p - 1) / q * n + 1);
    end_index = int16(p / q * n);
    disp([start_index end_index])
    y = y(start_index : end_index, :);
    y_mean = mean(y);
    y_std = var(y) .^ 0.5;
    y_sharpe = y_mean ./ y_std;
    max_mean_index = find(y_mean == max(y_mean));
    max_sharpe_index = find(y_sharpe == max(y_sharpe));
    max_sharpe_index = max_sharpe_index(1);
    max_mean_index = max_mean_index(1);
    disp([y_mean(max_mean_index); y_mean(max_sharpe_index)])
    disp([y_sharpe(max_mean_index); y_sharpe(max_sharpe_index)])
end

