import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

###############################################################################
# MODELES STABLES
###############################################################################

def amp_model(f, A0, f0, Q):
    return A0 / np.sqrt(1 + Q**2 * (f/f0 - f0/f)**2)

def phase_model(f, f0, Q, phi0):
    return np.degrees(phi0 + np.arctan(2*Q*(f/f0 - f0/f)))

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
    p0_amp = [np.max(A), f[np.argmax(A)], 5]
    pars_amp, _ = curve_fit(amp_model, f, A, p0=p0_amp, maxfev=20000)
    A0, f0_amp, Q_amp = pars_amp

    # ---- Fit phase ----
    p0_phase = [f0_amp, Q_amp, 0]
    pars_phase, _ = curve_fit(phase_model, f, P, p0=p0_phase, maxfev=20000)
    f0_phase, Q_phase, phi0 = pars_phase

    return {
        "label": label,
        "f": f, "A": A, "P": P,
        "amp_params": pars_amp,
        "phase_params": pars_phase
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
    A0, f0, Q = res["amp_params"]
    label = res["label"]
    c = colors[label]

    # données
    plt.scatter(f, A, color=c, s=20, label=f"{label} data")

    # fit
    ffit = np.linspace(min(f), max(f), 500)
    plt.plot(ffit, amp_model(ffit, A0, f0, Q), color=c, linestyle="--",
             label=f"{label} fit")

    # ligne verticale f0
    plt.axvline(f0, color=c, linestyle=":", alpha=0.8)
    plt.text(f0, max(A)*0.9, f"f0={f0:.3f} Hz", color=c, ha="left")

plt.title("Amplitude en fonction de la fréquence")
plt.xlabel("f [Hz]")
plt.ylabel("Amplitude [deg]")
plt.grid()
plt.legend()
#plt.show()
plt.savefig("force_amp.png")
###############################################################################
# GRAPHIQUE 2 : PHASES
###############################################################################

plt.figure(figsize=(12,6))

for res in (res05, res09):
    f = res["f"]
    P = res["P"]
    f0, Q, phi0 = res["phase_params"]
    label = res["label"]
    c = colors[label]

    # données
    plt.scatter(f, P, color=c, s=20, label=f"{label} data")

    # fit
    ffit = np.linspace(min(f), max(f), 500)
    plt.plot(ffit, phase_model(ffit, f0, Q, phi0), color=c, linestyle="--",
             label=f"{label} fit")

    # ligne verticale f0
    plt.axvline(f0, color=c, linestyle=":", alpha=0.8)
    plt.text(f0, np.mean(P), f"f0={f0:.3f} Hz", color=c, ha="left")

plt.title("Phase en fonction de la fréquence")
plt.xlabel("f [Hz]")
plt.ylabel(r"$\phi$ [°]")
plt.grid()
plt.legend()
#plt.show()
plt.savefig("force_phase.png")
###############################################################################
# Résultats numériques
###############################################################################

print("\n=== RÉSULTATS ===\n")

for res in (res05, res09):
    label = res["label"]
    A0, f0_amp, Q_amp = res["amp_params"]
    f0_phase, Q_phase, phi0 = res["phase_params"]

    print(f"--- {label} ---")
    print(f"f0 (amplitude) = {f0_amp:.5f} Hz")
    print(f"Q  (amplitude) = {Q_amp:.5f}")
    print()
    print(f"f0 (phase)     = {f0_phase:.5f} Hz")
    print(f"Q  (phase)     = {Q_phase:.5f}")
    print(f"phi0 (phase)   = {phi0:.3f}")
    print()

