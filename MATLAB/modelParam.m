close all;%clear all;
%% Plant Equations
load('normalPosData3.mat') % Data
% Initialization
iniForce = 0.0901;
zeta =  0.3;
wn =  1.9662+0.1;
gain = 435;

pos5_x = normalPosData3(:,1);
pos5_y = normalPosData3(:,2);
% Plant equation
Gp = tf(gain,[1 2*zeta*wn wn^2]);
[gpnum,gpden] = tfdata(Gp)
figure(5);
plot(pos5_x,pos5_y - pos5_y(1,1),'-r')
%hold on
%step(iniForce*Gp)
%% Designing a compensator 1
% Poles of the desired systems
syms a b;
rt = 3;
po = 5;
[a,b]= solve(pi-atan(sqrt(1 - a^2)/a)/(b*sqrt(1-a^2))-rt , 100*exp((-a*pi)/sqrt(1-a^2))-po);

zetaDes = double(a);
wnDes = double(b);

Sd1 = (-zetaDes*wnDes + 1i*wnDes*sqrt(1-zetaDes^2));
Sd2 = (-zetaDes*wnDes - 1i*wnDes*sqrt(1-zetaDes^2));
%Sd1=Sd2;
phi = phase(freqresp(Gp,Sd1))*180/pi-360;
phiC = -180 - phi;
zc = real(Sd1);
phiZc = phase(Sd1-zc)*180/pi;
phiPc = phiZc - phiC;
pc =    real(Sd1) - imag(Sd1)/tand(phiPc);
% Gain
K = abs(Sd1-pc)/(abs(Sd1-zc)*abs(freqresp(Gp,Sd1)));
% Lead compensator
Gct = K*tf([1 -zc],[1 -pc]);
essDes = 1;
KvDes = 1/essDes;
KvCurr =  abs(freqresp(Gp*Gct,essDes));
alphaLag = KvDes/KvCurr;
Zc = real(Sd1);
Pc = Zc/alphaLag;
% Compensator for steadystate
%Gcss = tf([1 -Zc],[1 -Pc]);
%Gc = Gct*Gcss;
% System
%G = Gc*Gp;
%% PD Controller system
T = -1/Pc;
Kp = K*Zc/Pc;
Kd = K*T;

C = tf([Kd Kp],[T 1]);
%% Plotting
%C1 = pid(0.01,0,0.005);
C1 = pid(0.09,0,1.6);

TT = feedback(C*Gp,1);
CF = feedback(C,Gp);
opt = stepDataOptions('StepAmplitude',15);

figure(2)
step(TT)
stepinfo(TT)
hold on;
%plot(impData1(:,1),impData1(:,2),'r-',impData1(:,1),impData1(:,3),'-b')

%figure(3)
%step(CF,opt)
%% Code

