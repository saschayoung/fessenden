function [ t ] = time_of_flight( p1,p2 )
%TIME_OF_FLIGHT Calcalate time of flight between two points on earth's
%surface
%   

speed_of_light = 299792458.0;

d = distance(p1,p2);
t = d / speed_of_light;
end

