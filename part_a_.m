clear 
load DataEOG.txt
x = DataEOG;

n = 1: 600;
% comment is added 
subplot(2,1,1)
plot(n,x)

h = ones(1,11)/11;

y = conv(x,h);

n = 1:610

subplot(2,1,2)
plot(n,y)
