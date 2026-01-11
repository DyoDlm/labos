exp = "Decharge de condenstateur"
a_names = ["egale_0.csv", "mgra_10_.csv", "mgra_50.csv", "pgra_10.csv", "pgra_35.csv"]
a_is = ["Amortissement faible", "Amortissement fort", "Amortissement critique"]


exp = "Mesure des oscillation d'une bobine de cuivre avec inductances variables"
e_names = ["e_aff.csv", "e_aci.csv", "e_air.csv", "e_alu.csv"]
e_is = ["Oscillation acier feuillete", "Oscillation acier", "Oscillation air", "Oscillation aluminium"]


exp = "Mesures de comparaison pour la bobine d'inductance"
f_names = ["f_aci.csv", "f_aff.csv", "f_air.csv", "f_alu.csv"]
f_is = []


experiences = [a_names,e_names,f_names]
exp_names = ["a", "exp_e", "exp_f"]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse professionnelle de signaux amortis

- Nettoyage rigoureux des données
- Ajustement de modèles physiques concurrents
- Estimation spectrale préalable (FFT)
- Contraintes physiques sur les paramètres
- Sélection objective par AIC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
FORCED_MODELS = {
    1:  "Faiblement amorti",
    10: "Faiblement amorti",
    11: "Faiblement amorti",
}


# ============================================================
# Modèles physiques
# ============================================================

def underdamped(t, A, alpha, omega, phi):
    return A * np.exp(-alpha * t) * np.cos(omega * t + phi)


def critical(t, A, B, alpha):
    return (A + B * t) * np.exp(-alpha * t)


def overdamped(t, A, B, alpha1, alpha2):
    return A * np.exp(-alpha1 * t) + B * np.exp(-alpha2 * t)


# ============================================================
# Outils statistiques
# ============================================================

def compute_aic(y, y_fit, k):
    n = len(y)
    rss = np.sum((y - y_fit) ** 2)
    if rss <= 0:
        return np.inf
    return n * np.log(rss / n) + 2 * k


# ============================================================
# Estimation spectrale (clé de la robustesse)
# ============================================================

def estimate_omega_fft(x, y):
    """
    Estimation robuste de la pulsation dominante via FFT
    """
    y0 = y - np.mean(y)
    dt = np.mean(np.diff(x))

    fft = np.fft.rfft(y0)
    freqs = np.fft.rfftfreq(len(y0), dt)

    idx = np.argmax(np.abs(fft[1:])) + 1
    return 2 * np.pi * freqs[idx]


# ============================================================
# Nettoyage des données
# ============================================================

def clean_data(df):
    x = pd.to_numeric(df.iloc[:, 0], errors="coerce")
    y = pd.to_numeric(df.iloc[:, 1], errors="coerce")

    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]

    x, y = x.values, y.values

    idx = np.argsort(x)
    x, y = x[idx], y[idx]

    _, uidx = np.unique(x, return_index=True)
    x, y = x[uidx], y[uidx]

    if len(x) < 15:
        raise ValueError("Nombre de points insuffisant pour une analyse fiable.")

    return x, y


# ============================================================
# Contraintes physiques
# ============================================================

BOUNDS_UNDERDAMPED = (
    [0, 0, 0, -np.pi],
    [np.inf, np.inf, np.inf, np.pi]
)

BOUNDS_CRITICAL = (
    [-np.inf, -np.inf, 0],
    [np.inf, np.inf, np.inf]
)

BOUNDS_OVERDAMPED = (
    [-np.inf, -np.inf, 0, 0],
    [np.inf, np.inf, np.inf, np.inf]
)


def is_physical_underdamped(popt, x):
    A, alpha, omega, _ = popt
    T_obs = x[-1] - x[0]

    if A <= 0:
        return False
    if alpha < 0:
        return False
    if omega < 2 * np.pi / T_obs:
        return False

    return True


# ============================================================
# Sélection du meilleur modèle
# ============================================================

def select_best_model(x, y, iteration, forced_models=None):

    # ---------- Forçage éventuel
    forced_name = None

    if iteration == 1 or iteration == 10 or iteration == 11:
        forced_name = "Faiblement amorti"

    models = {}

    omega0 = estimate_omega_fft(x, y)
    A0 = np.max(np.abs(y))
    alpha0 = 1 / (x[-1] - x[0])

    models["Faiblement amorti"] = {
        "func": underdamped,
        "p0": [A0, alpha0, omega0, 0],
        "bounds": BOUNDS_UNDERDAMPED,
        "k": 4,
        "check": is_physical_underdamped
    }

    models["Critique"] = {
        "func": critical,
        "p0": [A0, -A0 / (x[-1] - x[0]), alpha0],
        "bounds": BOUNDS_CRITICAL,
        "k": 3,
        "check": None
    }

    models["Fortement amorti"] = {
        "func": overdamped,
        "p0": [A0, -A0, alpha0, 5 * alpha0],
        "bounds": BOUNDS_OVERDAMPED,
        "k": 4,
        "check": None
    }

    best = {
        "name": None,
        "aic": np.inf,
        "popt": None,
        "y_fit": None
    }

    for name, m in models.items():

        # 👉 Forçage ici

        if forced_name is not None and name != forced_name:
            continue

        try:
            popt, _ = curve_fit(
                m["func"],
                x, y,
                p0=m["p0"],
                bounds=m["bounds"],
                maxfev=40000
            )

            if m["check"] is not None:
                if not m["check"](popt, x):
                    continue

            y_fit = m["func"](x, *popt)
            aic = compute_aic(y, y_fit, m["k"])

            if aic < best["aic"]:
                best.update({
                    "name": name,
                    "aic": aic,
                    "popt": popt,
                    "y_fit": y_fit
                })

        except (RuntimeError, ValueError):
            continue

    if best["name"] is None:
        raise RuntimeError("Aucun modèle valide n'a été trouvé.")

    return best


# ============================================================
# Tracé final
# ============================================================

def plot(df, name, iteration, forced_models):
    fileName = name.replace(".csv", "_plot.png")

    x, y = clean_data(df)
    result = select_best_model(x, y, iteration, forced_models)

    regime = result["name"]
    popt = result["popt"]
    y_fit = result["y_fit"]

    if regime == "Faiblement amorti":
        A, alpha, omega, phi = popt
        equation = rf"$U(t)={A:.3g}e^{{-{alpha:.3g}t}}\cos({omega:.3g}t+{phi:.3g})$"
    elif regime == "Critique":
        A, B, alpha = popt
        equation = rf"$U(t)=({A:.3g}+{B:.3g}t)e^{{-{alpha:.3g}t}}$"
    else:
        A, B, a1, a2 = popt
        equation = rf"$U(t)={A:.3g}e^{{-{a1:.3g}t}}+{B:.3g}e^{{-{a2:.3g}t}}$"

    plt.figure(figsize=(9, 5))
    plt.grid(True)

    plt.plot(x, y, "o", label="Données expérimentales")
    plt.plot(x, y_fit, "-", label=f"Fit ({regime})")

    plt.xlabel("Temps [s]")
    plt.ylabel("Tension [V]")
    plt.title("Analyse automatique du régime amorti")

    plt.text(
        0.02, 0.95,
        equation,
        transform=plt.gca().transAxes,
        fontsize=11,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9)
    )

    plt.legend()
    plt.tight_layout()
    plt.savefig(fileName, dpi=300)
    plt.show()

    return fileName


# ============================================================
# Exemple d'utilisation
# ============================================================














iteration = 0
for exp in experiences:
    for file in exp:
        dir = exp_names[iteration] + "/"
        df = pd.read_csv(dir + file)
#        df = pd.read_excel(dir + file, engine=".ods")
        new = plot(df, file, iteration, FORCED_MODELS)
        print(f"New file created : {new} !")
    iteration += 1


