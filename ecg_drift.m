clc;
clear all ;

load ecg_lfn.dat;
r = [0.2,0.3,0.4,0.6,0.8,0.9];

for i = 1:6    
    y = filter([1,-1],[1,-r(i)],ecg_lfn);
    
    figure(i)

    plot(ecg_lfn,'b')
    
    hold on 
    plot(y,'r')
   
    legend('Original Signal','Filtered signal')
    title(['Filtering with pole at r=',num2str(r(i))])
    hold off
end

for i = 1:6    
    [h,w] = freqz([1,-1],[1,-r(i)]);
    
    figure(i)
    plot(w/pi,20*log(abs(h)))
    legend('Filter response')
    title(['Filter response with pole at r=',num2str(r(i))])
    hold off
end