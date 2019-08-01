close all
clear all

folder_results = '.\results\';

tableAcc_filename = [folder_results 'accuracy_table.csv'];
tablesAcc = readtable(tableAcc_filename);

tableAccOnline_filename = [folder_results 'online_accuracy_table.csv'];
tableAccOnline = readtable(tableAccOnline_filename);

acc_matrix = [];
xlabels = {'CSP','TRCSP @ 1e^-3', 'TRCSP @ 1e^-2', 'TRCSP @ 1e^-1', 'TRCSP @ 1'};
acc_matrix = table2array(tablesAcc(:,2:2+size(xlabels,2) - 1));

disp([repmat('_',1,80) newline])
%% Show data collected
h1 = figure;
title_str = 'Figure 1: Accuracy per training mode';

imagesc(acc_matrix)
xticklabels(xlabels)
xtickangle(80)
title(title_str)
ylabel('Sessions')
colorbar

set(h1,'PaperPositionMode','auto');
set(h1,'PaperOrientation','landscape');
set(h1,'Position',[50 50 1200 800]);
print(gcf, '-dpdf', [folder_results 'Accuracy per training mode.pdf']);

disp(title_str)
disp(['Just a visualization of the matrix of simulations' newline newline ...
    'CSP is the classical way of calculating the CSP spatial filter' newline ...
    'TRCSP stands for  Tikhonov Regularizazed CSP, the algorithm implemented in the RCSP box on openvibe'])

disp([repmat('_',1,80) newline])

%% Show diff against calssical CSP
h2 = figure;
acc_matrix_mean_rcsp = mean(acc_matrix(:,2:end), 2);

tmp = [acc_matrix(:,1) acc_matrix_mean_rcsp];
diff_matrix = tmp - acc_matrix(:,1);

imagesc(diff_matrix)
xticks([1 2])
xticklabels({'CSP', 'TRCSP'})
xtickangle(80)
title_str = 'Figure 2: Accuracy diff against training with classical CSP';
title(title_str)
ylabel('Sessions')
colorbar

set(h2,'PaperPositionMode','auto');
set(h2,'PaperOrientation','landscape');
set(h2,'Position',[50 50 1200 800]);
print(gcf, '-dpdf', [folder_results 'Accuracy diff against training with classical CSP.pdf']);

mean_diff = mean(tmp - acc_matrix(:,1));
disp(title_str)
disp(['mean diff = ' num2str(mean_diff(2)) '%'])

% I'm using the mean of all rcsp tests, since they seem to be about the same

disp([repmat('_',1,80) newline])

%% Show histogram of accuracies
h3 = figure;
title_str = 'Histograms of accuracy';

mean_acc_with_csp   = mean(acc_matrix(:,1));
median_acc_with_csp = median(acc_matrix(:,1));
std_acc_with_csp    = std(acc_matrix(:,1));

mean_acc_with_trcsp   = mean(acc_matrix_mean_rcsp(:,1));
median_acc_with_trcsp = median(acc_matrix_mean_rcsp(:,1));
std_acc_with_trcsp    = std(acc_matrix_mean_rcsp(:,1));

subplot(2,1,1)
hist(acc_matrix(:,1))
title('Calculated using classical CSP')
subplot(2,1,2)

hist(acc_matrix_mean_rcsp)
title('Calculated using TRCSP')

[~,h3_suplabel] = suplabel(title_str,'t');
set(h3_suplabel,'FontSize',30)

set(h3,'PaperPositionMode','auto');
set(h3,'PaperOrientation','landscape');
set(h3,'Position',[50 50 1200 800]);
print(gcf, '-dpdf', [folder_results 'Histograms of accuracy.pdf']);

disp(title_str)
disp('The following summarize the histograms of the plots:')
disp(newline)
disp('Calculated using Classical CSP:')
disp(['  mean   = ' num2str(mean_acc_with_csp) '%'])
disp(['  median = ' num2str(median_acc_with_csp) '%'])
disp(['  std    = ' num2str(std_acc_with_csp)])
disp(newline)
disp('Calculated using TRCSP (average of columns):')
disp(['  mean   = ' num2str(mean_acc_with_trcsp) '%'])
disp(['  median = ' num2str(median_acc_with_trcsp) '%'])
disp(['  std    = ' num2str(std_acc_with_trcsp)])