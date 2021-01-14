gauAvg = smoothdata(impData1(:,2),'gaussian');
mvngMed = smoothdata(impData1(:,2),'movmedian');
ss1 = mean(gauAvg(end-500:end));
ss2 = mean(mvngMed(end-500:end));

figure(1);
plot(impData1(:,1),gauAvg)
hold on;
%plot(impData1(:,1),mvngMed)
plot(impData1(:,1),ss1*ones(size(impData1(:,1))),'--k')
%plot(impData1(:,1),ss2*ones(size(impData1(:,1))),'--b')

title('Normal Position Control Implemented results with gaussian Filter')
xlabel('Time in sec')
ylabel('theta "\theta"')
legend('System Response [Filtered]', 'Steady State')

figure(2);
plot(impData1(:,1),mvngMed)
hold on;
plot(impData1(:,1),ss2*ones(size(impData1(:,1))),'--k')

title('Normal Position Control Implemented results with Moving Median Filter')
xlabel('Time in sec')
ylabel('theta "\theta"')
legend('System Response [Filtered]', 'Steady State')
