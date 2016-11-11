function [rx_signal,average_delay] = channel(signal, chan_mode)

%make sure we get a signal
if (isempty(signal)) || (nargin < 1)
     ME=MException('digMod:noInput','%s requires an input signal', mfilename);
     throw(ME)
end

%basic check to see if it's binary
if (max(signal) > 1) || (min(signal) < 0)
     ME=MException('digMod:notBinaryInput', '%s expected binary input', mfilename);
     throw(ME)
end

%set defaults
if nargin < 2
    chan_mode = 1;
end

average_delay = -1;



switch(chan_mode)
 case 0
  awgn_mode = 0;
  flat_fading = 0;
  freq_specific_fading = 0;
  ranges = 0;
 case 1
  awgn_mode = 1;
  flat_fading  = 0;
  freq_specific_fading = 0;
  ranges = 1;
 case 2
  awgn_mode = 0;
  flat_fading = 1;
  freq_specific_fading = 0;
  ranges = 1;
 case 3
  awgn_mode = 0;
  flat_fading = 0;
  freq_specific_fading = 1;
  ranges = 1;
 case 4
  awgn_mode = 1;
  flat_fading = 1;
  freq_specific_fading = 0;
  ranges = 1;
 case 5
  awgn_mode = 1;
  flat_fading = 0;
  freq_specific_fading = 1;
  ranges = 1;
 case 6
  awgn_mode = 0;
  flat_fading = 1;
  freq_specific_fading = 1;
  ranges = 1;
 case 7
  awgn_mode = 1;
  flat_fading = 1;
  freq_specific_fading = 1;
  ranges = 1;
 case 8
  awgn_mode = 0;
  flat_fading = 2;
  freq_specific_fading = 0;
  ranges = 1;
 case 9
  awgn_mode = 0;
  flat_fading = 0;
  freq_specific_fading = 2;
  ranges = 1;
 case 10
  awgn_mode = 1;
  flat_fading = 2;
  freq_specific_fading = 0;
  ranges = 1;
 case 11
  awgn_mode = 1;
  flat_fading = 0;
  freq_specific_fading = 2;
  ranges = 1;
 case 12
  awgn_mode = 0;
  flat_fading = 2;
  freq_specific_fading = 1;
  ranges = 1;
 case 13
  awgn_mode = 0;
  flat_fading = 1;
  freq_specific_fading = 2;
  ranges = 1;
 case 14
  awgn_mode = 0;
  flat_fading = 2;
  freq_specific_fading = 2;
  ranges = 1; 
 case 15
  awgn_mode = 1;
  flat_fading = 2;
  freq_specific_fading = 1;
  ranges = 1;
 case 16
  awgn_mode = 1;
  flat_fading = 1;
  freq_specific_fading = 2;
  ranges = 1;
 case 17
  awgn_mode = 1;
  flat_fading = 2;
  freq_specific_fading = 2;
  ranges = 1;  
 otherwise
  awgn_mode = randi(2)-1;
  flat_fading = randi(3)-1;
  freq_specific_fading = randi(3)-1;
  ranges = 1;
end

switch(ranges)
 case 0
  delay = 0;
 
 case 1
  %Number of Paths
  max_paths = 20;
  min_paths = 1;
  num_paths = min_paths + randi(max_paths-min_paths);

  %samp_rate
  max_samp = 1000;
  min_samp = 1000;
  samp_rate = min_samp + (max_samp - min_samp).*rand();
  
  %max doppler
  max_speed = 10; %m/s
  min_speed = 0; %m/s
  speed = min_speed + (max_speed-min_speed).*rand();
  frequency = 500e6;
  max_doppler = speed*frequency/3e8;
  
  %SNR
  max_SNR = 30;
  min_SNR = 30;
  SNR = min_SNR + (max_SNR - min_SNR).*rand();
  
  %Path Delay
  %range from matlab docs on fading channels for typical outdoor delays
  max_delay = 1e-5;
  min_delay = 1e-7;
  
  delay = min_delay + (max_delay - min_delay)*rand(1,num_paths);
  
  average_delay = mean(delay);
  
  %Average Path Gain (dB)
  max_gain = 0;
  min_gain = -20;
    
  path_gain = min_gain + (max_gain - min_gain).*rand(1,num_paths);
                
  %Rician K-factor
  max_K = 100;
  min_K = 0;
        
  K = min_K + (max_K - min_K).*rand();
 otherwise
        
end

if flat_fading > 0
    %fprintf('Flat Fading Applied\n');
    if flat_fading == 1
        fade_channel = rayleighchan(1/samp_rate, max_doppler);
    elseif flat_fading == 2
        fade_channel = ricianchan(1/samp_rate, max_doppler, K);
    end
    signal = filter(fade_channel, signal);
end

if freq_specific_fading > 0
    %fprintf('Frequency Specific Fading Applied\n');
    if freq_specific_fading == 1
        fade_channel = rayleighchan(1/samp_rate, max_doppler, delay, path_gain);
    elseif freq_specific_fading == 2
        fade_channel = ricianchan(1/samp_rate, max_doppler, K, delay, path_gain);
    end
    signal = filter(fade_channel, signal);
end
        
if awgn_mode > 0
    %fprintf('Awgn Applied\n');
    signal = awgn(signal,SNR,'measured');
end

rx_signal = signal;
return

