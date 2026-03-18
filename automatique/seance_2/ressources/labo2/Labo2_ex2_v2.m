load('Z:\MT\systeme_asservis\SIRAu_stepResponse.mat')

t = time;

%% Affichage propre des fonctions de transfert
clear; close all; clc;

s = tf('s');

%% G moteur
K_mot = 4.53e3;
tau_mot = 8e-3;
G_mot = K_mot / (1 + tau_mot*s);

%% G element
K_ele = 20.8e-3;
tau_ele = 1.5e-4;
G_ele = K_ele / (1 + tau_ele*s);

%% G mesure
K_mes = 10.7e-3;
G_mes = tf(K_mes);

%% G systeme complet
G_s = G_mot * G_ele * G_mes;

disp('===== G_s =====')
G_s

%% D) Regulateur PI
k_R = 3306;
T_n = 8e-3;

G_R = k_R * (1 + s*T_n) / s;

disp('===== G_R =====')
G_R

%% Boucle ouverte
G_0 = G_R * G_s;

disp('===== G_0 avant simplification =====')
G_0

%% Simplification
G_0_simpl = minreal(G_0);

disp('===== G_0 apres simplification =====')
G_0_simpl

%% Boucle fermee
G_cf = feedback(G_0_simpl,1);

disp('===== G_cf =====')
G_cf

%% Recuperer numerateur et denominateur
[num,den] = tfdata(G_cf,'v');

disp('===== Numerateur de G_cf =====')
num

disp('===== Denominateur de G_cf =====')
den

%% Affichage de la forme Kcf / (a s^2 + b s + c)
K_cf = num(end);
a = den(1);
b = den(2);
c = den(3);

fprintf('\nG_cf(s) = %.6f / ( %.6e s^2 + %.6e s + %.6e )\n',K_cf,a,b,c);

%% Verification graphique
figure;
step(G_cf);
grid on;
title('Reponse indicielle de G_{cf}')

%% Parametres temporels
info = stepinfo(G_cf,'SettlingTimeThreshold',0.05,'RiseTimeLimits',[0 1]);

Overshoot = info.Overshoot
RiseTime = info.RiseTime
SettlingTime = info.SettlingTime

%% Bode et Nyquist de la boucle ouverte --> point E)
figure;
margin(G_0_simpl);
grid on;
title('Diagramme de Bode de G_0')

figure;
nyquist(G_0_simpl);
grid on;

title('Diagramme de Nyquist de G_0')


%% EVANS --> Point F
figure;
rlocus(G_0_simpl); % trouver les yeros
grid on;

figure;
step(G_cf);
grid on;