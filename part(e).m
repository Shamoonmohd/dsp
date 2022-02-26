clear 
load DataEOG.txt
x = DataEOG;

h = ones(1,31)/31;
y = conv(x,h);

y2= y;
y2(1:15) = [];
y2(end-14:end) = [];

len = length(y2)
n = 1: len;
plot(n,x,'r',n,y2,'k')