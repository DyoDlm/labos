import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


# ---------------------------------------------------------
# Fonction FWHM robuste
# ---------------------------------------------------------
def compute_fwhm(freq, curve):
    """
    freq : tableau de fréquences (déjà interpolé)
    curve : tableau normalisé entre 0 et 1
    Retourne : FWHM, f_low, f_high
    """
    target = 0.5
    indices = np.where(np.diff(np.sign(curve - target)))[0]

    if len(indices) < 2:
        raise RuntimeError("Impossible de trouver deux points pour le FWHM — données insuffisantes.")

    # interpolation pour chaque croisement
    f1 = np.interp(target,
                   [curve[indices[0]], curve[indices[0] + 1]],
                   [freq[indices[0]], freq[indices[0] + 1]])

    f2 = np.interp(target,
                   [curve[indices[1]], curve[indices[1] + 1]],
                   [freq[indices[1]], freq[indices[1] + 1]])

    return abs(f2 - f1), f1, f2


# ---------------------------------------------------------
# Analyse
# ---------------------------------------------------------
def analyze_sheet(df, label):
    print(f"\n--- Analyse {label} ---")

    # === Charger données ===
    f = df["Freq [Hz]"].astype(float).values
    A = df["Amplitude"].astype(float).values
    phase = df["Phase [°]"].astype(float).values

    # === Trier par fréquence ===
    idx = np.argsort(f)
    f = f[idx]
    A = A[idx]
    phase = phase[idx]

    # === Puissance ===
    P = A**2

    # === Normalisation par le maximum réel ===
    P_rel = P / np.max(P)

    # === Interpolation fine ===
    F_interp = np.linspace(np.min(f), np.max(f), 2000)
    P_interp = interp1d(f, P_rel, kind='cubic')(F_interp)

    # === Calcul FWHM ===
    fwhm, f_low, f_high = compute_fwhm(F_interp, P_interp)
    f0_meas = F_interp[np.argmax(P_interp)]
    Q = f0_meas / fwhm

    print(f"f0 mesuré = {f0_meas:.4f} Hz")
    print(f"FWHM = {fwhm:.5f} Hz")
    print(f"Limite basse = {f_low:.4f} Hz")
    print(f"Limite haute = {f_high:.4f} Hz")
    print(f"Q = {Q:.3f}")

    # ---------------------------------------------------------
    # PLOTS
    # ---------------------------------------------------------

    # Amplitude
    plt.figure(figsize=(7,5))
    plt.plot(f, A, 'o-', label="Amplitude")
    plt.axvline(f0_meas, color='r', linestyle='--', label="f0 mesuré")
    plt.title(f"Amplitude vs fréquence ({label})")
    plt.xlabel("f [Hz]")
    plt.ylabel("Amplitude [°]")
    plt.grid()
    plt.legend()

    # Puissance relative + FWHM
    plt.figure(figsize=(7,5))
    plt.plot(F_interp, P_interp, '-', label="P_rel interpolé")
    plt.axhline(0.5, color='r', linestyle='--', label="1/2 max")
    plt.axvline(f_low, color='g', linestyle='--', label="FWHM low")
    plt.axvline(f_high, color='g', linestyle='--', label="FWHM high")
    plt.title(f"Puissance relative + FWHM ({label})")
    plt.xlabel("f [Hz]")
    plt.ylabel("P_rel")
    plt.grid()
    plt.legend()

    # Phase
    plt.figure(figsize=(7,5))
    plt.plot(f, phase, 'o-', label="Phase")
    plt.axvline(f0_meas, color='r', linestyle='--')
    plt.title(f"Phase vs fréquence ({label})")
    plt.xlabel("f [Hz]")
    plt.ylabel("Phase [°]")
    plt.grid()
    plt.legend()

    plt.show()

    return {
        "f0": f0_meas,
        "FWHM": fwhm,
        "Q": Q,
        "f_low": f_low,
        "f_high": f_high
    }


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
file = "labo1Cphysique.xlsx"

df05 = pd.read_excel(file, sheet_name="0.5A")
df09 = pd.read_excel(file, sheet_name="0.9A")

print(df05.columns.tolist())
print(df09.columns.tolist())

res05 = analyze_sheet(df05, "0.5A")
res09 = analyze_sheet(df09, "0.9A")

