% Radar Estimator - Batch Estimator
% Author:qingyuanxingsi
% 2015-07-22

% time step
T = 1;

% duration
duration = 60;

% Radar Parameter Configuration
% System Deviation and noise
radar_deviation = [20   8;
                   0.03 0.04; 
                   0.02 0.02;
                   0.01 0.01;
                   0.01 0.01;
                   0.01 0.01];

% Radar position
radar_pos = [50  80;
             120 160;
             20  40];


% target initial states
target_init_state = [100 60 200;
                     100 80 100;
                     10  20  30;
                     10  15  5;
                     20  10  10;
                     10   5    10;
                     0   0    0;
                     0   0    0;
                     0   0    0];

% target transition matrix
F = [1 0 0 T 0 0 0 0 0;
     0 1 0 0 T 0 0 0 0;
     0 0 1 0 0 T 0 0 0;
     0 0 0 1 0 0 0 0 0;
     0 0 0 0 1 0 0 0 0;
     0 0 0 0 0 1 0 0 0;
     0 0 0 0 0 0 0 0 0;
     0 0 0 0 0 0 0 0 0;
     0 0 0 0 0 0 0 0 0];

radar_cnt = size(radar_pos,2);
iters = duration/T;
target_num = size(target_init_state,2);
history = zeros(radar_cnt,target_num,3,iters);
measure_history = zeros(radar_cnt,target_num,3,iters);
pos_test = [10;10;10];
pos_test_num = 10;
estimation_errors = zeros(radar_cnt,3,pos_test_num);
for test_index=1:pos_test_num
    radar_pos(:,2) = radar_pos(:,2)+test_index*pos_test;
    for tag=1:radar_cnt
        target_pos = target_init_state;
        radar_position = radar_pos(:,tag);
        Y = [];
        A = [];
        for index=1:iters
            target_pos = F*target_pos;
            for i=1:target_num
                target = target_pos(1:3,i);
                history(tag,i,1:3,index) = target;
                dis = sqrt(sum((radar_position-target).^2));
                angle = atan((radar_position(2)-target(2))/(radar_position(1)-target(1)));
                tmp_dis = sqrt(sum((radar_position(1:2) - target(1:2)).^2));
                pitch_angle = atan((target(3)-radar_position(3))/tmp_dis);
                m_dist = dis+radar_deviation(1,tag)+randn*radar_deviation(4,tag);
                m_angle = angle + radar_deviation(2,tag)+randn*radar_deviation(5,tag);
                m_pitch_angle = pitch_angle + radar_deviation(3,tag)+randn*radar_deviation(6,tag);
                measure_position = [m_dist*cos(m_pitch_angle)*cos(m_angle)+radar_position(1);
                     m_dist*cos(m_pitch_angle)*sin(m_angle)+radar_position(2);
                     m_dist*sin(m_pitch_angle)+radar_position(3)];
                measure_history(tag,i,1:3,index) = measure_position;
                y = measure_position - target;
                Y = [Y;y];
                a = [cos(pitch_angle)*cos(angle) -dis*cos(pitch_angle)*sin(angle) -dis*sin(pitch_angle)*cos(angle);
                     cos(pitch_angle)*sin(angle)  dis*cos(pitch_angle)*cos(angle) -dis*sin(pitch_angle)*sin(angle);
                     sin(pitch_angle)             0                                dis*cos(pitch_angle)];
                A = [A;a];
            end    
        end
        estimation_errors(tag,1:3,test_index) = abs(radar_deviation(1:3,tag)-inv(A'*A)*A'*Y);
    end
end

title_str = cell(3);
title_str{1} = '¾àÀëÏµÍ³Îó²î¾ø¶ÔÎó²î';
title_str{2} = '·½Î»½ÇÏµÍ³Îó²î¾ø¶ÔÎó²î';
title_str{3} = '¸©Ñö½ÇÏµÍ³Îó²î¾ø¶ÔÎó²î';
close all;
estimation_errors(2,:,:)
x=1:10;
for plot_index=1:3
    subplot(1,3,plot_index)
    tmp = reshape(estimation_errors(2,plot_index,:),pos_test_num,1);
    plot(x,tmp,'LineWidth',2)
    grid on
    title(title_str{plot_index})
end