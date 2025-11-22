import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================
# 1. --- FONCTIONS UTILES ---
# ============================================================

def model(t, A, lam, omega1, phi, C):
    """ Oscillateur amorti : y = A e^{-λt} cos(ω1 t + φ) + C """
    return A * np.exp(-lam * t) * np.cos(omega1 * t + phi) + C

def omega0_and_uncertainty(omega1, sigma_omega1, lam, sigma_lam, cov_omega1_lam=0):
    """Propagation des incertitudes : ω0 = sqrt(ω1² + λ²)"""
    omega0 = np.sqrt(omega1**2 + lam**2)

    d1 = omega1 / omega0
    d2 = lam / omega0

    var = (d1**2)*sigma_omega1**2 + (d2**2)*sigma_lam**2 + 2*d1*d2*cov_omega1_lam
    return omega0, np.sqrt(var)

def format_val(val, err):
    """Retourne val ± err avec chiffres significatifs corrects."""
    if err == 0:
        return f"{val:.3g} ± 0"
    exp = int(np.floor(np.log10(abs(err))))
    n_dec = max(0, -exp + 1)
    return f"{val:.{n_dec}f} ± {err:.{n_dec}f}"

# ============================================================
# 2. --- CHARGEMENT AUTOMATIQUE DES .csv ---
# ============================================================

data_folder = "./"
csv_files = glob.glob(data_folder + "*.csv")

if not csv_files:
    raise FileNotFoundError("Aucun fichier .csv trouvé dans le dossier.")

print("Fichiers détectés :")
for f in csv_files:
    print(" →", f)

# ============================================================
# 3. --- BOUCLE SUR LES FICHIERS ---
# ============================================================

for filepath in csv_files:

    print("\n============================")
    print("Analyse du fichier :", filepath)
    print("============================")

    # Lecture du fichier
    df = pd.read_csv(filepath)
    t = df.iloc[:, 0].values
    y = df.iloc[:, 1].values

    # ============================================================
    # 4. --- FIT ---
    # ============================================================

    # Estimations initiales (robustes)
    A0 = (np.max(y) - np.min(y)) / 2
    lam0 = 0.02
    omega1_0 = 2*np.pi*0.5
    phi0 = 0
    C0 = np.mean(y)

    p0 = [A0, lam0, omega1_0, phi0, C0]

    pars, pcov = curve_fit(model, t, y, p0=p0, maxfev=20000)

    A, lam, omega1, phi, C = pars
    sigA, siglam, sigomega1, sigphi, sigC = np.sqrt(np.diag(pcov))

    cov_omega1_lam = pcov[2, 1]

    # ============================================================
    # 5. --- CALCUL DE ω0 ET SON INCERTITUDE ---
    # ============================================================

    omega0, sigma_omega0 = omega0_and_uncertainty(
        omega1, sigomega1, lam, siglam, cov_omega1_lam
    )

    # ============================================================
    # 6. --- AFFICHAGE DES RÉSULTATS ---
    # ============================================================

    print("\n--- Résultats :")
    print("A        =", format_val(A, sigA))
    print("λ        =", format_val(lam, siglam))
    print("ω₁       =", format_val(omega1, sigomega1))
    print("φ        =", format_val(phi, sigphi))
    print("C        =", format_val(C, sigC))
    print("ω₀       =", format_val(omega0, sigma_omega0))

    # ============================================================
    # 7. --- GRAPHIQUE ---
    # ============================================================

    plt.figure(figsize=(10, 6))
    plt.plot(t, y, 'b.', markersize=3, label="Mesures")
    plt.plot(t, model(t, *pars), 'r--', linewidth=2, label="Fit")

    plt.xlabel("Temps / s")
    plt.ylabel("Angle / °")
    plt.legend()

    # Zone texte sous le graphique
    txt = (
        f"A = {format_val(A, sigA)} °\n"
        f"λ = {format_val(lam, siglam)} s⁻¹\n"
        f"ω₁ = {format_val(omega1, sigomega1)} rad·s⁻¹\n"
        f"ω₀ = {format_val(omega0, sigma_omega0)} rad·s⁻¹\n"
        f"φ = {format_val(phi, sigphi)} rad"
    )

    plt.figtext(0.5, -0.15, txt, ha='center', fontsize=11)

    plt.tight_layout()
    plt.show()
# ============================================================
# 8. --- SAUVEGARDE DES RÉSULTATS ω0 DANS UN CSV ---
# ============================================================

resultats = {
    "fichier": [],
    "omega0": [],
    "sigma_omega0": []
}

for filepath in csv_files:

    # Relecture et refit (ou stockez durant la boucle principale)
    df = pd.read_csv(filepath)
    t = df.iloc[:, 0].values
    y = df.iloc[:, 1].values

    pars, pcov = curve_fit(model, t, y, p0=p0, maxfev=20000)
    A, lam, omega1, phi, C = pars
    sigA, siglam, sigomega1, sigphi, sigC = np.sqrt(np.diag(pcov))
    cov_omega1_lam = pcov[2, 1]

    # ω0 + incertitude
    omega0, sigma_omega0 = omega0_and_uncertainty(omega1, sigomega1, lam, siglam, cov_omega1_lam)

    # Stockage
    resultats["fichier"].append(filepath)
    resultats["omega0"].append(omega0)
    resultats["sigma_omega0"].append(sigma_omega0)

# Création DataFrame
df_out = pd.DataFrame(resultats)

# Calculs statistiques
mean_w0 = np.average(df_out["omega0"], weights=1/df_out["sigma_omega0"]**2)
sigma_mean = 1 / np.sqrt(np.sum(1/df_out["sigma_omega0"]**2))
std_exp = np.std(df_out["omega0"], ddof=1)

# Ajout ligne finale
df_out.loc[len(df_out)] = ["MOYENNE", mean_w0, sigma_mean]
df_out.loc[len(df_out)] = ["ECART_TYPE_EXP", std_exp, ""]

# Sauvegarde dans un CSV
output_name = "resultats_w0.csv"
df_out.to_csv(output_name, index=False)

print("\n========================================")
print(" Résultats ω0 exportés dans :", output_name)
print("========================================")

