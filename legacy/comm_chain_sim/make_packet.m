function packet=make_packet(beacon_id, packet_size, reset)
persistent packet_num;

if nargin < 3
    reset = 0;
end

if reset > -1
    packet_num = reset;
end

payload1 = de2bi(uint16(packet_num));
payload1 = double(payload1);

payload2 = de2bi(uint16(beacon_id));
payload2 = double(payload2);

data_buffer = de2bi(uint8(packet_num));
data_buffer = double(data_buffer);

%pad the payload if necessary
len = size(payload1);
len = len(2);
if len<16
    pad = zeros(1,(16-len));
    payload1 = [payload1,pad];
end

len = size(payload2);
len = len(2);
if len<16
    pad = zeros(1, (16-len));
    payload2 = [payload2,pad];
end

len = size(data_buffer);
len = len(2);
if len<8
    pad = zeros(1, (8-len));
    data_buffer = [data_buffer,pad];
end

%reverse the payload so it goes a way that makes sense
payload1 = payload1(end:-1:1);
payload2 = payload2(end:-1:1);
data_buffer = data_buffer(end:-1:1);

packet = [payload1,payload2];

packet_size = packet_size -4;
for i=1:packet_size,
    packet = [packet,data_buffer];
end

packet_num = packet_num + 1;
return
end