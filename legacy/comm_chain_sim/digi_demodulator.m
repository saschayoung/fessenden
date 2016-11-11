function demodulated_wave = digi_demodulator(signal, mod_type, plot, over_samp)
%%%%%%%%%%%%%%%%%%%%%
%11 August 2009 
%Demodulates input digital signal
%M is default set to 16
%default mod_type is qam
%default oversampling rate is 1
%basic error checking currently
%%%%%%%%%%%%%%%%%%%%%

%check for a signal
if (isempty(signal)) || (nargin < 1)
    ME=MException('digDemod:noInput', '%s requires an input signal', mfilename);
    throw(ME)
end

%set defaults to mirror digi_modulator
if nargin < 2
    mod_type = 'dqpsk';    
    plot = 0;
    over_samp = 1;
elseif nargin < 3
    plot = 0;
    over_samp = 1;
elseif nargin < 4
    over_samp = 1;
end

%plot recieved data
if plot == 1 
    scatterplot(signal,over_samp,0,'k*');
    title('Received Constellation');
end

%build demodulator object
switch lower(mod_type)
    case 'qam'
        h=modem.qamdemod(4);
    case 'dbpsk'
        h=modem.dpskdemod('M', 1);
    case 'dqpsk'
        h=modem.pskdemod(2);
    otherwise
        if ~(ischar(mod_type))
            mod_type = num2str(mod_type);
        end
        ME=MException('digDemod:badModType','Mod_type %s not recognised, options are: qam, dbpsk, or dqpsk', mod_type);
        throw(ME)
end

%demodulate signal
symbols = demodulate(h,signal);

%plot symbols from demodulator
if plot == 1
    figure;
    stem(symbols(1:40));
    title('Demodulated Symbols')
    xlabel('Symbol Index'); ylabel('Interger Value');
end

%convert back to binary vector
demodulated_wave = de2bi(symbols, 'left-msb');
demodulated_wave = reshape(demodulated_wave.',[],1);

%plot bits out
if plot == 1
    figure;
    stem(signal(1:40),'filled');
    title('Demodulated Bits');
    xlabel('Bit Index'); ylabel('Binary Value');
end
