clear all;
clc;
title_str = cell(3);
title_str{1} = '¾àÀëÏµÍ³Îó²î¾ø¶ÔÎó²î';
title_str{2} = '·½Î»½ÇÏµÍ³Îó²î¾ø¶ÔÎó²î';
title_str{3} = '¸©Ñö½ÇÏµÍ³Îó²î¾ø¶ÔÎó²î';
test_num = 10;
close all;
estimation_errors = zeros(2,3,test_num);
for tag=1:test_num
     radar_system = [20;0.03;0.02]+tag*[10;0.01;0.01];
     error = radar_estimator_test(radar_system);
     estimation_errors(1,1:3,tag) = error(:,1);
     estimation_errors(2,1:3,tag) = error(:,2);
end

x=1:test_num;

for radar_index=1:2
    figure(radar_index)
    for plot_index=1:3
        subplot(1,3,plot_index)
        tmp = reshape(estimation_errors(radar_index,plot_index,:),1,test_num);
        plot(x,tmp,'LineWidth',2)
        grid on
        title(title_str{plot_index})
    end
end