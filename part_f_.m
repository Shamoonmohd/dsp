clear 
load DataEOG.txt
x = DataEOG;

h = ones(1,67)/67;
y = conv(x,h);

y2= y;
y2(1:33) = [];
y2(end-32:end) = [];

len = length(y2)
n = 1:len;
plot(n,x,'r',n,y2,'k')