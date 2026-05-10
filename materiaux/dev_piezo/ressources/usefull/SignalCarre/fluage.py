import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================
# FICHIER
# ============================================================
filename = "signal_carre.csv"

# ============================================================
# LECTURE CSV
# ============================================================
df = pd.read_csv(filename, skiprows=2)

# ============================================================
# DONNEES
# ============================================================
t = df.iloc[:, 0].values
canal_A = df.iloc[:, 1].values
canal_B = df.iloc[:, 2].values / 1000  # mV -> V

# ============================================================
# MODELES
# ============================================================
def rise_model(t, A, tau, B):
    return A * (1 - np.exp(-t / tau)) + B

def decay_model(t, A, tau, B):
    return A * np.exp(-t / tau) + B

# ============================================================
# FENETRES DE TEMPS POUR MONTEE ET DESCENTE
# ============================================================
# Fenêtre pour la montée (0.88 à 0.90 s)
rise_start_time = 0.855
rise_end_time = 1

# Fenêtre pour la descente (0.38 à 0.40 s)
decay_start_time = 0.355
decay_end_time = 0.8

# Trouver les indices correspondants dans t
rise_start_idx = np.argmin(np.abs(t - rise_start_time))
rise_end_idx = np.argmin(np.abs(t - rise_end_time))

decay_start_idx = np.argmin(np.abs(t - decay_start_time))
decay_end_idx = np.argmin(np.abs(t - decay_end_time))

# ============================================================
# AJUSTEMENT POUR LA MONTEE
# ============================================================
t_rise = t[rise_start_idx:rise_end_idx]
y_rise = canal_B[rise_start_idx:rise_end_idx]

# Remise à zéro du temps pour la montée
t_rise = t_rise - t_rise[0]

# Paramètres initiaux pour la montée
A0_rise = y_rise[-1] - y_rise[0]
B0_rise = y_rise[0]
tau0_rise = (t_rise[-1] - t_rise[0]) / 10
p0_rise = [A0_rise, tau0_rise, B0_rise]

# Bornes pour la montée
bounds_rise = ([-np.inf, 1e-7, -np.inf], [np.inf, 1.0, np.inf])

# Ajustement pour la montée
params_rise, cov_rise = curve_fit(
    rise_model,
    t_rise,
    y_rise,
    p0=p0_rise,
    bounds=bounds_rise,
    maxfev=20000
)
A_rise, tau_rise, B_rise = params_rise
dA_rise, dtau_rise, dB_rise = np.sqrt(np.diag(cov_rise))

# Courbe fit pour la montée
t_smooth_rise = np.linspace(np.min(t_rise), np.max(t_rise), 2000)
y_smooth_rise = rise_model(t_smooth_rise, A_rise, tau_rise, B_rise)

# ============================================================
# AJUSTEMENT POUR LA DESCENTE
# ============================================================
t_decay = t[decay_start_idx:decay_end_idx]
y_decay = canal_B[decay_start_idx:decay_end_idx]

# Remise à zéro du temps pour la descente
t_decay = t_decay - t_decay[0]

# Paramètres initiaux pour la descente
A0_decay = y_decay[0] - y_decay[-1]
B0_decay = y_decay[-1]
tau0_decay = (t_decay[-1] - t_decay[0]) / 10
p0_decay = [A0_decay, tau0_decay, B0_decay]

# Bornes pour la descente
bounds_decay = ([-np.inf, 1e-7, -np.inf], [np.inf, 1.0, np.inf])

# Ajustement pour la descente
params_decay, cov_decay = curve_fit(
    decay_model,
    t_decay,
    y_decay,
    p0=p0_decay,
    bounds=bounds_decay,
    maxfev=20000
)
A_decay, tau_decay, B_decay = params_decay
dA_decay, dtau_decay, dB_decay = np.sqrt(np.diag(cov_decay))

# Courbe fit pour la descente
t_smooth_decay = np.linspace(np.min(t_decay), np.max(t_decay), 2000)
y_smooth_decay = decay_model(t_smooth_decay, A_decay, tau_decay, B_decay)

# ============================================================
# AFFICHAGE
# ============================================================
plt.figure(figsize=(12, 8))

# Tracé des mesures
plt.plot(t, canal_B, label="Mesures", linewidth=1, color="gray")

# Tracé du fit pour la montée
plt.plot(
    t_smooth_rise + t[rise_start_idx],
    y_smooth_rise,
    linewidth=3,
    label=f"Fit montée\nτ = {tau_rise:.3e} ± {dtau_rise:.1e} s"
)

# Tracé du fit pour la descente
plt.plot(
    t_smooth_decay + t[decay_start_idx],
    y_smooth_decay,
    linewidth=3,
    label=f"Fit descente\nτ = {tau_decay:.3e} ± {dtau_decay:.1e} s"
)

plt.xlabel("Temps (s)")
plt.ylabel("Canal B (V)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("fluage_fit_montée_descente.png", dpi=300)
plt.close()

# ============================================================
# RESULTATS
# ============================================================
print("\n================ RESULTATS MONTEE ================\n")
print(f"A    = {A_rise:.6e} ± {dA_rise:.2e}")
print(f"tau  = {tau_rise:.6e} ± {dtau_rise:.2e} s")
print(f"B    = {B_rise:.6e} ± {dB_rise:.2e}")

print("\n================ RESULTATS DESCENTE ================\n")
print(f"A    = {A_decay:.6e} ± {dA_decay:.2e}")
print(f"tau  = {tau_decay:.6e} ± {dtau_decay:.2e} s")
print(f"B    = {B_decay:.6e} ± {dB_decay:.2e}")

print("\nFigures sauvegardées : fluage_fit_montée_descente.png")
