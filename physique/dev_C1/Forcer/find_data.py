import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

###############################################################################
# MODELES STABLES
###############################################################################

def amp_model(f, A0, f0, gamma):
    """Amplitude en fonction de la fréquence pour un oscillateur forcé amorti"""
    return A0 / np.sqrt((1 - (f/f0)**2)**2 + (2*gamma*f/f0)**2)

def phase_model(f, f0, gamma, phi0):
    """Phase en fonction de la fréquence"""
    return np.degrees(phi0 + np.arctan2(2*gamma*f/f0, 1 - (f/f0)**2))

###############################################################################
# ANALYSE D’UN SHEET
###############################################################################

def analyze(df, label):
    f = df.iloc[:,1].astype(float).values
    A = df.iloc[:,3].astype(float).values
    P = df.iloc[:,5].astype(float).values

    idx = np.argsort(f)
    f = f[idx]; A = A[idx]; P = P[idx]

    # ---- Fit amplitude ----
    p0_amp = [np.max(A), f[np.argmax(A)], 0.05]  # A0, f0, gamma
    pars_amp, cov_amp = curve_fit(amp_model, f, A, p0=p0_amp, maxfev=200000)
    A0, f0, gamma = pars_amp
    sigma_A0, sigma_f0, sigma_gamma = np.sqrt(np.diag(cov_amp))

    # ---- Fit phase ----
    p0_phase = [f0, gamma, 0]
    pars_phase, cov_phase = curve_fit(phase_model, f, P, p0=p0_phase, maxfev=500000)
    f0_phase, gamma_phase, phi0 = pars_phase

    # ---- Calcul des pulsations ----
    omega_d = 2*np.pi*f0            # pseudo-pulsation (pic amplitude)
    omega_d_err = 2*np.pi*sigma_f0

    # pulsation propre approximée à partir du fit canonique
    omega0 = 2*np.pi*f0 * np.sqrt(1 + 2*gamma**2)  # gamma petit, approx.
    omega0_err = 2*np.pi*sigma_f0

    return {
        "label": label,
        "f": f, "A": A, "P": P,
        "amp_params": pars_amp,
        "phase_params": pars_phase,
        "omega0": omega0,
        "omega0_err": omega0_err,
        "omega_d": omega_d,
        "omega_d_err": omega_d_err
    }

###############################################################################
# PROGRAMME PRINCIPAL
###############################################################################

file = "labo1Cphysique.xlsx"
df05 = pd.read_excel(file, sheet_name="0.5A")
df09 = pd.read_excel(file, sheet_name="0.9A")

res05 = analyze(df05, "0.5A")
res09 = analyze(df09, "0.9A")

###############################################################################
# GRAPHIQUE 1 : AMPLITUDES
###############################################################################

plt.figure(figsize=(12,6))
colors = {"0.5A":"blue", "0.9A":"red"}

for res in (res05, res09):
    f = res["f"]
    A = res["A"]
    A0, f0, gamma = res["amp_params"]
    label = res["label"]
    c = colors[label]

    # données
    plt.scatter(f, A, color=c, s=20, label=f"{label} data")

    # fit
    ffit = np.linspace(min(f), max(f), 500)
    plt.plot(ffit, amp_model(ffit, A0, f0, gamma), color=c, linestyle="--",
             label=f"{label} fit")

    # ligne verticale f0
    plt.axvline(f0, color=c, linestyle=":", alpha=0.8)
    plt.text(f0, max(A)*0.9, f"f0={f0:.3f} Hz", color=c, ha="left")

plt.title("Amplitude en fonction de la fréquence")
plt.xlabel("f [Hz]")
plt.ylabel("Amplitude [deg]")
plt.grid()
plt.legend()
plt.savefig("force_amp.png")

###############################################################################
# GRAPHIQUE 2 : PHASES
###############################################################################

plt.figure(figsize=(12,6))

for res in (res05, res09):
    f = res["f"]
    P = res["P"]
    f0, gamma, phi0 = res["phase_params"]
    label = res["label"]
    c = colors[label]

    # données
    plt.scatter(f, P, color=c, s=20, label=f"{label} data")

    # fit
    ffit = np.linspace(min(f), max(f), 500)
    plt.plot(ffit, phase_model(ffit, f0, gamma, phi0), color=c, linestyle="--",
             label=f"{label} fit")

    # ligne verticale f0
    plt.axvline(f0, color=c, linestyle=":", alpha=0.8)
    plt.text(f0, np.mean(P), f"f0={f0:.3f} Hz", color=c, ha="left")

plt.title("Phase en fonction de la fréquence")
plt.xlabel("f [Hz]")
plt.ylabel(r"$\phi$ [°]")
plt.grid()
plt.legend()
plt.savefig("force_phase.png")

###############################################################################
# Résultats numériques
###############################################################################

print("\n=== RÉSULTATS ===\n")

for res in (res05, res09):
    label = res["label"]
    A0, f0, gamma = res["amp_params"]
    f0_phase, gamma_phase, phi0 = res["phase_params"]
    omega0 = res["omega0"]
    omega0_err = res["omega0_err"]
    omega_d = res["omega_d"]
    omega_d_err = res["omega_d_err"]

    print(f"--- {label} ---")
    print(f"A0      = {A0:.5f} ± {np.nan:.5f} (approx.)")
    print(f"gamma   = {gamma:.5f} ± {np.nan:.5f} (approx.)")
    print(f"ω0      = {omega0:.4f} ± {omega0_err:.4f} rad/s")
    print(f"ω_d     = {omega_d:.4f} ± {omega_d_err:.4f} rad/s")
    print()

