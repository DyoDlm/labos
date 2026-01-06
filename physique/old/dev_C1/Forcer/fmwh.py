import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

###############################################################################
# LARGEUR A MI-HAUTEUR (FWHM)
###############################################################################

def compute_fwhm(f, y):
    """Retourne la largeur à mi-hauteur Δf."""
    half = np.max(y) / 2
    roots = []

    for i in range(len(f)-1):
        y1 = y[i] - half
        y2 = y[i+1] - half
        if y1 * y2 < 0:  # changement de signe
            # interpolation linéaire
            root = f[i] - y1*(f[i+1]-f[i])/(y[i+1]-y[i])
            roots.append(root)

    if len(roots) == 2:
        return roots[1] - roots[0]
    return np.nan

###############################################################################
# PUISSANCE RELATIVE
###############################################################################

def relative_power(f, A, f0):
    A_interp = interp1d(f, A, kind="cubic", fill_value="extrapolate")
    A0 = A_interp(f0)
    return (A/A0)**2

###############################################################################
# Q = f0 / Δf
###############################################################################

def compute_Q(f, A, f0):
    idx = np.argsort(f)
    f = f[idx]
    A = A[idx]

    P_rel = relative_power(f, A, f0)
    df = compute_fwhm(f, P_rel)
    Q = f0 / df

    return Q, f, P_rel, df

###############################################################################
# PROGRAMME PRINCIPAL
###############################################################################

file = "labo1Cphysique.xlsx"

df05 = pd.read_excel(file, sheet_name="0.5A")
f05 = df05.iloc[:,1].astype(float).values
A05 = df05.iloc[:,3].astype(float).values

f0_05 = 0.45  # Remplacer par res05["f0_amp"]

Q05, f_sorted05, P_rel05, df_width05 = compute_Q(f05, A05, f0_05)

print("=== Q pour 0.5A ===")
print("f0 =", f0_05)
print("Δf =", df_width05)
print("Q =", Q05)

