% Radar Estimator - Batch Estimator
% Author:qingyuanxingsi
% 2015-07-22

% time step
T = 1;

% duration
duration = 60;

% Radar Parameter Configuration
% System Deviation and noise
radar_deviation = [20   8    15;
                   0.03 0.04 0.01; 
                   0.02 0.02 0.02;
                   0.01 0.01 0.01;
                   0.01 0.01 0.01;
                   0.01 0.01 0.01];

% Radar position
radar_pos = [50  70  20;
             120 150 160;
             20  30  30];


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
    estimate_error = inv(A'*A)*A'*Y
end

% Plot the trajectory of the targets measured by different sensors
close all;
for tag=1:radar_cnt
    for i=1:target_num
        path = reshape(history(tag,i,:,:),3,iters);
        measure_path = reshape(measure_history(tag,i,:,:),3,iters);
        plot_index = (tag-1)*target_num+i;
        subplot(radar_cnt,target_num,plot_index);
        plot3(path(1,:),path(2,:),path(3,:))
        grid on
        hold on
        plot3(measure_path(1,:),measure_path(2,:),measure_path(3,:))
        title(['Radar ' num2str(tag) ' Target ' num2str(i)])
    end
end
