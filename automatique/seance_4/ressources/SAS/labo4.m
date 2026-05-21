%% =========================================================
%  LABO 4 - Création automatique du modèle Simulink
%  Lance ce script -> le modèle Simulink s'ouvre tout seul
%  =========================================================
clear; clc; close all;

%% --- 1. PARAMÈTRES ---
K_mot   = 4.53e3;
tau_mot = 8e-3;
K_ele   = 20.8e-3;
tau_ele = 1e-3;
K_mes   = 10.7e-3;

% Calcul PI automatique
K_total  = K_mot * K_ele * K_mes;
D_max    = 5;
zeta     = sqrt(log(D_max/100)^2 / (pi^2 + log(D_max/100)^2));
PM_cible = atand(2*zeta / sqrt(sqrt(1+4*zeta^4) - 2*zeta^2));
Ti       = tau_mot;
wc       = tand(90 - PM_cible) / tau_ele;
Kp       = wc * sqrt(1+(wc*tau_ele)^2) * Ti / K_total;


fprintf('PI calculé : Kp = %.3f   Ti = %.1f ms\n', Kp, Ti*1e3);

w_ref_rads  = 10;
w_ref_volts = w_ref_rads * K_mes;

%% --- 2. CRÉATION DU MODÈLE SIMULINK ---
mdl = 'Labo4_DEF';
if bdIsLoaded(mdl), close_system(mdl, 0); end
new_system(mdl);
open_system(mdl);

% Echelon de consigne (en Volts)
add_block('simulink/Sources/Step', [mdl '/Consigne'], ...
    'Time','0', ...
    'Position',[30 170 60 200]);

% Somme (erreur = consigne - mesure)
add_block('simulink/Math Operations/Sum', [mdl '/Somme'], ...
    'Inputs','+-', 'Position',[120 168 150 202]);

% Régulateur PI
num_PI = Kp * [Ti, 1];
den_PI = [Ti, 0];
add_block('simulink/Continuous/Transfer Fcn', [mdl '/PI'], ...
    'Numerator', mat2str(num_PI), 'Denominator', mat2str(den_PI), ...
    'Position',[210 163 310 207]);

% G_ele
add_block('simulink/Continuous/Transfer Fcn', [mdl '/G_ele'], ...
    'Numerator', mat2str(K_ele), 'Denominator', mat2str([tau_ele, 1]), ...
    'Position',[370 163 470 207]);

% G_mot
add_block('simulink/Continuous/Transfer Fcn', [mdl '/G_mot'], ...
    'Numerator', mat2str(K_mot), 'Denominator', mat2str([tau_mot, 1]), ...
    'Position',[530 163 630 207]);

% G_mes
add_block('simulink/Math Operations/Gain', [mdl '/G_mes'], ...
    'Gain', num2str(K_mes), 'Position',[530 290 630 330]);

% Scopes
add_block('simulink/Sinks/Scope', [mdl '/Scope_omega'], ...
    'Position',[700 163 730 197]);
add_block('simulink/Sinks/Scope', [mdl '/Scope_ucm'], ...
    'Position',[370 80 400 110]);

% To Workspace
add_block('simulink/Sinks/To Workspace', [mdl '/omega_ws'], ...
    'VariableName','omega_out', 'MaxDataPoints','inf', ...
    'SaveFormat','Array', 'Position',[700 220 760 250]);
add_block('simulink/Sinks/To Workspace', [mdl '/ucm_ws'], ...
    'VariableName','ucm_out', 'MaxDataPoints','inf', ...
    'SaveFormat','Array', 'Position',[370 120 430 150]);

% Connexions
add_line(mdl, 'Consigne/1', 'Somme/1');
add_line(mdl, 'Somme/1',    'PI/1');
add_line(mdl, 'PI/1',       'G_ele/1');
add_line(mdl, 'PI/1',       'Scope_ucm/1');
add_line(mdl, 'PI/1',       'ucm_ws/1');
add_line(mdl, 'G_ele/1',    'G_mot/1');
add_line(mdl, 'G_mot/1',    'Scope_omega/1');
add_line(mdl, 'G_mot/1',    'omega_ws/1');
add_line(mdl, 'G_mot/1',    'G_mes/1');
add_line(mdl, 'G_mes/1',    'Somme/2');

%% --- 3. RÉGLAGES SIMULATION ---
set_param(mdl, 'StopTime','0.15', 'Solver','ode45', 'MaxStep','1e-5');

%% --- 4. LANCER ---
fprintf('Simulation en cours...\n');

% Changer le format des blocs To Workspace
set_param([mdl '/omega_ws'], 'SaveFormat', 'Structure With Time');
set_param([mdl '/ucm_ws'],   'SaveFormat', 'Structure With Time');

simOut = sim(mdl);
fprintf('Simulation terminée.\n\n');

%% --- 5. RÉSULTATS ---
t_sim = simOut.get('omega_out').time;
y_sim = simOut.get('omega_out').signals.values;
u_sim = simOut.get('ucm_out').signals.values;

y_fin  = y_sim(end);
y_max  = max(y_sim);
depass = (y_max - y_fin) / y_fin * 100;

idx = find(abs(y_sim - y_fin) > 0.05*y_fin, 1, 'last');
if isempty(idx), tr5 = 0; else, tr5 = t_sim(idx); end
idx2 = find(abs(y_sim - y_fin) > 0.02*y_fin, 1, 'last');
if isempty(idx2), tr2 = 0; else, tr2 = t_sim(idx2); end

fprintf('Vitesse finale   : %.3f rad/s\n', y_fin);
fprintf('Dépassement      : %.2f%%\n', depass);
fprintf('Tr 5%%            : %.2f ms\n', tr5*1e3);
fprintf('Tr 2%%            : %.2f ms\n', tr2*1e3);
fprintf('u_cm max         : %.3f V\n', max(abs(u_sim)));

% Figure 1 : omega
figure('Name','Tâche C - Réponse indicielle');
plot(t_sim*1e3, y_sim, 'b', 'LineWidth', 2); hold on;
yline(w_ref_rads, 'r--', 'Consigne 10 rad/s');
yline(y_fin*1.05, 'k:', '+5%');
yline(y_fin*0.95, 'k:', '-5%');
xlabel('Temps [ms]'); ylabel('\omega [rad/s]');
title(sprintf('Réponse indicielle — D=%.1f%%  Tr5%%=%.1f ms', depass, tr5*1e3));
legend('Sortie \omega(t)', 'Consigne'); grid on;

% Figure 2 : ucm
figure('Name','Tâche D - Tension ucm');
plot(t_sim*1e3, u_sim, 'r', 'LineWidth', 2); hold on;
yline( 10, 'k--', '+10V limite');
yline(-10, 'k--', '-10V limite');
xlabel('Temps [ms]'); ylabel('u_{cm} [V]');
title(sprintf('Tension u_{cm} — max = %.3f V', max(abs(u_sim))));
legend('u_{cm}(t)', 'Limite ±10V'); grid on;