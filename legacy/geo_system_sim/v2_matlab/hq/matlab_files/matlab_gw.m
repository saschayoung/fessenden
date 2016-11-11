function matlab_gw()
% MATLAB_GW - gateway to matlab tdoa functions
%   x1,y1,x2,y2,x3,y3,toa1,toa2,toa3)

f = fopen('matlab_gw_params')

x1 = str2double(fgetl(f));
y1 = str2double(fgetl(f));
x2 = str2double(fgetl(f));
y2 = str2double(fgetl(f));
x3 = str2double(fgetl(f));
y3 = str2double(fgetl(f));
toa1 = str2double(fgetl(f));
toa2 = str2double(fgetl(f));
toa3 = str2double(fgetl(f));

fclose(f);

ERR = 0;

p1 = [x1 y1];
p2 = [x2 y2];
p3 = [x3 y3];
      
if ( (toa1 == toa2) & (toa1 == toa3) )
  if ERR
    fprintf('\n\n\n\n\n\n\nerror!!!\n')
    fprintf('(toa1 == toa2) and (toa1 == toa3)!!\n')
    fprintf('\n\n\n\n\n\n\n')
  end
  

elseif ( (toa1 == toa2) & ~(toa1 == toa3) )
  [x_h1,y_h1] = hyperbola(p3,p2,toa3,toa2);
  [x_h2,y_h2] = hyperbola(p1,p3,toa1,toa3);
elseif ( not (toa1 == toa2) & (toa1 == toa3) )
  [x_h1,y_h1] = hyperbola(p1,p2,toa1,toa2);
  [x_h2,y_h2] = hyperbola(p2,p3,toa2,toa3);
else
  [x_h1,y_h1] = hyperbola(p1,p2,toa1,toa2);
  [x_h2,y_h2] = hyperbola(p1,p3,toa1,toa3);
end

if ( isnan(x_h1(1)) | isnan(y_h1(1)) )
  if ERR
    fprintf('\n\n\n\n\n\n\n\n\n\n\n\n\nerror!!!\n')
    fprintf('isnan(x_h1(0)) or isnan(y_h1(0))!!\n')
    fprintf('\n\n\n\n\n\n\n\n\n\n\n\n\n')
  end
elseif ( isnan(x_h2(1)) | isnan(y_h2(1)) )
  if ERR
    fprintf('\n\n\n\n\n\n\n\n\n\n\n\n\nerror!!!\n')
    fprintf('isnan(x_h2(0)) or isnan(y_h2(0))!!\n')
    fprintf('\n\n\n\n\n\n\n\n\n\n\n\n\n')
  end    
end
   
try
  [x_coords, y_coords] = intersections(x_h1,y_h1,x_h2,y_h2);
catch
  x_coords = -1;
  y_coords = -1;
  if ERR
    fprintf('intersection.m returns no data, return -1 to main')
  end
end
  




	
	
	

fid = fopen('../results','w+');
fprintf(fid, '%.15f\n%.15f\n', x_coords, y_coords);
fclose(fid);

exit
