vowel = audiorecorder(16000,16,1);

disp(" Start of Clip")
recordblocking(vowel,2);
play(vowel)
disp("End of clip")

x = getaudiodata(vowel);

n = 1: 32000;
k =1:800;

x1 = x(13200:13999);

subplot(2,1,1)
plot(n,x)
title(" speech signal of a vowel fs = 16kHz 16 bit")

subplot(2,1,2)
plot(k,x1)
title( "50 ms clip showing periodic behaviour of the vowel sound")
