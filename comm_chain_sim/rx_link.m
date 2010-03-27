function rx_link(num_rx, chan_mode, code, delay, reset_packet_num, filename, plot, append, test_mode)

if nargin < 1
  num_rx = 1;
  chan_mode = 1;
  code = 0;
  delay = 0;
  reset_packet_num = -1;
  filename = 'matlab_out';
  plot = 0;
  append = 0;
  test_mode = 0;
elseif nargin < 2
  chan_mode = 1;
  code = 0;
  delay = 0;
  reset_packet_num = -1;
  filename = 'matlab_out';        
  plot = 0;
  append = 0;    
  test_mode = 0;
elseif nargin < 3
  code = 0;
  delay = 0;
  reset_packet_num = -1;
  filename = 'matlab_out';    
  plot = 0;
  append = 0;    
  test_mode = 0;
elseif nargin < 4
  delay = 0;
  reset_packet_num = -1;
  filename = 'matlab_out';    
  plot = 0;
  append = 0;    
  test_mode = 0;
elseif nargin < 5
  reset_packet_num = -1;
  filename = 'matlab_out';    
  plot = 0;
  append = 0;    
  test_mode = 0;
elseif nargin < 6
  filename = 'matlab_out';
  plot = 0;
  append = 0;    
  test_mode = 0;
elseif nargin < 7
  plot = 0;
  append = 0;    
  test_mode = 0;
elseif nargin < 8
  append = 0;
  test_mode = 0;
elseif nargin < 9
  test_mode = 0;
end

if plot > 0
  close all
end

if test_mode > 0
  append = 1;
end

%Make Packet
packet_size = 1500; %in bytes , 1 byte = 8bits
beacon_id = 42;
max_delay = 5;

packet = make_packet(beacon_id,packet_size,reset_packet_num);

if test_mode > 0
  f1 = fopen(filename, 'a');
  fprintf(f1, '***PKT\n');
  fprintf(f1, '%d', packet);
  fprintf(f1, '\n***PKT\n');
  fclose(f1);
end

if delay > 0
  sleep_time = randi(max_delay + 1) - 1;
  fprint('Random Backoff: %d seconds',sleep_time);
  pause(sleep_time)
end

packet = reshape(packet,[],1);

original_packet = packet;

%Encode
if code > 0
  coded_packet = encoder(packet);
else
  coded_packet = packet;
end

%Modulation
tx_signal = digi_modulator(coded_packet,'dqpsk',plot);

%Amplification
tx_signal = tx_signal * 10^(35/10);


if test_mode > 0
  f1 = fopen(filename, 'a');
  fprintf(f1, '***TX\n');
  fprintf(f1, '%d::', tx_signal);
  fprintf(f1, '\n***TX\n');
  fclose(f1);
end




%Channel
if test_mode > 0
  f1 = fopen(filename, 'a');
end

fprintf('Chan_mode: %d\n',chan_mode);

rx_signals = cell(1,num_rx);
delays = zeros(1,num_rx);
for i=1:num_rx
  [rx_signal, delay] = channel(tx_signal, chan_mode);
% $$$   rx_signal = tx_signal;
  rx_signals{i} = rx_signal;
  delays(i) = delay;
  
  if test_mode > 0
    fprintf(f1, '***RX\n');
    fprintf(f1, '%d::', rx_signal);
    fprintf(f1, '\n***RX\n');
  end
end

if test_mode > 0
  fclose(f1);
end


%Demod and decode
len_orig = size(original_packet);
len_orig = len_orig(1);

demod_waves = cell(1, num_rx);
for i=1:num_rx
  dropped = 1;
  wave = digi_demodulator(rx_signals{i},'dqpsk', plot);
  
  if code > 0
    wave = decoder(wave);
  end
  
  demod_waves{i} = wave;
  
% $$$   len = size(wave);
% $$$   len = len(1);
% $$$   if len_orig == len
% $$$     if wave == original_packet
% $$$       demod_waves{i} = wave;
% $$$       dropped = 0;
% $$$     else
% $$$       fprintf('Data Mismatch->');
% $$$     end
% $$$   else
% $$$     fprintf('Length Mismatch->');
% $$$   end
% $$$  
% $$$   if dropped == 1
% $$$     fprintf('dropped\n');
% $$$     demod_waves{i} = 'dropped';
% $$$   end
end
%Writ to File

file_flag = 'w';
if append > 0 
  file_flag = 'a';
end

f1 = fopen(filename, file_flag);
for i=1:num_rx
  fprintf(f1,'###\n');
  if ~isnumeric(demod_waves{i})
    fprintf(f1, demod_waves{i});
  else
    fprintf(f1,'%d',demod_waves{i});
  end
  fprintf(f1,'\n');
  fprintf(f1,'%d',delays(i));
  fprintf(f1,'\n###\n');
end
fclose(f1);

exit
