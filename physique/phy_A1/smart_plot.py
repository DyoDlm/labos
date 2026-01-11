#import matplotlib.pyplot as plt
#import pandas as pd
#import numpy as np
#from scipy.signal import find_peaks
#from scipy.optimize import curve_fit

#   define raw data
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
#    tab2 = tab[0].split(".csv")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyse automatique de signaux amortis (RLC, mécanique, etc.)

- Nettoyage des données CSV
- Test de plusieurs modèles physiques
- Sélection objective via AIC
- Affichage du meilleur fit et de l'équation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.signal import find_peaks


# ============================================================
# Modèles physiques
# ============================================================

def underdamped(t, A, alpha, omega, phi):
    """Régime faiblement amorti"""
    return A * np.exp(-alpha * t) * np.cos(omega * t + phi)


def critical(t, A, B, alpha):
    """Régime critique"""
    return (A + B * t) * np.exp(-alpha * t)


def overdamped(t, A, B, alpha1, alpha2):
    """Régime fortement amorti"""
    return A * np.exp(-alpha1 * t) + B * np.exp(-alpha2 * t)


# ============================================================
# Outils statistiques
# ============================================================

def compute_aic(y, y_fit, k):
    """
    Akaike Information Criterion
    k : nombre de paramètres
    """
    n = len(y)
    rss = np.sum((y - y_fit) ** 2)

    if rss <= 0:
        return np.inf

    return n * np.log(rss / n) + 2 * k


# ============================================================
# Nettoyage et préparation des données
# ============================================================

def clean_data(df):
    """
    Nettoie et prépare les données expérimentales
    """
    x = pd.to_numeric(df.iloc[:, 0], errors="coerce")
    y = pd.to_numeric(df.iloc[:, 1], errors="coerce")

    # Suppression NaN et inf
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]

    # Conversion numpy
    x, y = x.values, y.values

    # Tri par temps croissant
    idx = np.argsort(x)
    x, y = x[idx], y[idx]

    # Suppression doublons
    _, unique_idx = np.unique(x, return_index=True)
    x, y = x[unique_idx], y[unique_idx]

    if len(x) < 10:
        raise ValueError("Pas assez de points valides pour une analyse fiable.")

    return x, y


# ============================================================
# Sélection automatique du meilleur modèle
# ============================================================

def select_best_model(x, y):
    """
    Fit tous les modèles et sélectionne le meilleur via AIC
    """

    models = {
        "Faiblement amorti": {
            "func": underdamped,
            "p0": [np.max(y), 1.0, 10.0, 0.0],
            "k": 4
        },
        "Critique": {
            "func": critical,
            "p0": [np.max(y), -1.0, 1.0],
            "k": 3
        },
        "Fortement amorti": {
            "func": overdamped,
            "p0": [np.max(y), -np.max(y), 1.0, 5.0],
            "k": 4
        }
    }

    best = {
        "name": None,
        "aic": np.inf,
        "popt": None,
        "y_fit": None
    }

    for name, model in models.items():
        try:
            popt, _ = curve_fit(
                model["func"],
                x,
                y,
                p0=model["p0"],
                maxfev=200000
            )

            y_fit = model["func"](x, *popt)
            aic = compute_aic(y, y_fit, model["k"])

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
        raise RuntimeError("Aucun modèle n'a pu être ajusté correctement.")

    return best


# ============================================================
# Fonction principale de tracé
# ============================================================

def plot(df, name):
    """
    Analyse complète et tracé
    """
    fileName = name.split(".csv")[0] + "_plot.png"
    print(f"Fichier généré : {fileName}")

    x, y = clean_data(df)
    result = select_best_model(x, y)

    regime = result["name"]
    popt = result["popt"]
    y_fit = result["y_fit"]

    # Construction équation affichée
    if regime == "Faiblement amorti":
        A, alpha, omega, phi = popt
        equation = rf"$U(t)={A:.3g}e^{{-{alpha:.3g}t}}\cos({omega:.3g}t+{phi:.3g})$"

    elif regime == "Critique":
        A, B, alpha = popt
        equation = rf"$U(t)=({A:.3g}+{B:.3g}t)e^{{-{alpha:.3g}t}}$"

    else:
        A, B, a1, a2 = popt
        equation = rf"$U(t)={A:.3g}e^{{-{a1:.3g}t}}+{B:.3g}e^{{-{a2:.3g}t}}$"

    # Tracé
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
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
    )

    plt.legend()
    plt.tight_layout()
    plt.savefig(fileName, dpi=300)
    plt.show()

    return fileName


# ============================================================
# Exemple d'utilisation
# ============================================================

    df = pd.read_csv("data.csv", sep=",")
    plot(df, "data.csv")


iteration = 0
for exp in experiences:
    for file in exp:
        dir = exp_names[iteration] + "/"
        df = pd.read_csv(dir + file)
#        df = pd.read_excel(dir + file, engine=".ods")
        new = plot(df, file)#exp_names[iteration], file)
        print(f"New file created : {new} !")
    iteration += 1

