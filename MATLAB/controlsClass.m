%% Class 2
close all; clear all;
%% Systesm
Gp = tf([1 20],[1 5.4 2 0]);

%% Desired System calculations
zetaDes = 0.5912;
wnDes = 0.4511;
% Desired poles
Sd1 = (-zetaDes*wnDes + 1i*wnDes*sqrt(1-zetaDes^2));
Sd2 = (-zetaDes*wnDes - 1i*wnDes*sqrt(1-zetaDes^2));
% calculating phase
phi = phase(freqresp(Gp,Sd1))*180/pi -360;
phiC = -180 - phi;
% Taking one pole as zero
zc = -0.4;
phiZc = phase(Sd1-zc)*180/pi;
phiPc = phiZc - phiC;
% Finding pole
pc = real(Sd1) - imag(Sd1)/tand(phiPc);
% Finding Gain
K = abs(Sd1-pc)/(abs(Sd1-zc)*abs(freqresp(Gp,Sd1)));

% Transient Compensator
Gct = K*tf([1 -zc],[1 -pc]);
essDes = 0.01;
KvDes = 1/essDes;
ramp = tf([1 0],[1]);
KvCurr =  abs(freqresp(ramp*Gp*Gct,essDes));
alphaLag = KvDes/KvCurr;
zc = real(Sd1)/100;
pc = zc/alphaLag;


Gcss = tf([1 -zc],[1 -pc]);
Gc = Gct*Gcss;
%t = 0:0.01:2000;
T = feedback(Gc*Gp,1)/ramp;
step(T)
hold on;
step(1/ramp)

stepinfo(T)

step(Gp)