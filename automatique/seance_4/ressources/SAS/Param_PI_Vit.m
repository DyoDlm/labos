%% Données pour labo moteur DC vitesse
%  sur schema SIRAu_PI_vit.mdl
% clear all;
%% Général
TE=1e-3;
Temps_manip=5;

%% Capteur de vitesse:
Kmes = 10.7e-3;

%% Paramètres du système
Kmot = 4.53e3;
Kele = 20.8e-3;
T1 = 8e-3;
% G : 
%T2 = 1e-3;
% H :
T2 = 0.0015;

Ks = Kmot * Kele * Kmes;

%% Dimensionnement du régulateur:


Tn = 8e-3;
Tv = 0;
Ti = 2 * Ks * T2; %2,016ms
Kp = Tn/Ti;
Td = 0;

%% Filtre d'entrée:
Kmes_filtre = Kmes;
%tg=slrt;
