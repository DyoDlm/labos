# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ===============================
# Lecture CSV robuste
# ===============================
def read_csv(filename):
    print("Lecture :", filename)
    df = pd.read_csv(filename)
    t = pd.to_numeric(df.iloc[:, 0], errors="coerce")
    y = pd.to_numeric(df.iloc[:, 1], errors="coerce")

    # Supprime lignes NaN
    mask = np.isfinite(t) & np.isfinite(y)
    t, y = t[mask].values, y[mask].values

    # Tri croissant
    idx = np.argsort(t)
    t, y = t[idx], y[idx]

    return t, y

# ===============================
# Modèles physiques
# ===============================
def model_under(t, A, gamma, omega, phi):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

def model_over(t, A, a, B, b):
    return A * np.exp(-a * t) + B * np.exp(-b * t)

def model_critical(t, A, B, lam):
    return (A + B * t) * np.exp(-lam * t)

# ===============================
# Estimation initiale pour régime faible
# ===============================
    # FFT pour omega
def guess_params_under(t, y):
    # Soustraire la moyenne pour éviter offset
    y_detrended = y - np.mean(y)

    # FFT pour omega
    fft = np.fft.fft(y_detrended)
    freqs = np.fft.fftfreq(len(t), d=(t[1]-t[0]))
    idx = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
    omega0 = 2 * np.pi * abs(freqs[idx])

    # Estimation de l'amplitude sur les pics locaux
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(y_detrended)
    if len(peaks) > 0:
        A0 = np.max(np.abs(y_detrended[peaks]))
    else:
        A0 = (np.max(y_detrended) - np.min(y_detrended)) / 2

    gamma0 = 0.05  # faible amortissement initial
    phi0 = 0.0
    return [A0, gamma0, omega0, phi0]

# ===============================
# Ajustements robustes
# ===============================
def fit_under(t, y):
    p0 = guess_params_under(t, y)
    bounds = ([0, 0, 0, -2*np.pi], [np.inf, 1.0, np.inf, 2*np.pi])
    return curve_fit(model_under, t, y, p0=p0, bounds=bounds, maxfev=60000)

def fit_over(t, y):
    # Min/max sur les 20% initial et final pour éviter les outliers
    n = max(1, len(y)//5)
    p0 = [np.mean(y[:n]), 0.5, np.mean(y[-n:]), 2.0]
    bounds = ([-np.inf, 0, -np.inf, 0], [np.inf, 5.0, np.inf, 5.0])
    return curve_fit(model_over, t, y, p0=p0, bounds=bounds, maxfev=60000)

def fit_critical(t, y):
    A0 = y[0]
    B0 = (y[1]-y[0])/(t[1]-t[0])
    lam0 = 1.0/(t[-1]-t[0])

    # Ajustement pour rester dans les bornes
    lam0 = min(lam0, 5.0)  # borne supérieure
    B0 = np.clip(B0, -np.inf, np.inf)
    A0 = np.clip(A0, -np.inf, np.inf)

    p0 = [A0, B0, lam0]

    # bornes adaptatives
    bounds = ([-np.inf, -np.inf, 0], [np.inf, np.inf, max(10, lam0*5)])

    return curve_fit(model_critical, t, y, p0=p0, bounds=bounds, maxfev=60000)

# ===============================
# Tracé individuel
# ===============================
def plot_fit(title, t, y, t_fit, y_fit):
    plt.figure(figsize=(9, 4))
    plt.scatter(t, y, s=15, marker="+", label="Données")
    plt.plot(t_fit, y_fit, "r-", label="Fit")
    plt.xlabel("Temps [s]")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# ===============================
# Fonction centrale
# ===============================
def smart_plot(filepath, exp_name, forced_model):
    t, y = read_csv(filepath)
    t_fit = np.linspace(t.min(), t.max(), 2000)

    if forced_model == "under":
        params, cov = fit_under(t, y)
        y_fit = model_under(t_fit, *params)
        label = "Amortissement faible"
    elif forced_model == "critical":
        params, cov = fit_critical(t, y)
        y_fit = model_critical(t_fit, *params)
        label = "Amortissement critique"
    elif forced_model == "over":
        params, cov = fit_over(t, y)
        y_fit = model_over(t_fit, *params)
        label = "Amortissement fort"
    else:
        raise ValueError("Modèle forcé invalide")

    sigma = np.sqrt(np.diag(cov))
    print(f"\nModèle utilisé : {label}")
    for val, err in zip(params, sigma):
        print(f"{val:.6g} ± {err:.3g}")

    plot_fit(f"{exp_name} — {label}", t, y, t_fit, y_fit)
    return filepath.replace(".csv", "_plot.png")

# ===============================
# Expériences et fichiers
# ===============================
exp_names = ["a", "exp_e", "exp_f"]
experiences = [
    ["egale_0.csv", "mgra_10_.csv", "mgra_50.csv", "pgra_10.csv", "pgra_35.csv"],
    ["e_aff.csv", "e_aci.csv", "e_air.csv", "e_alu.csv"],
    ["f_aci.csv", "f_aff.csv", "f_air.csv", "f_alu.csv"]
]

# ===============================
# Forçage des modèles
# ===============================
FORCED_MODELS = {
    "egale_0.csv": "critical",
    "mgra_10_.csv": "under",
    "mgra_50.csv": "over",
    "pgra_10.csv": "critical",
    "pgra_35.csv": "critical",
    "e_aff.csv": "under",
    "e_aci.csv": "under",
    "e_air.csv": "under",
    "e_alu.csv": "under",
    "f_aci.csv": "under",
    "f_aff.csv": "under",
    "f_air.csv": "under",
    "f_alu.csv": "under",
}

# ===============================
# Boucle principale
# ===============================
iteration = 0
for exp in experiences:
    for file in exp:
        dir_path = exp_names[iteration] + "/"
        model = FORCED_MODELS.get(file)
        if model is None:
            raise RuntimeError(f"Aucun modèle défini pour {file}")
        smart_plot(dir_path + file, exp_names[iteration], model)
    iteration += 1

