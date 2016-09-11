method_name = 'SPA';
month_list = {'12m', '6m', '3m', '1m'};

for i = 1:4;
    subplot(4,3,i * 3 - 2);
    h = histogram(difference(:, i));
    shape = size(h.Values);
    if shape(2) == 1
        h.BinLimits = [h.BinLimits(1) - 4, h.BinLimits(1) + 4];
    end
    title(strcat(method_name, ' Reject Models (', month_list(i), ')'));
    
    subplot(4,3,i * 3 - 1);
    h = histogram(differenceS1(:, i));
    shape = size(h.Values);
    if shape(2) == 1
        h.BinLimits = [h.BinLimits(1) - 4, h.BinLimits(1) + 4];
    end
    title(strcat(method_name, ' k Reject Models (', month_list(i), ')'));
    
    subplot(4,3,i * 3);
    h = histogram(differenceS2(:, i));
    shape = size(h.Values);
    if shape(2) == 1
        h.BinLimits = [h.BinLimits(1) - 4, h.BinLimits(1) + 4];
    end
    title(strcat(method_name, ' k P values (', month_list(i), ')'));
end


ha = axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0 1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');

text(0.5, 1,'\bf SPA & SPA k (Mean Difference)','HorizontalAlignment','center','VerticalAlignment', 'top')