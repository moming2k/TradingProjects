function [ y ] = load_file(p, q)
%LOAD_FILE Summary of this function goes here
%   Detailed explanation goes here

    if nargin < 2
        p = 2;
        q = 8;
    end
    file_name = '20160703_3m_updated.csv';

    y=csvread(file_name, 1, 1);   % load the data matrix y

    [n, ~]=size(y);          % n is the sample size of data matrix y
                             % m is the number of models of data matrix y
    start_index = int16((p - 1) / q * n + 1);
    end_index = int16(p / q * n);
    disp(start_index)
    disp(end_index)
    y = y(start_index : end_index, :);
end

