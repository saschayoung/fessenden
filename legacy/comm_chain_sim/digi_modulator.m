function modulated_wave = digi_modulator(signal, mod_type, plot)
%%%%%%%%%%%%%%%%%%%%%
%11 August 2009 
%Modulates input binary vector using M symbols
%M is default set to 16
%default mod_type is qam
%allows qam, dpsk, and psk
%basic error checking currently
%%%%%%%%%%%%%%%%%%%%%

%check for a signal
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
    mod_type = 'dbpsk';
    plot = 0;
elseif nargin < 3
    plot = 0;    
end

%ploting to show modulation affect on the signal
%here the inital input is shown
if plot == 1
    figure();
    stem(signal(1:40),'filled');
    title('Input Bits');
    xlabel('Bit Index'); ylabel('Binary Value');
end

%determination of M
switch lower(mod_type)
    case 'dbpsk'
        M = 1;
    case 'dqpsk'
        M = 2;
    case 'qam'
        M = 4;
end

%determination of necessary number of bits
k = log2(M);

%pads signal with trailing zeros if necessary
modulo=mod(length(signal),k);
if ~(modulo == 0)
    signal = [signal; zeros(k-modulo,1)];
end

%grouping bits into symbols as defined by M
symbols = bi2de(reshape(signal,k,length(signal)/k).','left-msb');


%here symbol values are shown
if plot == 1
    figure;
    stem(symbols(1:40));
    title('Input Symbols')
    xlabel('Symbol Index'); ylabel('Interger Value');
end

switch lower(mod_type)
    case 'qam'
        h=modem.qammod(M);
    case 'dbpsk'
        h=modem.dpskmod('M', M);
    case 'dqpsk'
        h=modem.pskmod(M);
    otherwise
        if ~(ischar(mod_type))
            mod_type = num2str(mod_type);
        end
        ME=MException('digMod:badModType','Mod_type %s not recognised, options are: qam, dbpsk, or dqpsk', mod_type);
        throw(ME)
end

%finally the data is modulated
modulated_wave = modulate(h,symbols);

%here the modulated constellation is shown
if plot == 1
    scatterplot(modulated_wave,1,0,'k*');
    title('Modulated Constellation');
end
