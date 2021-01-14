syms a;
%% Peak overshoot def
eq = 100*exp((-a*pi)/sqrt(1-a^2)) == 25;
ep = eval(solve(eq));
zeta = ep(1,1)
%% peak time def
syms a;
syms b;
eq2 = pi/(b*sqrt(1-zeta^2)) == 1.363;
wn = eval(solve(eq2))

%% rise time def
syms c
%eps = 1.504;
%wn = 2.6424;
eq3 = (pi-atan(sqrt(1 - zeta^2)/zeta))/(wn*sqrt(1-zeta^2))==c;
eval(solve(eq3))

%% settling time
syms a,b;
eq4 = 4/(wn*zeta) == b;
eval(solve(eq4))


%% Closed loop poles
zeta = 0.0709;
wn = 0.4511;
Sd1 = (-zeta*wn + i*wn*sqrt(1-zeta^2))
Sd2 = (-zeta*wn - i*wn*sqrt(1-zeta^2))

%% Calculating Phase 
% Current phase phi = Gp(Sd)

phi = phase(evalfr(Gp, sd))

%% system

zeta =  0.2660 ;%- 3.0727i;
wn =  1.7400;

sys = tf([120],[1 2*zeta*wn wn^2])
step(sys)
[z,gain] = zero(sys)
stepinfo(sys)


