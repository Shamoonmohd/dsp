%% 
% *Question 1*

vowel = audiorecorder(16000,16,1);

disp(" Start of Clip")
recordblocking(vowel,1);
play(vowel)
disp("End of clip")

x = getaudiodata(vowel);
audiowrite("vowel.wav",x,16000)
n = 1:16000;
k =1:800;

x1 = x(10000:10799);

subplot(2,1,1)
plot(n,x)
title(" speech signal of a vowel fs = 16kHz 16 bit")

subplot(2,1,2)
plot(k,x1)
title( "50 ms clip showing periodic behaviour of the vowel sound")
%% 
% 
% 
% From the graph we see that the period of the vowel sound is around 100 samples. 
% 
% thus $\textrm{pitch}\;\textrm{period}\;,\;T=\frac{471-371}{\textrm{Fs}}=\frac{100}{16000}=6\ldotp 
% 25\;\textrm{ms}\;\;\left(\textrm{approx}\ldotp \right)$ 
%% 
% The consonant sound : 

const = audiorecorder(16000,16,1);

disp(" Start of Clip")
recordblocking(const,1);
play(const)
disp("End of clip")

y = getaudiodata(const);
sound(y)
n = 1: 16000;
plot(n,y)
k =1:800;
y1 = y(10000:10799);
subplot(2,1,1)
plot(n,y)
title(" speech signal of a constonant fs = 16kHz 16 bit")
subplot(2,1,2)
plot(k,y1)
title( "50 ms clip of the constonant sound q ")
%% 
% Question 2 FFT

fftx1 = fft(x1);
lg_x1 = 20*log10(abs(x1));
ffty1 = fft(y1);
lg_y1 = 20*log10(abs(y1));
subplot(2,2,1)
spectrogram(fftx1)
title('Vowel')
subplot(2,2,2)
spectrogram(ffty1)
title('Constonant')
subplot(2,2,3)
plot(k,lg_x1)
title('Log plot of vowel')
subplot(2,2,4)
plot(k,lg_y1)
title('Log plot of constonant')
%% 
%