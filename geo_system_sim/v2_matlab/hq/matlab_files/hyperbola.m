function [ x_hyperbola_p, y_hyperbola_p ] = hyperbola( p1,p2,toa1,toa2 )
%HYPERBOLA Calculate tdoa hyperbola
%         calculates hyperbola that represents equidifference
%         curves for time of arrival (TDOA) for two points.
% 
%         input:
%                p1,p2           location in the form (lat,lon)
%                toa1,toa2       timestamp in seconds
% 
%         return:
%                (x1,y1,x2,y2)   x & y coordinates of asymptotes 1 & 2

DEBUG = 1;

speed_of_light = 299792458.0;




% convert to UTM--or not
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% $$$ [x1, y1] = grn2eqa(p1(1),p1(2))
% $$$ [x2, y2] = grn2eqa(p2(1),p1(2))

x1 = p1(1);
y1 = p1(2);

x2 = p2(1);
y2 = p2(2);

alpha = atan((y2-y1)/(x2-x1));

if DEBUG
  fprintf('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
  fprintf('hyperbola.m\n')
  fprintf('x1 = %.10f\n',x1)
  fprintf('y1 = %.10f\n',y1)
  fprintf('x2 = %.10f\n',x2)
  fprintf('y2 = %.10f\n',y2)  
  fprintf('alpha: %1.10f\n',alpha)
end % if DEBUG

m = midpoint(p1,p2);
x_0 = m(1);
y_0 = m(2);

a = (0.5)*speed_of_light*(abs(toa1 - toa2))/(60*1852);
d = distance(p1,p2)/(60*1852);
b = sqrt((d/2.0)^2 - a^2);
dd = speed_of_light*((toa1 - toa2))/(60*1852);

if DEBUG
  fprintf('a = %.10f\n', a)
  fprintf('distance = %.10f\n', d)
  fprintf('b = %.10f\n', b)
  fprintf('dd = %.10f\n',dd)
end % if DEBUG

t = linspace(-3,3,100);

if (x1 < x2)
    fprintf ('x1 < x2 \n');
    if (dd < 0)
        fprintf ('dd < 0 \n');
        x_hyperbola = -a*cosh(t);
        y_hyperbola =  b*sinh(t);
    else %if (dd > 0)
        fprintf ('dd > 0 \n');
        x_hyperbola = a*cosh(t);
        y_hyperbola = b*sinh(t);
    end
else %if (x1 > x2)
    fprintf ('x1 > x2 \n');
    if (dd > 0)
        fprintf ('dd > 0 \n');
        x_hyperbola = -a*cosh(t);
        y_hyperbola =  b*sinh(t);
    else %if (dd < 0)      
        fprintf ('dd < 0 \n');
        x_hyperbola = a*cosh(t);
        y_hyperbola = b*sinh(t);
    end
end

% $$$ x_hyperbola_utm = x_hyperbola*cos(alpha) - y_hyperbola*sin(alpha)+x_0; 
% $$$ y_hyperbola_utm = x_hyperbola*sin(alpha) + y_hyperbola*cos(alpha)+y_0;
% $$$ 
% $$$ [x_hyperbola_p, y_hyperbola_p] = eqa2grn(x_hyperbola_utm,y_hyperbola_utm);

x_hyperbola_p = x_hyperbola*cos(alpha) - y_hyperbola*sin(alpha)+x_0; 
y_hyperbola_p = x_hyperbola*sin(alpha) + y_hyperbola*cos(alpha)+y_0;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


















% $$$ x_hyperbola_utm = x_hyperbola*cos(alpha) - y_hyperbola*sin(alpha)+x_0;
% $$$ y_hyperbola_utm = x_hyperbola*sin(alpha) + y_hyperbola*cos(alpha)+y_0 ;
% $$$ length(x_hyperbola_utm)
% $$$ size(x_hyperbola_utm)
% $$$ length(y_hyperbola_utm)
% $$$ size(y_hyperbola_utm)
% $$$ a = ones(1,length(x_hyperbola_utm));
% $$$ zone = '18 S' * a';
% $$$ length(zone)
% $$$ size(zone)
% $$$ 
% $$$ x_hyperbola_utm = x_hyperbola_utm'
% $$$ y_hyperbola_utm = y_hyperbola_utm'
% $$$ zone = zone'
% $$$ [x_hyperbola_p, y_hyperbola_p] = utm2deg(x_hyperbola_utm, y_hyperbola_utm, ...
% $$$ 					 zone)

% second iteration
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% $$$ x1 = rx1_lon;
% $$$ y1 = rx1_lat;
% $$$ p1 = [x1 y1];
% $$$ 
% $$$ x2 = rx3_lon;
% $$$ y2 = rx3_lat;
% $$$ p2 = [x2 y2];
% $$$ 
% $$$ alpha = atan((y2-y1)/(x2-x1));
% $$$ if DEBUG
% $$$   fprintf('x1 = %.10f\n',x1)
% $$$   fprintf('y1 = %.10f\n',y1)
% $$$   fprintf('x2 = %.10f\n',x2)
% $$$   fprintf('y2 = %.10f\n',y2)  
% $$$   fprintf('alpha: %1.10f\n',alpha)
% $$$ end % if DEBUG
% $$$ 
% $$$ m = midpoint(p1,p2);
% $$$ x_0 = m(1);
% $$$ y_0 = m(2);
% $$$ 
% $$$ toa1 = time_of_flight(tx,p1);
% $$$ toa2 = time_of_flight(tx,p2);
% $$$ 
% $$$ a = (0.5)*speed_of_light*(abs(toa1 - toa2))/(60*1852);
% $$$ d = distance(p1,p2)/(60*1852);
% $$$ b = sqrt((d/2.0)^2 - a^2);
% $$$ dd = speed_of_light*((toa1 - toa2))/(60*1852);
% $$$ 
% $$$ 
% $$$ if DEBUG
% $$$   fprintf('a = %.10f\n', a)
% $$$   fprintf('distance = %.10f\n', d)
% $$$   fprintf('b = %.10f\n', b)
% $$$   fprintf('dd = %.10f\n',dd)
% $$$ end % if DEBUG
% $$$   
% $$$ 
% $$$ t = linspace(-3,3,100);
% $$$ 
% $$$ 
% $$$ 
% $$$ if (x1 < x2)
% $$$     fprintf ('x1 < x2 \n');
% $$$     if (dd < 0)
% $$$         fprintf ('dd < 0 \n');
% $$$         x_hyperbola = -a*cosh(t);
% $$$         y_hyperbola =  b*sinh(t);
% $$$     end
% $$$     
% $$$     if (dd > 0)
% $$$         fprintf ('dd > 0 \n');
% $$$         x_hyperbola = a*cosh(t);
% $$$         y_hyperbola = b*sinh(t);
% $$$     end
% $$$ end
% $$$     
% $$$ if (x1 > x2)
% $$$     fprintf ('x1 > x2 \n');
% $$$     if (dd > 0)
% $$$         fprintf ('dd > 0 \n');
% $$$         x_hyperbola = -a*cosh(t);
% $$$         y_hyperbola =  b*sinh(t);
% $$$     end
% $$$     
% $$$     if (dd < 0)
% $$$         fprintf ('dd < 0 \n');
% $$$         x_hyperbola = a*cosh(t);
% $$$         y_hyperbola = b*sinh(t);
% $$$     end
% $$$ end
% $$$ 
% $$$ x_hyperbola_p = x_hyperbola*cos(alpha) - y_hyperbola*sin(alpha)+x_0; 
% $$$ y_hyperbola_p = x_hyperbola*sin(alpha) + y_hyperbola*cos(alpha)+y_0; 
% $$$ 
% $$$ plot(x_hyperbola_p,y_hyperbola_p)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% $$$ tx_lon = -77.0647611111111;
% $$$ tx_lat = 38.80734722222222;
% $$$ 
% $$$ rx1_lon = -77.03778888888888;
% $$$ rx1_lat = 38.81201111111111;
% $$$ 
% $$$ rx2_lon = -77.06365833333334;
% $$$ rx2_lat = 38.80172777777778;
% $$$ 
% $$$ rx3_lon = -77.08458333333333;
% $$$ rx3_lat = 38.82368333333334;
% $$$ 
% $$$ rx4_lon = -77.04163611111112;
% $$$ rx4_lat = 38.79973611111111;
% $$$ 
% $$$ if DEBUG
% $$$   fprintf('Transmitter coordinates:\t\t(%3.15f,%3.15f)\n', tx_lon,tx_lat)
% $$$   fprintf('RX1 - Boathouse coordinates:\t\t(%3.15f,%3.15f)\n',rx1_lon,rx1_lat)
% $$$   fprintf('RX2 - USPTO coordinates:\t\t(%3.15f,%3.15f)\n',rx2_lon,rx2_lat)
% $$$   fprintf('RX3 - TC Williams HS coordinates:\t(%3.15f,%3.15f)\n',rx3_lon,rx3_lat)
% $$$   fprintf('RX4 - Lee St Park coordinates:\t\t(%3.15f,%3.15f)\n',rx4_lon,rx4_lat)
% $$$ end


% $$$ tx = [tx_lon tx_lat];
% $$$ toa1 = time_of_flight(tx,p1);
% $$$ toa2 = time_of_flight(tx,p2);
