# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================
# Modèles physiques
# ============================================================
def underdamped(t, A, alpha, omega, phi):
    return A * np.exp(-alpha * t) * np.cos(omega * t + phi)

def critical(t, A, B, alpha):
    return (A + B*t) * np.exp(-alpha * t)

def overdamped(t, A, B, alpha1, alpha2):
    return A * np.exp(-alpha1 * t) + B * np.exp(-alpha2 * t)

def envelope(t, A, alpha):
    return A * np.exp(-alpha * t)

# ============================================================
# Outils statistiques
# ============================================================
def compute_aic(y, y_fit, k):
    n = len(y)
    rss = np.sum((y - y_fit)**2)
    if rss <= 0:
        return np.inf
    return n * np.log(rss / n) + 2*k

# ============================================================
# Estimation spectrale
# ============================================================
def estimate_omega_fft(x, y):
    y0 = y - np.mean(y)
    dt = np.mean(np.diff(x))
    fft = np.fft.rfft(y0)
    freqs = np.fft.rfftfreq(len(y0), dt)
    idx = np.argmax(np.abs(fft[1:])) + 1
    return 2*np.pi*freqs[idx]

# ============================================================
# Nettoyage des données
# ============================================================
#def clean_data(df):
#    x = pd.to_numeric(df.iloc[:,0], errors='coerce')
#    y = pd.to_numeric(df.iloc[:,1], errors='coerce')
#    mask = np.isfinite(x) & np.isfinite(y)
#    x, y = x[mask].values, y[mask].values
#    idx = np.argsort(x)
#    x, y = x[idx], y[idx]
#    _, uidx = np.unique(x, return_index=True)
#    x, y = x[uidx], y[uidx]
#    if len(x) < 15:
#        raise ValueError("Nombre de points insuffisant pour une analyse fiable.")
#    return x, y

def clean_data(df, min_points_plateau=5, rel_tol=0.01):
    """
    Nettoie les données et supprime le plateau initial.
    - min_points_plateau : nombre de points consécutifs dépassant le seuil pour détecter début oscillation
    - rel_tol : tolérance relative par rapport à la plage après plateau
    """
    x = pd.to_numeric(df.iloc[:,0], errors='coerce')
    y = pd.to_numeric(df.iloc[:,1], errors='coerce')

    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask].values, y[mask].values

    # Tri et suppression des doublons
    idx = np.argsort(x)
    x, y = x[idx], y[idx]
    _, uidx = np.unique(x, return_index=True)
    x, y = x[uidx], y[uidx]

    # Estimation plateau initial
    plateau_end = 10
    A_init = np.mean(y[:plateau_end])
    
    # Seuil basé sur amplitude après plateau
    y_rest = y[plateau_end:]
    threshold = rel_tol * (np.max(y_rest) - np.min(y_rest))

    # Chercher le premier point où min_points_plateau consécutifs dépassent le seuil
    start_idx = plateau_end
    while start_idx + min_points_plateau < len(y):
        if np.all(np.abs(y[start_idx:start_idx+min_points_plateau] - A_init) > threshold):
            break
        start_idx += 1

    x, y = x[start_idx:], y[start_idx:]

    if len(x) < 15:
        raise ValueError("Nombre de points insuffisant après nettoyage.")

    return x, y




# ============================================================
# Contraintes
# ============================================================
BOUNDS_UNDERDAMPED = ([0, 0, 0, -np.pi], [np.inf, np.inf, np.inf, np.pi])
BOUNDS_CRITICAL = ([-np.inf, -np.inf, 0], [np.inf, np.inf, np.inf])
BOUNDS_OVERDAMPED = ([-np.inf, -np.inf, 0, 0], [np.inf, np.inf, np.inf, np.inf])

# ============================================================
# Vérification physique
# ============================================================
def is_physical_underdamped(popt, x):
    A, alpha, omega, _ = popt
    T_obs = x[-1] - x[0]
    if A <= 0 or alpha < 0 or omega < 2*np.pi/T_obs:
        return False
    return True

# ============================================================
# Sélection du meilleur modèle avec forçage
# ============================================================
def select_best_model(x, y, iteration, forced_models=None):
    forced_name = forced_models.get(iteration) if forced_models else None

    omega0 = estimate_omega_fft(x, y)
    A0 = np.max(np.abs(y))
    alpha0 = 1/(x[-1]-x[0])

    models = {
        "Faiblement amorti": {"func":underdamped, "p0":[A0, alpha0, omega0, 0], "bounds":BOUNDS_UNDERDAMPED, "k":4, "check":is_physical_underdamped},
        "Critique": {"func":critical, "p0":[A0, -A0/(x[-1]-x[0]), alpha0], "bounds":BOUNDS_CRITICAL, "k":3, "check":None},
        "Fortement amorti": {"func":overdamped, "p0":[A0, -A0, alpha0, 5*alpha0], "bounds":BOUNDS_OVERDAMPED, "k":4, "check":None}
    }

    best = {"name":None, "aic":np.inf, "popt":None, "y_fit":None}

    for name, m in models.items():
        if forced_name is not None and name != forced_name:
            continue
        try:
            popt, pcov = curve_fit(m["func"],
                                   x, y,
                                   p0=m["p0"],
                                   bounds=m["bounds"],
                                   maxfev=40000
                                   )
            if m["check"] is not None and not m["check"](popt, x):
                continue
            y_fit = m["func"](x, *popt)
            aic = compute_aic(y, y_fit, m["k"])
            if aic < best["aic"]:
                best.update({"name":name, "aic":aic,
                             "popt":popt, "pcov":pcov, 
                             "y_fit":y_fit})
        except (RuntimeError, ValueError):
            continue
    if best["name"] is None:
        raise RuntimeError("Aucun modèle valide trouvé.")
    return best


def find_decimals(var):
    strdecimal = str(var)
    i_ = 0
    i = 0
    while strdecimal[i_] == '0' or strdecimal[i_] == '.':
        #if strdecimal[i_] == '0':
        i += 1
        i_ += 1
    return i

# ============================================================
# Tracé final
# ============================================================
def plot(df, name, iteration, forced_models):
    fileName = name.replace(".csv","_plot.png")
    x, y = clean_data(df)
    result = select_best_model(x, y, iteration, forced_models)
    regime = result["name"]
    popt = result["popt"]
    pcov = result["pcov"]
    perr = np.sqrt(np.diag(pcov))
    y_fit = result["y_fit"]

    plt.figure(figsize=(9,5))
    plt.grid(True)
    plt.plot(x, y, "o", label="Données")

    if regime == "Faiblement amorti":
        A, alpha, omega, phi = popt
        dA, dalpha, domega, dphi = perr
        nA = find_decimals(A) 
        nalpha = find_decimals(alpha)
        nomega = find_decimals(omega)
        nphi = find_decimals(phi)

        y_env = envelope(x, A, alpha)
        plt.plot(x, y_fit, "-", label=f"Fit oscillatoire")
        plt.plot(x, y_env, "--", label="Enveloppe exponentielle")
        equation = (
        rf"$U(t)={A:.{nA + 2}f}e^{{-{alpha:.{nalpha}f}t}}"
        rf"\cos({omega:.{nomega}f}t+{phi:.{nphi}f})$"
    )

    elif regime == "Critique":
        A, B, alpha = popt
        dA, dB, dalpha = perr
        nA = find_decimals(A)
        nB = find_decimals(B)
        nalpha = find_decimals(alpha)

        plt.plot(x, y_fit, "-", label="Fit critique")
        equation = rf"$U(t)=({A:.{nA + 2}f}+{B:.{nB}f}t) \cdot e^{{-{alpha:.{nalpha}f}t}}$"
    else:
        A, B, a1, a2 = popt
        dA, dB, da1, da2 = perr
        nA = find_decimals(A)
        nB = find_decimals(B)
        na1 = find_decimals(a1)
        na2 = find_decimals(a2)

        plt.plot(x, y_fit, "-", label="Fit fort")
        equation = rf"$U(t)={A:.{nA + 2}f} \cdot e^{{-{a1:.{na1}f}t}}+{B:.{nB}f} \cdot e^{{-{a2:.{na2}f}t}}$"

    print(f"------{fileName}-------")

    if regime == "Faiblement amorti":
        print(f"Regime : {regime}")
        print(f"A (Amplitude initiale)                : {A:.5f} ± {dA:.{nA + 4}f}")
        print(f"Lambda (coeff. d'amortissement)       : {alpha:.{nalpha + 3}f} ± {dalpha:.{nalpha + 1}f}")
        print(f"Omega (pulsation)                     : {omega:.{nomega + 3}f} ± {domega:.{nomega + 1}f}")
        print(f"Phi (déphasage)                       : {phi:.{nphi + 4}f} ± {dphi:.{nphi + 1}f}")

    elif regime == "Critique":
        print(f"Regime : {regime}")
        print(f"A (constante initiale) : {A:.{nA + 3}f} ± {dA:.{nA + 3}f}")
        print(f"B (coefficient linéaire) : {B:.{nB + 4}f} ± {dB:.{nB}f}")
        print(f"Lambda : {alpha:.{nalpha + 4}f} ± {dalpha:.{nalpha + 1}f}")

    else:
        print(f"Regime : {regime}")
        print(f"A (amplitude e1) : {A:.{nA + 3}f} ± {dA:.{nA + 3}f}")
        print(f"B (amplitude e2) : {B:.{nB + 2}f} ± {dB:.{nB + 2}f}")
        print(f"Lambda 1 : {a1:.{na1 + 3}f} ± {da1:.{na1 + 1}f}")
        print(f"Lambda 2 : {a2:.{na2 + 3}f} ± {da2:.{na2 + 1}f}")


    print("-----------------------")
    plt.xlabel("t \ s")
    plt.ylabel("U \ V")
    plt.title(f"{name} — {regime}")
    plt.text(0.02, 0.95, equation, transform=plt.gca().transAxes,
             fontsize=11, verticalalignment="top",
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.9))
    plt.legend()
    plt.tight_layout()
    plt.savefig(fileName, dpi=300)
    plt.show()

# ============================================================
# Dictionnaire d'expériences
# ============================================================
experiences = {
    "a": ["egale_0.csv", "mgra_10_.csv", "mgra_50.csv", "pgra_10.csv", "pgra_35.csv"],
    "exp_e": ["e_aff.csv", "e_aci.csv", "e_air.csv", "e_alu.csv"],
    "exp_f": ["f_aci.csv", "f_aff.csv", "f_air.csv", "f_alu.csv"]
}

# Forçage des modèles (itération correspond au numéro du fichier)
FORCED_MODELS = {
        2: "Faiblement amorti",
    11: "Faiblement amorti",
    12: "Faiblement amorti"
}

# ============================================================
# Boucle principale
# ============================================================
iteration = 1
for exp_name, files in experiences.items():
    for file in files:
        dir_path = f"{exp_name}/{file}"
        try:
            df = pd.read_csv(dir_path)
            plot(df, file, iteration, FORCED_MODELS)
        except Exception as e:
            print(f"Erreur sur {file}: {e}")
        iteration += 1

