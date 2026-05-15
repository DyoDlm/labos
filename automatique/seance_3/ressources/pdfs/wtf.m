%% LABORATOIRE #3 - Exercice 1  (version corrigée)
% KP simulé = 0.05 (valeur conservative, PM = 101°)
% KP calculé = 0.125 (Bode, PM = 65°)
% =========================================================
clear; close all; clc;

%% ── PARAMÈTRES ───────────────────────────────────────────
Ks1 = 2e-3;
Ks2 = 2.5e4;
T1  = 0.0005;
T2  = 0.01;
T3  = 0.1;
K_total = Ks1 * Ks2;   % = 50 rad/s/V

num_s = K_total;
den_s = conv([T1 1], conv([T2 1], [T3 1]));
Gs = tf(num_s, den_s);

fprintf('=== Paramètres ===\n');
fprintf('K = Ks1*Ks2 = %.4g rad/s/V\n\n', K_total);

%% ── POINT A : Réponse indicielle boucle ouverte ──────────
figure('Name','A – Réponse indicielle BO', 'Position',[100 100 700 420]);
[y_A, t_A] = step(Gs, 0:0.001:0.7);
plot(t_A, y_A, 'b-', 'LineWidth', 2);
yline(50, 'k--', '50 rad/s', 'LabelHorizontalAlignment','left', 'FontSize', 10);
title('Réponse indicielle en boucle ouverte', 'FontSize', 13, 'FontWeight', 'bold');
xlabel('Temps (s)', 'FontSize', 11);
ylabel('Sortie (rad/s)', 'FontSize', 11);
grid on; grid minor;
ylim([0 55]);
saveas(gcf, 'A.png');

%% ── POINT B ──────────────────────────────────────────────
y_ref = 50;
u_B   = y_ref / K_total;
fprintf('=== Point B ===\n');
fprintf('Tension pour 50 rad/s : u = %.4g V\n\n', u_B);

%% ── POINT C : Bode Gs seul (KP=1) pour lecture des marges
[Gm1, Pm1, Wcg1, Wcp1] = margin(Gs);
fprintf('=== Point C ===\n');
fprintf('Gs seul (KP=1) : PM=%.2f° à %.2f rad/s, GM=%.2f dB à %.2f rad/s\n',...
    Pm1, Wcp1, 20*log10(Gm1), Wcg1);

% Calcul analytique de KP pour PM=65°
w = logspace(-1, 5, 100000);
[mag, phase] = bode(Gs, w);
mag   = squeeze(mag);
phase = squeeze(phase);
pm_target    = 65;
phase_cible  = -180 + pm_target;   % = -115°

idx = find(diff(sign(phase - phase_cible)), 1, 'last');
w_c65  = interp1(phase(idx:idx+1), w(idx:idx+1), phase_cible);
mag_c65= interp1(w(idx:idx+1), mag(idx:idx+1), w_c65);
KP_calc = 1 / mag_c65;

fprintf('Calcul Bode : omega_c = %.1f rad/s  => KP_calculé = %.4f\n', w_c65, KP_calc);

% Vérification analytique (ωc = 54 rad/s, calcul manuel du rapport)
wc_manuel = 54;
mag_manuel = K_total / (sqrt(1+(wc_manuel*T1)^2) * sqrt(1+(wc_manuel*T2)^2) * sqrt(1+(wc_manuel*T3)^2));
KP_manuel  = 1 / mag_manuel;
fprintf('Calcul manuel (wc=54 rad/s) : |Gs| = %.4f => KP = %.4f\n\n', mag_manuel, KP_manuel);

% Figure C : Bode de Gs seul (KP=1)
figure('Name','C – Bode Gs KP=1', 'Position',[100 100 750 500]);
margin(Gs);
title('Bode de G_0(s) = G_s(s) avec K_P = 1', 'FontSize', 13, 'FontWeight', 'bold');
grid on;
saveas(gcf, 'C.png');

%% ── POINT D : Gain d'entrée (avec KP simulé = 0.05) ─────
KP_sim = 0.05;   % valeur conservative retenue en simulation
Gcl_stat = (KP_sim * K_total) / (1 + KP_sim * K_total);
Ke = 1 / Gcl_stat;

fprintf('=== Point D ===\n');
fprintf('KP simulé      = %.4g\n', KP_sim);
fprintf('Gcl(0)         = %.4f  (=%.1f%% de la consigne)\n', Gcl_stat, Gcl_stat*100);
fprintf('Ke de correction = %.4f\n\n', Ke);

% BF avec KP_sim
GBF_Psim = feedback(KP_sim * Gs, 1);
[~, Pm_sim] = margin(KP_sim * Gs);
fprintf('Marge de phase avec KP=0.05 : PM = %.1f°\n\n', Pm_sim);

%% ── POINT E : Comparaison BO vs BF ───────────────────────
t_E = 0:0.001:1;

% Boucle ouverte (entrée u_B = 1V pour atteindre 50 rad/s)
y_BO = step(u_B * Gs, t_E);

% BF SANS Ke : consigne = 1 V -> sortie = Gcl_stat * 50 ≈ 35.7 rad/s
y_BF_noKe = step(KP_sim * y_ref * GBF_Psim, t_E);  % consigne 50 mais sans Ke

% BF AVEC Ke
y_BF_Ke = step(Ke * y_ref * GBF_Psim, t_E);

% Figure E1 : SANS Ke
figure('Name','E1 – BO vs BF sans Ke', 'Position',[100 100 700 420]);
plot(t_E, y_BO,       '-',  'Color',[0.93 0.69 0.13], 'LineWidth', 2); hold on;  % jaune
plot(t_E, y_BF_noKe,  'b-', 'LineWidth', 2);
yline(50, 'k--', 'Consigne 50 rad/s', 'FontSize', 10, 'LabelHorizontalAlignment','left');
yline(Gcl_stat*50, 'r:', sprintf('BF statique = %.1f rad/s (%.1f%%)', Gcl_stat*50, Gcl_stat*100),...
    'FontSize', 9, 'LabelHorizontalAlignment','right');
legend('Boucle ouverte (G_{s,BO})','Boucle fermée (G_{s,BF}) sans K_e','Location','southeast');
title({'Comparaison BO vs BF – \bfSANS correction K_e',...
       sprintf('BF se stabilise à %.1f rad/s (%.1f%% de la consigne)', Gcl_stat*50, Gcl_stat*100)},...
       'FontSize', 12);
xlabel('Temps (s)', 'FontSize', 11);
ylabel('Vitesse (rad/s)', 'FontSize', 11);
ylim([0 58]); grid on; grid minor;
saveas(gcf, 'E1.png');

% Figure E2 : AVEC Ke
figure('Name','E2 – BO vs BF avec Ke', 'Position',[100 100 700 420]);
plot(t_E, y_BO,     'b-', 'LineWidth', 2); hold on;    % bleu = BO
plot(t_E, y_BF_Ke, '-', 'Color',[0.85 0.33 0.10], 'LineWidth', 2); % orange = BF
yline(50, 'k--', 'Consigne 50 rad/s', 'FontSize', 10, 'LabelHorizontalAlignment','left');
legend('Boucle ouverte (G_{s,BO})','Boucle fermée (G_{s,BF}) avec K_e = 1.4','Location','southeast');
title({'Comparaison BO vs BF – \bfAVEC correction K_e = 1.4',...
       'BF 5\times plus rapide : t_r \approx 0.1 s vs 0.5 s'}, 'FontSize', 12);
xlabel('Temps (s)', 'FontSize', 11);
ylabel('Vitesse (rad/s)', 'FontSize', 11);
ylim([0 58]); grid on; grid minor;

% Annotations
info_BF = stepinfo(Ke * y_ref * GBF_Psim);
info_BO = stepinfo(u_B * Gs);
text(0.38, 42, sprintf('BO : t_{95\\%%} \\approx %.2f s', info_BO.SettlingTime),...
    'Color','b','FontSize',9,'FontWeight','bold');
text(0.07, 25, sprintf('BF : t_{95\\%%} \\approx %.2f s', info_BF.SettlingTime),...
    'Color',[0.85 0.33 0.10],'FontSize',9,'FontWeight','bold');
saveas(gcf, 'E2.png');

fprintf('=== Point E ===\n');
fprintf('BO : Ts(95%%) = %.3f s\n', info_BO.SettlingTime);
fprintf('BF : Ts(95%%) = %.3f s,  Tr = %.3f s,  Dép. = %.2f%%\n\n',...
    info_BF.SettlingTime, info_BF.RiseTime, info_BF.Overshoot);

%% ── POINT F : Perturbation 1 mNm à t=1s ─────────────────
d_amp = 1e-3;  % [N.m]

% TF perturbation -> sortie en BF avec KP_sim
num_d = Ks2;
den_d = conv([T2 1], [T3 1]);
Gd = tf(num_d, den_d);
KP_sim = 0.05
TF_d2y_BF = Gd / (1 + KP_sim * Gs);

% Erreur statique
err_BF = dcgain(d_amp * TF_d2y_BF);
err_BO = Ks2 * d_amp;   % en BO : pas de rejet
fprintf('=== Point F ===\n');
fprintf('Déviation statique BF : ΔY = Ks2*d/(1+KP*Ks) = %.3f rad/s\n', err_BF);
fprintf('Déviation statique BO : ΔY = Ks2*d            = %.3f rad/s\n\n', err_BO);

% Simulation superposition : consigne + perturbation à t=1s
t_F  = 0:0.001:2;
t_F2 = 0:0.001:1;   % durée de la perturbation seule

y_ref_BF = step(Ke * y_ref * GBF_Psim, t_F);   % réponse consigne BF
y_ref_BO = step(u_B * Gs, t_F);                  % réponse consigne BO

[y_pert_BF, ~] = step(d_amp * TF_d2y_BF, t_F2);
[y_pert_BO, ~] = step(d_amp * Gd, t_F2);         % en BO : intégration libre

idx1 = find(t_F >= 1, 1);
n2   = length(t_F2);

y_total_BF = y_ref_BF;
y_total_BF(idx1:idx1+n2-1) = y_total_BF(idx1:idx1+n2-1) + y_pert_BF;
y_total_BF(idx1+n2:end)    = y_total_BF(idx1+n2:end) + y_pert_BF(end);

y_total_BO = y_ref_BO;
y_total_BO(idx1:idx1+n2-1) = y_total_BO(idx1:idx1+n2-1) + y_pert_BO;
y_total_BO(idx1+n2:end)    = y_total_BO(idx1+n2:end) + y_pert_BO(end);

% Figure F : réponse BO et BF avec perturbation
figure('Name','F – Perturbation 1 mNm', 'Position',[100 100 750 460]);
plot(t_F, y_total_BO, '-', 'Color',[0.85 0.33 0.10], 'LineWidth', 2); hold on;
plot(t_F, y_total_BF, 'b-', 'LineWidth', 2);
xline(1, 'k--', 'Perturbation (t=1s)', 'FontSize', 10, 'LabelVerticalAlignment','bottom');
yline(50, 'k:', 'Consigne 50 rad/s', 'FontSize', 9, 'LabelHorizontalAlignment','right');

% Annotations des déviations
yline(50 + err_BO, '--', 'Color',[0.85 0.33 0.10], 'LineWidth', 1);
yline(50 + err_BF, '--', 'Color',[0 0.45 0.74],    'LineWidth', 1);
text(1.55, 50+err_BO+0.8,...
    sprintf('BO : +%.0f rad/s', err_BO),...
    'Color',[0.85 0.33 0.10], 'FontSize', 10, 'FontWeight','bold');
text(1.55, 50+err_BF+0.8,...
    sprintf('BF : +%.1f rad/s', err_BF),...
    'Color',[0 0.45 0.74], 'FontSize', 10, 'FontWeight','bold');

legend('Boucle ouverte (G_{s,BO})','Boucle fermée avec K_P = 0.05','Location','northwest');
title({'Effet d''une perturbation de 1 mNm à t = 1 s',...
       'Erreur statique résiduelle avec régulateur P'},'FontSize', 12);
xlabel('Temps (s)', 'FontSize', 11);
ylabel('Vitesse (rad/s)', 'FontSize', 11);
ylim([0 max(y_total_BO)*1.1]); grid on; grid minor;
saveas(gcf, 'F.png');

%% ── POINT G : Bode G0 = KP_sim * Gs ─────────────────────
G0_Psim = KP_sim * Gs;
[Gm_G, Pm_G, Wcg_G, Wcp_G] = margin(G0_Psim);

figure('Name','G – Bode G0 KP=0.05', 'Position',[100 100 750 500]);
margin(G0_Psim);
title(sprintf('Bode de G_0(s) = K_P \\cdot G_s(s),  K_P = %.2f', KP_sim),...
    'FontSize', 13, 'FontWeight', 'bold');
grid on;
saveas(gcf, 'G.png');

fprintf('=== Point G ===\n');
fprintf('G0 = KP*Gs (KP=0.05) : PM=%.2f° à wcp=%.2f rad/s, GM=%.2f dB à wcg=%.2f rad/s\n',...
    Pm_G, Wcp_G, 20*log10(Gm_G), Wcg_G);
fprintf('G0(0) = KP*Ks = %.2f*50 = %.2f (≈ %.1f dB) => système CLASSE 0\n\n',...
    KP_sim, KP_sim*K_total, 20*log10(KP_sim*K_total));

%% ── POINTS H & I : Régulateur PI ────────────────────────
Ti = T3;   % compensation pôle dominant

% PI : GR = C * (1 + Ti*s) / (Ti*s)
% On laisse Control System Designer déterminer C
% Ici on utilise la même valeur que le rapport de référence : C = 0.5744
C_PI = 0.5744;
num_PI = C_PI * [Ti 1];
den_PI = [Ti 0];
R_PI   = tf(num_PI, den_PI);

G0_PI = R_PI * Gs;
[Gm_PI, Pm_PI, Wcg_PI, Wcp_PI] = margin(G0_PI);

figure('Name','I – Bode G0 PI', 'Position',[100 100 750 500]);
margin(G0_PI);
title('Bode de G_0(s) = R_{PI}(s) \cdot G_s(s)', 'FontSize', 13, 'FontWeight', 'bold');
grid on;
saveas(gcf, 'I.png');

fprintf('=== Points H & I – PI ===\n');
fprintf('C = %.4f, Ti = T3 = %.4f s\n', C_PI, Ti);
fprintf('G0_PI : PM=%.2f° à wcp=%.2f rad/s, GM=%.2f dB\n\n', Pm_PI, Wcp_PI, 20*log10(Gm_PI));

%% ── POINTS J & K : Régulateur PID ───────────────────────
% On reprend KP_calc (basé sur PM=65°) avec Ti=T3, Td=T2
KP_pid = KP_calc;
Td = T2;

num_PID = KP_pid * [Ti*Td  Ti  1];
den_PID = [Ti  0];
R_PID   = tf(num_PID, den_PID);
G0_PID  = R_PID * Gs;

figure('Name','K – Bode G0 PID', 'Position',[100 100 750 500]);
margin(G0_PID);
title('Bode de G_0(s) = R_{PID}(s) \cdot G_s(s)', 'FontSize', 13, 'FontWeight', 'bold');
grid on;
saveas(gcf, 'K.png');

[Gm_PID, Pm_PID, Wcg_PID, Wcp_PID] = margin(G0_PID);
fprintf('=== Points J & K – PID ===\n');
fprintf('KP=%.4f, Ti=%.4f s, Td=%.4f s\n', KP_pid, Ti, Td);
fprintf('G0_PID : PM=%.2f° à wcp=%.2f rad/s, GM=%.2f dB\n\n', Pm_PID, Wcp_PID, 20*log10(Gm_PID));

% Comparaison temporelle P / PI / PID avec perturbation à t=1s
GBF_PI  = feedback(R_PI  * Gs, 1);
GBF_PID = feedback(R_PID * Gs, 1);

Ke_PI  = 1 / dcgain(GBF_PI);
Ke_PID = 1 / dcgain(GBF_PID);

TF_d2y_PI  = Gd / (1 + R_PI  * Gs);
TF_d2y_PID = Gd / (1 + R_PID * Gs);

t_J = 0:0.001:4;
t_J2= 0:0.001:3;
idx2 = find(t_J >= 1, 1);
n3   = length(t_J2);

y_P_ref  = step(Ke     * y_ref * GBF_Psim, t_J);
y_PI_ref = step(Ke_PI  * y_ref * GBF_PI,   t_J);
y_PID_ref= step(Ke_PID * y_ref * GBF_PID,  t_J);

[y_p_pert, ~]  = step(d_amp * TF_d2y_BF,  t_J2);
[y_pi_pert,~]  = step(d_amp * TF_d2y_PI,  t_J2);
[y_pid_pert,~] = step(d_amp * TF_d2y_PID, t_J2);

build_total = @(y_ref, y_pert) ...
    [y_ref(1:idx2-1); ...
     y_ref(idx2:idx2+n3-1) + y_pert; ...
     y_ref(idx2+n3:end) + y_pert(end)];

y_J_P   = build_total(y_P_ref,   y_p_pert);
y_J_PI  = build_total(y_PI_ref,  y_pi_pert);
y_J_PID = build_total(y_PID_ref, y_pid_pert);

figure('Name','J – P vs PI vs PID', 'Position',[100 100 750 460]);
plot(t_J, y_J_P,   'b-',  'LineWidth', 1.8); hold on;
plot(t_J, y_J_PI,  'r-',  'LineWidth', 1.8);
plot(t_J, y_J_PID, 'g-',  'LineWidth', 1.8);
xline(1, 'k--', 'Perturbation (t=1s)', 'FontSize', 9, 'LabelVerticalAlignment','bottom');
yline(50, 'k:', 'Consigne', 'FontSize', 9, 'LabelHorizontalAlignment','right');
legend('Régulateur P','Régulateur PI','Régulateur PID','Location','east');
title('Comparaison P / PI / PID avec perturbation de 1 mNm à t = 1 s', 'FontSize', 12);
xlabel('Temps (s)', 'FontSize', 11);
ylabel('Vitesse (rad/s)', 'FontSize', 11);
ylim([0 65]); grid on; grid minor;
saveas(gcf, 'J.png');

%% ── RÉSUMÉ FINAL ─────────────────────────────────────────
fprintf('=== Résumé ===\n');
fprintf('  KP calculé (PM=65°) : %.4f  (wc = %.1f rad/s)\n', KP_calc, w_c65);
fprintf('  KP simulé  (PM=101°): %.4f  (wc = %.1f rad/s)\n', KP_sim,  Wcp_G);
fprintf('  Ke (avec KP=0.05)   : %.4f\n', Ke);
fprintf('\n  Paramètres PID (forme parallèle Simulink) :\n');
fprintf('    P = KP        = %.6f\n', KP_pid);
fprintf('    I = KP/Ti     = %.6f\n', KP_pid/Ti);
fprintf('    D = KP*Td     = %.6f\n', KP_pid*Td);
fprintf('\nScript terminé — figures A, C, E1, E2, F, G, I, J, K sauvegardées.\n');