clc; clear all;
DEBUG = 1;

tx_lon = -77.0647611111111;
tx_lat = 38.80734722222222;
tx = [tx_lon tx_lat];

rx1_lon = -77.03778888888888;
rx1_lat = 38.81201111111111;
rx1 = [rx1_lon rx1_lat];

rx2_lon = -77.06365833333334;
rx2_lat = 38.80172777777778;
rx2 = [rx2_lon rx2_lat];

rx3_lon = -77.08458333333333;
rx3_lat = 38.82368333333334;
rx3 = [rx3_lon rx3_lat];

rx4_lon = -77.04163611111112;
rx4_lat = 38.79973611111111;
rx4 = [rx4_lon rx4_lat];


if DEBUG
  fprintf('Transmitter coordinates:\t\t(%3.15f,%3.15f)\n', tx_lon,tx_lat)
  fprintf('RX1 - Boathouse coordinates:\t\t(%3.15f,%3.15f)\n',rx1_lon,rx1_lat)
  fprintf('RX2 - USPTO coordinates:\t\t(%3.15f,%3.15f)\n',rx2_lon,rx2_lat)
  fprintf('RX3 - TC Williams HS coordinates:\t(%3.15f,%3.15f)\n',rx3_lon,rx3_lat)
  fprintf('RX4 - Lee St Park coordinates:\t\t(%3.15f,%3.15f)\n',rx4_lon,rx4_lat)
end

x_results = []
y_results = []

hold on
% $$$ tdoa_sim(tx,rx1,rx2,rx3)
[x_intersection,y_intersection] = tdoa_sim(tx,rx1,rx2,rx3)
x_results = [x_results; x_intersection]
y_results = [y_results; y_intersection]

% $$$ tdoa_sim(tx,rx1,rx3,rx4)
[x_intersection,y_intersection] = tdoa_sim(tx,rx1,rx3,rx4)
x_results = [x_results; x_intersection]
y_results = [y_results; y_intersection]

[x_intersection,y_intersection] = tdoa_sim(tx,rx2,rx3,rx4)
x_results = [x_results; x_intersection]
y_results = [y_results; y_intersection]

% first iteration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% $$$ x1 = rx1_lon;
% $$$ y1 = rx1_lat;
% $$$ 
% $$$ x2 = rx2_lon;
% $$$ y2 = rx2_lat;
% $$$ 
% $$$ 
% $$$ tof_1 = time_of_flight(tx,rx1);
% $$$ tof_2 = time_of_flight(tx,rx2);
% $$$ tof_3 = time_of_flight(tx,rx3);
% $$$ tof_4 = time_of_flight(tx,rx4);
% $$$ 
% $$$ [t_x1,t_y1] = hyperbola(rx1,rx2,tof_1,tof_2);
% $$$ [t_x3,t_y3] = hyperbola(rx1,rx3,tof_1,tof_3);
% $$$ [t_x5,t_y5] = hyperbola(rx1,rx4,tof_1,tof_4);
% $$$ [t_x7,t_y7] = hyperbola(rx2,rx3,tof_2,tof_3);
% $$$ [t_x9,t_y9] = hyperbola(rx2,rx4,tof_2,tof_4);
% $$$ [t_x11,t_y11] = hyperbola(rx3,rx4,tof_3,tof_4);
% $$$ 
% $$$ 
% $$$ plot(x_tx,y_tx,'^-',x1,y1,'^',x2,y2,'^',...
% $$$      x3,y3,'^',x4,y4,'^',...
% $$$      t_x5,t_y5,'b',...
% $$$      t_x7,t_y7,'g')
% $$$ 
% $$$  
% $$$ % plot(x_tx,y_tx,'^-',x1,y1,'^',x2,y2,'^',...
% $$$ %      x3,y3,'^',x4,y4,'^',...
% $$$ %      t_x5,t_y5,'r');
% $$$ 
% $$$ %[x0,y0] = intersections(t_x1,t_y1,t_x3,t_y3);
% $$$ 
% $$$ % x0
% $$$ % y0
% $$$  