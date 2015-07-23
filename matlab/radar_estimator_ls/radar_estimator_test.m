% Radar Estimator - Batch Estimator
% Author:qingyuanxingsi
% 2015-07-22

function estimation_error = radar_estimator_test(radar_system)

estimation_error = [];
T=1;
% duration
duration = 60;

% Radar Parameter Configuration
% System Deviation and noise
radar_deviation = [20  20;
                   0.03 0.03; 
                   0.02 0.02;
                   0.01 0.01;
                   0.01 0.01;
                   0.01 0.01];

radar_deviation(1:3,1) = radar_system;
radar_deviation(1:3,2) = radar_system;
               
% Radar position
radar_pos = [50  70;
             120 150;
             20  30];


% target initial states
target_init_state = [100 120;
                     100 120;
                     10  20;
                     10  15;
                     20  10;
                     10   5;
                     0   0;
                     0   0;
                     0   0];

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
iters = floor(duration/T);
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
    estimation_error = [estimation_error abs(radar_deviation(1:3,tag)-inv(A'*A)*A'*Y)];
end
estimation_error