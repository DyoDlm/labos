load('Z:\MT\systeme_asservis\SIRAu_stepResponse.mat')

t = time;

%% Affichage propre des fonctions de transfert
clear; close all; clc;

s = tf('s');

%% G moteur
K_mot = 4.53e3;
tau_mot = 8e-3;
G_mot = K_mot / (1 + tau_mot*s);

disp(' ')
disp('===== G_mot forme classique =====')
G_mot

G_mot_zpk_evans = zpk(G_mot);
disp('===== G_mot forme Evans (zpk) =====')
G_mot_zpk_evans

G_mot_zpk_bode = zpk(G_mot);
G_mot_zpk_bode.DisplayFormat = 'frequency';
disp('===== G_mot forme Bode =====')
G_mot_zpk_bode

%% G element
K_ele = 20.8e-3;
tau_ele = 1.5e-4;
G_ele = K_ele / (1 + tau_ele*s);

disp(' ')
disp('===== G_ele forme classique =====')
G_ele

G_ele_zpk_evans = zpk(G_ele);
disp('===== G_ele forme Evans (zpk) =====')
G_ele_zpk_evans

G_ele_zpk_bode = zpk(G_ele);
G_ele_zpk_bode.DisplayFormat = 'frequency';
disp('===== G_ele forme Bode =====')
G_ele_zpk_bode

%% G mesure
K_mes = 10.7e-3;
G_mes = tf(K_mes);

disp(' ')
disp('===== G_mes forme classique =====')
G_mes

G_mes_zpk_evans = zpk(G_mes);
disp('===== G_mes forme Evans (zpk) =====')
G_mes_zpk_evans

G_mes_zpk_bode = zpk(G_mes);
G_mes_zpk_bode.DisplayFormat = 'frequency';
disp('===== G_mes forme Bode =====')
G_mes_zpk_bode

%% G final
G_final = G_mot * G_ele * G_mes;

disp(' ')
disp('===== G_final forme classique =====')
G_final

G_final_zpk_evans = zpk(G_final);
disp('===== G_final forme Evans (zpk) =====')
G_final_zpk_evans

G_final_zpk_bode = zpk(G_final);
G_final_zpk_bode.DisplayFormat = 'frequency';
disp('===== G_final forme Bode =====')
G_final_zpk_bode

%% le systeme donc 
G_s = G_final;

%%  Regulateur PI (Gr)
k_R = 3306;
T_n = 8e-3;
G_R = k_R * (1 + s*T_n) / s;
G_0 = G_R * G_s;
G_cf = feedback(G_0, 1);


%%  G ouvert

%G_o = %% Boucle ouverte
G_0 = G_R * G_s;

disp('===== G_0 avant simplification =====')
%G_0

%% Simplification
G_0_simpl = minreal(G_0);

disp('===== G_0 apres simplification =====')
%G_0_simpl

%% Boucle fermee
G_cf = feedback(G_0_simpl,1);

disp('===== G_cf =====')
%G_cf

%%  G fermé

%G_cf = ...;



%% Diagramme de Bode et Nyguist 
figure;
bode(G_0);
grid on;
margin(G_0); % Affiche la marge de phase et de gain

figure;
nyquist(G_0);
grid on;


%% PLOT

[y_mod, t_mod] = step(G_final, t);

% Reponse du modele
%[y_mod, t_mod] = step(G_mot*G_ele*exp(-0.1*s), t);

% Reponse du modele
%[y_mod, t_mod] = step(G_mot*G_ele*exp(-0.1*s) *G_mes, t);

figure;
%plot(t_ex1, y_ex1,'b','LineWidth',1.2); hold on;
plot(t_mod, y_mod,'r--','LineWidth',1.2);
grid on;
xlabel('Temps [s]');
ylabel('Vitesse angulaire [rad/s]');
title('Comparaison mesure / modele');
legend('Ex1','Gele*Gmot');

%%% 