function [ x0, y0 ] = tdoa_sim( tx,rx1,rx2,rx3 )
% function intersection = tdoa_sim( tx,rx1,rx2,rx3 )
% TDOA_SIM - primary tdoa sim block in matlab
%   

x_tx = tx(1);
y_tx = tx(2);

x_rx1 = rx1(1);
y_rx1 = rx1(2);

x_rx2 = rx2(1);
y_rx2 = rx2(2);

x_rx3 = rx3(1);
y_rx3 = rx3(2);

tof_1 = time_of_flight(tx,rx1);
tof_2 = time_of_flight(tx,rx2);
tof_3 = time_of_flight(tx,rx3);

[x_h1 y_h1] = hyperbola(rx1,rx2,tof_1,tof_2);
[x_h2 y_h2] = hyperbola(rx1,rx3,tof_1,tof_3);

[x0,y0] =  intersections(x_h1,y_h1,x_h2,y_h2)

plot(x_h1,y_h1,x_h2,y_h2,x0,y0,'*')

