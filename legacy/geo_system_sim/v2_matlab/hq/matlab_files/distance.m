function [ d ] = distance( p1,p2 )
%DISTANCE Distance between two points on earth's surface
% calculates distance between 2 points on earths surface
% assumes same hemisphere (i think) uses mean earth radius
% r = 6371 km
%
% input: p1,p2   location in the form (lon,lat)
% return: d      distance in meters   

earth_radius = 6371e3;




lon1 = p1(1) / 180 * pi;
lat1 = p1(2) / 180 * pi;


lon2 = p2(1) / 180 * pi;
lat2 = p2(2) / 180 * pi;

e = acos( sin(lat1)*sin(lat2) + ...
          cos(lat1)*cos(lat2)*cos(lon2-lon1) );
d = e * earth_radius;
end

