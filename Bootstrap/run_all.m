clc
% step_SPA_real
% step_SPA_real_diff
% SPA_SRC_on_real_file
% SPA_SRC_on_real_file_difference
% [sd,Fs] = audioread('Vivaldi - Spring.mp3');
% soundsc(sd, 2*Fs)
for i = 6:7
    y = load_file(i, 8);
end