% clc;
clear;
%PARAMETERS%
y = load_file();
[n, m]=size(y); 
                         
r=500;                   % number of simulation repititions%
B=1000;                  % number of bootstrapping
s_level=0.05;            % significant level
Q=0.9;                   % the porobability of picking the following sample

step_record = zeros(1, r);
reject_num_record = zeros(1, r);
reject_record = zeros(m, r);
   
%==========================================================================
%   calculate the maximum of the sample means
%==========================================================================
y_mean=mean(y);                   % calculate the sample mean.  This will give you row(1*m) vector.
max_y_mean=max(y_mean);           % the maximum of the sample means
                                  % or the non-standardized SPA statistis

%================================================================
% Calculate the covariance martix defined in Step-SPA test paper 
%================================================================
y_demean=y-ones(n,1)*y_mean;     % generate the de-meaned data

%==================================================
% Calculate the standardized SPA statistic
%==================================================
sspa_statistics=y_mean;         % the vector of the standardized statistics of all models.

yy=[y_demean'  y_demean']'; 
% a 2n x m matrix of de-meaned y; we stack one on another 

%==========================================================================
%   SPA procedure starts from here
%==========================================================================

for q=1:r;                      

    %==================================================
    % bootstrap procedure starts from here
    %==================================================              
    boot_means=zeros(B,m);  
    boot_sspa_statistic=zeros(B,1);           % the matrix for the bootstrapped statistics
              
    for b=1:B;
        ran_idx=floor(rand(n,1)*n)+1;    %the random index matrix

        pr=rand(n-1,1);                  %the probability matrix that will decide if we should 
                                         %get the next observation or do a random draw
        for j=2:n;                              
            if pr(j-1,1) < Q;                
                ran_idx(j,1)=ran_idx(j-1,1)+1;  
                % if the value is less than Q, we take the next one for next period;                                
                % that is, we re-define ran_idx(j,1)=ran_idx(j-1,1)+1. Then the 
                % probability of picking the next index will be Q
                % or we randomly pick one for next period.
                % That is we do not change ran_idx(j,1).
            end
        end
        x=yy(ran_idx,:);                         % X is the bth bootstrap (de-meaned) sample  
        boot_means(b,:)=mean(x);
    end
         
    %==================================================
    %Step-SPA procedure starts from here
    %==================================================

    k=1;                       %start with step 1

    reject_1=ones(1,m);        % if reject_1(1,j)=1, then model j is not rejected yet.  
                               % if reject_1(1,j)=0, then model j is rejected.
                               % the procedure start with every model is not rejected
                               % Hence, reject_1=ones(1,m). 

    reject_2=ones(1,m);        % denote the rejected models after kth step

    step=0;                    % number of the steps in this test

    while k<=m;          %the maximum steps of this procedure is m

        for b=1:B;
            boot_sspa_statistic(b,1)=max(boot_means(b,:).*reject_1);
            % boot_means(b,:).*a1 
            % for example, if model j is rejected before this step. then reject_1(j,1)=0.  Hence, the
            % bootstraped statistics for model j will be 0.
            % if model j is not rejected before this step. then reject_1(j,1)=1.  Hence, the
            % bootstraped statistics for model j will be the bootstrapped mean (centered and standardized) of model j.
        end
        boot_sspa_statistic=sort(boot_sspa_statistic,1); 
        sspa_critical= boot_sspa_statistic(floor((1 - s_level)*B),1); 
        %sspa_critical will be the critical value at this step

        for jj=1:m;
            if sspa_statistics(1,jj)>sspa_critical;
                reject_2(1,jj)=0;
                % if model jj is rejected at this step or at previous steps, then we
                % set reject_2(1,jj)=0;  otherwise, reject_2(1,jj)=1.
            end
        end
        step=step+1;   %the step count
        if reject_2==reject_1; 
            k=m+1;
            % if reject_2==reject_1, that means, there is no model rejected at
            % this stage, so the procedure has to stop.  Hence, we
            % set k=m+1;
        else
            k=k+1;
            reject_1=reject_2;
            % otherwise, we go to next step and set k=k+1;
            % and set reject_1=reject_2 for the next stage.

        end 

    end
    reject_num_record(1, q) = m - sum(reject_2);
    step_record(1, q) = step;
    reject_record(:, q) = reject_2;
    % will report the models we reject
    % if no model is rejected, will report  "Empty matrix: 0-by-1"
        
end

step_record = step_record';
reject_num_record = reject_num_record';
result = [
    mean(reject_num_record); min(reject_num_record); max(reject_num_record);
    mean(step_record); min(step_record); max(step_record);
    ];

% [sd,Fs] = audioread('Vivaldi - Spring.mp3');
% soundsc(sd, 2*Fs)
disp('Stepwise SPA difference')
disp(result)