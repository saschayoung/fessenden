function [ m ] = midpoint( p1,p2 )
%MIDPOINT Calculate midpoint between two points on earth's surface
%       calculates midpoint between 2 points on earths surface
%       assumes points are not geographically diverse so that 
%       ( (x1+x2)/2, (y1+y2)/2 ) is not sufficiently different from
%       midpoint along great circle route
% 
%       input: p1,p2   location in the form (lat,lon)
%       return: m      midpoint in the form (lat,lon)

lon = ( p1(1) + p2(1) )/2.0;
lat = ( p1(2) + p2(2) )/2.0;

m = [lon lat];

end

