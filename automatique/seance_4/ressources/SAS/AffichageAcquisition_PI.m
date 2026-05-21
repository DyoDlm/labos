%% Affichage des courbes:
close all;
tg = slrt;

plot(tg.TimeLog,tg.OutputLog); hold on;
legend('Mesure Position /rad','Mesure courant /A','Signal commande /V','Vitesse de consigne /rad/s', 'Vitesse mesurée /rad/s');
xlabel('Temps [s]');
grid on;
plotbrowser('on');
