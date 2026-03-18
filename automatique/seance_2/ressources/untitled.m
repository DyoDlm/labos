%% Labo 2 - Exercice 1

clear; close all; clc;

%% Charger les donnees
%%load('N:\PEDAGO\HEPIA\COURS\Olivier\Labo_stepResponse_moteur_DC.mat')


%% Verifier les variables chargees
whos

%% Tracer les donnees mesurees
figure;
plot(t, y,'b','LineWidth',1.2);
grid on;
xlabel('Temps [s]');
ylabel('Vitesse angulaire [rad/s]');
title('Reponse indicielle mesuree');

%% Estimation simple du systeme
K = 85;          % gain estime
tau = 0.01;      % constante de temps estimee
s = tf('s');
G = K/(1 + tau*s);

%% Reponse du modele
[y_mod, t_mod] = step(G, t);

%% Superposition mesure / modele
figure;
plot(t, y,'b','LineWidth',1.2); hold on;
plot(t_mod, y_mod,'r--','LineWidth',1.2);
grid on;
xlabel('Temps [s]');
ylabel('Vitesse angulaire [rad/s]');
title('Comparaison mesure / modele');
legend('Mesure','Modele');
