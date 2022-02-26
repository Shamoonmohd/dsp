%% 
% 
% 
% Reading the image and constructing the data :

clear 
close all
x = (imread('barbara.png'));
[h,w] = size(x);
figure
imshow(x)
%% 
% 
% 
% Making the desired filter using the FIR filter design functions 

[n,fo,ao,weight] = firpmord(0.5*7418*[0.75 0.78],[1 0],[0.01 0.01],7418);

b = firpm(n,fo,ao,weight);

%% 
% . we plot its pole zero diagram.
% 
% 

[br,a] = eqtflength(b,1);
sys1 = tf(br,a);
pzmap(sys1)

%% 
% 
% 
% We obsesrve that the filter has a pole at zero and zeros on the unit circle. 
% as expected from the amplitude and frequancy properties :

for i = 1:h
    y1(i,1:w) = filtfilt(br,a,double(x(i,1:w)));
end
imshow(y1)
%% 
% The filtered image doesnt contain any useful data. Acually its an empty image 
% : 
% 
% 
%% 
% Now constructing the minimum phase filter by keeepign all the zeros out of 
% the unit circle and scaling the gain. 
% 
% 

[z,p,k] = tf2zp(br,a);
len = length(z);
km = k;
z_min = zeros(len,1);
z_mag = abs(z);
for i = 1:len
    if(z_mag(i)> 1)
        z_min(i) = 1/conj(z(i));
km = km*z_mag(i);
    else
z_min(i) = z(i);
    end
end

%plotting the pole zero diagram of the new filter

[b_min,a_min] = zp2tf(z_min,p,km);
sys = tf(b_min,a_min);
pzmap(sys)
%% 
% 
% 
% PLotting the frequency responses and comapring the two filters" 

[H,W] = freqz(b);
[H1,W1] = freqz(b_min,a_min);
subplot(2,1,1)

plot(W/pi,20*log(abs(H)),W1/pi,20*log(abs(H1)))
title('Magnitude Plot')
legend('MinMax Filter','Min phase filter ')
subplot(2,1,2)

plot(W/pi,unwrap(angle(H)*2)/2,W1/pi,unwrap(angle(H1)*2)/2)
legend('MinMax Filter','Min phase filter ')
title('Phase plot')
%% 
% 
% 
% *Observation :* We see that magnitude wise these two filters are oppsite. 
% The minamx FIR behaves as low pass filter while the minimum phase behaves as 
% a high pass filter. In the phase plot we observe that the min phase has zero 
% phase till the cutoff frequency. while the MIN max FIR filter has a linear phase 
% response. 
%% 
% Appltying the filter we see that the image as 

for i = 1:h
    y2(i,1:w) = filtfilt(b_min,a_min,double(x(i,1:w)));
end
    imshow(y2)
    
%% 
%