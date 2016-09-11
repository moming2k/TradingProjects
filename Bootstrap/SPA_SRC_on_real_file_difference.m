clear; 
clc;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  This gives the parameters in the simulations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

r=500;                      %number of simulation repititions%
B=1000;                     %number of bootstrap repetitions%
max_com=10;                 % the maximum number of comparisions we make in the algorithm 
SPA_k=3;                    % the k-Step-SPA or K-Step-RC

y = csvread('20160703_1m_updated.csv', 1, 1);
[n, m] = size(y);           % m is number of models n is sample size

%%%%%%%%%%%%%%%%%%%%%%%%%
%%% here generates the means of the models
test_statistic=mean(y)';  %test statistic
y = y';

reject_matrix_SPA_1=zeros(m, r);
reject_matrix_SPA_k=zeros(m, r);

p_value_SPA_1 = ones(1, r) * 5;
p_value_SPA_k = zeros(1, r);

%%% this is the loop for simulations repetitions.

for q=1:r;
    
    boot_statistic_SPA=zeros(m,B); %bootstrap statistics for RC type test

    %%% for b=1:B;
    %%% this is the loop for bootstrap repetitions.
    for b=1:B;
        ran_idx=floor(rand(n,1)*n)+1;    % matrix of random indices

        y_boot=y(:,ran_idx);
        boot_statistic_SPA(:,b)=(mean(y_boot, 2)-test_statistic);     
    end;
       
    model_index=(1:m)'; %this generates a vector from 1 to m

    test_index=[test_statistic model_index]; % This label the models

    %%% This sort the models by the desending order of the test statistics
    %%% The new column gives the rank of each model
    test_index=[sortrows(test_index, -1) model_index];

    %%%Sort the matrix according to the original labels
    %%% therefore, the last column gives the ranks of original models among
    %%% based on the test statistics 
    test_index=sortrows(test_index, 2);  

    %%% THe following ranks the bootstrap statistics according to the ranks\
    ranked_boot_statistic_SPA=boot_statistic_SPA(test_index(:,3),:);

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %SPA-k procedure starts here
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

    %%% reject denotes the number of the rejected model in the currect step
    %%% before the procedure,  let it be zeros
    num_reject=0; 

    %reject1 denotes the numbers of the rejected model in the previous step
    % before the procedure, we let it be -m
    num_reject1=-m; 

    while num_reject > num_reject1; % the procedure will stop when there is no further rejections
        num_reject1=num_reject; %the num_reject will become num_reject` after this step

        %%% The CV depends on the number of rejections so far
        %%% We separate is by whether we need to consider add rejected models
        %%% back to the procedure or not

        if num_reject<SPA_k; %if num_reject<SPA_k, we don't need to consdier combinations
            sim_CV=sort(ranked_boot_statistic_SPA,'descend');
            k_sim_max=sim_CV(SPA_k,:);
            sort_k_sim_max=sort(k_sim_max','descend');
            CV= max(sort_k_sim_max(floor(0.05*B)+1),0);

        else  % otherwise, we do.
            com=combnk(1: num_reject, SPA_k-1); % give all the possible combinations
            [q1, q2]=size(com);                  % q1=C(num_reject,SPA_k-1 ) the number of all possible combinations  

            com=[com sum(com, 2)];               %
            com=sortrows(com, -3);            %rank the combinations in the desending order based on the sum
            com=com(:,1:(SPA_k-1));             

            max_com_loop=min([q1, max_com]);     % we pick up at most max_com combinations

            CV1=zeros(1,max_com_loop+1);

            %%%
            %%%This is the loop to consider the added rejected models 
            %%%Again, we consider at most max_com models

            for j=1:max_com_loop;
               sim_CV=sort(ranked_boot_statistic_SPA([com(j,:) num_reject:m],: ),'descend');
               k_sim_max=sim_CV(SPA_k,:);
               sort_k_sim_max=sort(k_sim_max','descend');
               CV1(j)= sort_k_sim_max(floor(0.05*B)+1);
            end
            %end for the for loop

        CV=max(CV1);

        end
        %end for the if loop

        reject=(test_statistic > CV) ;  %this gives the models that are rejected after this step 
        num_reject=sum(reject);          %the number of the all rejected models after this step
    end
    %end for the while loop

    %%%at the end of the procedure, save all the rejected models in the matrix reject_matrix_SPA_k 
    reject_matrix_SPA_k(:,q)=reject;   
    sim_CV=sort(ranked_boot_statistic_SPA,'descend');
    p_value_SPA_k(1, q) = sum(sim_CV(SPA_k,:) > CV) / B * 100;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %the SPA procedure starts here
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

    %note that Step-SPA does not need to added those rejected models back
    sim_CV=sort(ranked_boot_statistic_SPA,'descend');
    k_sim_max=sim_CV(1,:);
    sort_k_sim_max=sort(k_sim_max','descend');
    CV= max(sort_k_sim_max(floor(0.05*B)+1), 0);

    reject=(test_statistic > CV ) ;   

    reject_matrix_SPA_1(:,q)=reject;

    disp(q);

end

%%% false_reject_SPA_k gives the number of false rejections for k-Step-SPA
%%% procedure.  We just need to add up those ones from models m_plus+1 to m

false_reject_SPA_k=sum(reject_matrix_SPA_k(1:m,:));

%%% kFWER_SPA_k gives the k-FWER of k-Step-SPA procedure.  when the number
%%% of false rejections is greater than or equal to SPA_k, we will count
%%% one.  This is equivalent to strictly greater than SPA_k-1

kFWER_SPA_k=mean( (false_reject_SPA_k>SPA_k-1) );

%%% FWER_SPA_k gives the FWER of Step-SPA procedure.  when the number
%%% of false rejections is greater than or equal to 1, we will count
%%% one.  This is equivalent to strictly greater than 0
FWER_SPA_k=mean( (false_reject_SPA_k>0));

%%%those are defined similarly for other methods
false_reject_SPA_1=sum(reject_matrix_SPA_1(1:m,:));
kFWER_SPA_1=mean( (false_reject_SPA_1>SPA_k-1) );
FWER_SPA_1=mean( (false_reject_SPA_1>0));

[FWER_SPA_1;
 kFWER_SPA_k]

false_reject_SPA_1 = false_reject_SPA_1';
false_reject_SPA_k = false_reject_SPA_k';
p_value_SPA_1 = p_value_SPA_1';
p_value_SPA_k = p_value_SPA_k';
