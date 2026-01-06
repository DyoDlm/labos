import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

###############################################################################
# MODELES
###############################################################################

def amp_model(f, A0, f0, Q):
    return A0 / np.sqrt(1 + Q**2 * (f/f0 - f0/f)**2)

def phase_model(f, f0, Q, phi0):
    return np.degrees(phi0 + np.arctan(2*Q*(f/f0 - f0/f)))

def power_model(f, f0, Q):
    return 1 / (1 + Q**2 * (f/f0 - f0/f)**2)

###############################################################################
# LECTURE + ANALYSE AMPLITUDE / PHASE
###############################################################################

def analyze(df, label):

    f = df.iloc[:,1].astype(float).values
    A = df.iloc[:,3].astype(float).values
    P = df.iloc[:,5].astype(float).values

    idx = np.argsort(f)
    f = f[idx]; A = A[idx]; P = P[idx]

    # Fit amplitude
    p0_amp = [np.max(A), f[np.argmax(A)], 5]
    pars_amp, cov_amp = curve_fit(amp_model, f, A, p0=p0_amp, maxfev=20000)

    # Fit phase
    p0_phase = [pars_amp[1], pars_amp[2], 0]
    pars_phase, cov_phase = curve_fit(phase_model, f, P, p0=p0_phase, maxfev=20000)

    return {
        "label": label,
        "f": f, "A": A, "P": P,
        "amp_params": pars_amp,
        "amp_cov": cov_amp,
        "phase_params": pars_phase,
        "phase_cov": cov_phase
    }

###############################################################################
# ANALYSE PUISSANCE : FIT, INCERTITUDES, FWHM, Q
###############################################################################

def analyze_power(f, A):

    # Puissance normalisée
    P = (A / A.max())**2

    # Fit f0 et Q
    p0 = [f[np.argmax(P)], 5]
    pars, cov = curve_fit(power_model, f, P, p0=p0, maxfev=20000)
    f0, Q = pars
    σ_f0, σ_Q = np.sqrt(np.diag(cov))

    # FWHM numérique
    P_shift = P - 0.5
    interp = interp1d(f, P_shift)

    roots = []
    for i in range(len(f)-1):
        if P_shift[i] * P_shift[i+1] < 0:
            roots.append(float(interp(f[i])))

    if len(roots) == 2:
        fwhm = abs(roots[1] - roots[0])
    else:
        fwhm = np.nan

    # Incertitude FWHM via méthode des variations
    ε = 1e-4
    f_plus = power_model(f, f0 + σ_f0, Q)
    f_minus = power_model(f, f0 - σ_f0, Q)
    roots_plus, roots_minus = [], []

    for arr, store in [(f_plus - 0.5, roots_plus), (f_minus - 0.5, roots_minus)]:
        interp_pm = interp1d(f, arr)
        for i in range(len(f)-1):
            if arr[i] * arr[i+1] < 0:
                store.append(float(interp_pm(f[i])))

    if len(roots_plus) == 2 and len(roots_minus) == 2:
        fwhm_plus = abs(roots_plus[1] - roots_plus[0])
        fwhm_minus = abs(roots_minus[1] - roots_minus[0])
        σ_fwhm = 0.5 * abs(fwhm_plus - fwhm_minus)
    else:
        σ_fwhm = np.nan

    # Q expérimental
    Q_exp = f0 / fwhm
    σ_Qexp = Q_exp * np.sqrt( (σ_f0/f0)**2 + (σ_fwhm/fwhm)**2 )

    return {
        "f": f, "P": P,
        "f0": f0, "σ_f0": σ_f0,
        "Q_fit": Q, "σ_Q": σ_Q,
        "FWHM": fwhm, "σ_FWHM": σ_fwhm,
        "Q_exp": Q_exp, "σ_Qexp": σ_Qexp
    }

###############################################################################
# PROGRAMME PRINCIPAL
###############################################################################

file = "labo1Cphysique.xlsx"
df05 = pd.read_excel(file, sheet_name="0.5A")
df09 = pd.read_excel(file, sheet_name="0.9A")

res05 = analyze(df05, "0.5A")
res09 = analyze(df09, "0.9A")

power05 = analyze_power(res05["f"], res05["A"])
power09 = analyze_power(res09["f"], res09["A"])

###############################################################################
# GRAPHIQUES PUISSANCE
###############################################################################

def plot_power(power, label, color):

    f = power["f"]
    P = power["P"]
    f0 = power["f0"]
    Q = power["Q_fit"]

    plt.figure(figsize=(12,6))
    plt.scatter(f, P, color=color, s=20, label=f"{label} data")

    ffit = np.linspace(min(f), max(f), 800)
    plt.plot(ffit, power_model(ffit, f0, Q),
             color="black", linestyle="--", label=f"{label} fit")

    plt.axhline(0.5, color="gray", linestyle=":")
    plt.axvline(f0, color=color, linestyle="--")

    plt.xlabel("f [Hz]")
    plt.ylabel("P / P0")
    plt.grid()
    plt.legend()
    plt.savefig(f"power_{label}.png")

plot_power(power05, "0.5A", "blue")
plot_power(power09, "0.9A", "red")

###############################################################################
# RESULTATS NUMERIQUES
###############################################################################

print("\n===== RESULTATS PUISSANCE FORCÉE =====\n")

for label, p in zip(["0.5A", "0.9A"], [power05, power09]):
    print(f"--- {label} ---")
    print(f"f0 (fit)      = {p['f0']:.5f} ± {p['σ_f0']:.5f} Hz")
    print(f"Q (fit)       = {p['Q_fit']:.5f} ± {p['σ_Q']:.5f}")
    print(f"FWHM          = {p['FWHM']:.5f} ± {p['σ_FWHM']:.5f} Hz")
    print(f"Q_exp         = {p['Q_exp']:.5f} ± {p['σ_Qexp']:.5f}")
    print()

