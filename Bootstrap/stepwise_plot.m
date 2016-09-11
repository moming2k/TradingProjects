
subplot(4,2,1);
histogram(nRejects12m);
title('Reject models (12m)');

subplot(4,2,2);
histogram(Step12m);
title('Steps (12m)');

subplot(4,2,3);
histogram(nRejects6m);
title('Reject models (6m)');

subplot(4,2,4);
histogram(Step6m);
title('Steps (6m)');

subplot(4,2,5);
histogram(nRejects3m);
title('Reject models (3m)');

subplot(4,2,6);
histogram(Step3m);
title('Steps (3m)');

subplot(4,2,7);
h = histogram(nRejects1m);
shape = size(h.Values);
if shape(2) == 1
    h.BinLimits = [h.BinLimits(1) - 4, h.BinLimits(1) + 4];
end
title('Reject models (1m)');

subplot(4,2,8);
histogram(Step1m);
title('Steps (1m)');

ha = axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0 
1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');

text(0.5, 1,'\bf Stepwise SPA (Mean Difference)','HorizontalAlignment','center','VerticalAlignment', 'top')