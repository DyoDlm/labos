import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

pi = np.pi

# =============================================================================
# DONNÉES EXPÉRIMENTALES
# =============================================================================

# --- a) P1 seul : tension vs angle de P1 ---
angle_P1 = np.arange(0, 360, 10)
U_P1 = np.array([8, 19, 36, 54, 80, 97, 112, 120, 122, 112, 87, 85, 63, 45,
                  24, 11, 3, 2, 7, 20, 36, 57, 81, 98, 114, 123, 124, 118,
                  102, 89, 66, 42, 26, 12, 7, 4])
U_max_P1, U_min_P1 = 124, 2   # mV

# --- b) P2 seul (P1 fixé à 260°) : tension vs angle de P2 ---
angle_P2b = np.arange(0, 360, 10)
U_P2b = np.array([61, 45, 30, 16, 6, 2, 2, 8, 18, 33, 50, 63, 75, 85, 89,
                   89, 83, 72, 60, 44, 29, 16, 8, 3, 3, 8, 19, 31, 47, 63,
                   76, 84, 89, 89, 83, 73])
U_max_P2b, U_min_P2b = 89, 2   # mV

# --- d) Lame demi-onde (P1=260°, P2 sur minimum) : tension vs angle lame λ/2 ---
angle_lambda2 = np.arange(0, 360, 10)
U_lambda2 = np.array([16, 2, 14, 47, 84, 104, 106, 86, 47, 15, 2, 13, 46,
                       83, 107, 107, 84, 48, 14, 2, 14, 45, 84, 107, 106,
                       83, 46, 15, 2, 14, 46, 83, 107, 105, 82, 47])

# --- e) Lame quart d'onde (P1=260°, P2 réoptimisé) : tension vs angle P2 ---
angle_P2e = np.arange(0, 360, 10)
U_lambda4 = np.array([49, 50, 52, 54, 57, 60, 61, 62, 62, 60, 58, 56, 53,
                       51, 49, 47, 47, 48, 50, 52, 55, 58, 60, 61, 62, 62,
                       61, 59, 57, 55, 53, 50, 49, 48, 48, 48])
U_max_lambda4 = 62   # mV (corrigé : max dans le tableau est 62)

# =============================================================================
# FONCTIONS D'ANALYSE
# =============================================================================

def fit_malus(angle_deg, A, offset, phi):
    """Loi de Malus : I = offset + A * cos²(θ - φ)"""
    theta = np.radians(angle_deg)
    phi_r = np.radians(phi)
    return offset + A * np.cos(theta - phi_r)**2

def fit_demi_onde(angle_deg, A, offset, phi):
    """Lame λ/2 : période de 90° → sin²(2*(θ-φ))"""
    theta = np.radians(angle_deg)
    phi_r = np.radians(phi)
    return offset + A * np.sin(2*(theta - phi_r))**2

def energie_totale(U_array, delta_theta_deg=10):
    """Intégrale trapèze normalisée (proportionnelle à l'énergie angulaire)"""
    return np.trapezoid(U_array, dx=delta_theta_deg)

# =============================================================================
# ANALYSE NUMÉRIQUE
# =============================================================================
rapport_extinction_P1 = U_max_P1 / U_min_P1
rapport_extinction_P2 = U_max_P2b / U_min_P2b
E_P1  = energie_totale(U_P1)
E_P2b = energie_totale(U_P2b)

# Fits
p0_malus = [60, 30, 80]
popt_P1,  _ = curve_fit(fit_malus, angle_P1,  U_P1,  p0=p0_malus, maxfev=10000)
popt_P2b, _ = curve_fit(fit_malus, angle_P2b, U_P2b, p0=p0_malus, maxfev=10000)
popt_lbd2, _ = curve_fit(fit_demi_onde, angle_lambda2, U_lambda2,
                          p0=[50, 5, 10], maxfev=10000)

angle_dense = np.linspace(0, 360, 1000)

# =============================================================================
# AFFICHAGE DES RÉSULTATS
# =============================================================================
print("=" * 60)
print("a) ÉTAT DE POLARISATION DE LA SOURCE")
print("=" * 60)
print(f"   U_max = {U_max_P1} mV,  U_min = {U_min_P1} mV")
print(f"   Rapport d'extinction = {rapport_extinction_P1:.1f}  ({10*np.log10(rapport_extinction_P1):.1f} dB)")

print("\n" + "=" * 60)
print("b) POLARISATION AVEC P1 + P2")
print("=" * 60)
print(f"   U_max = {U_max_P2b} mV,  U_min = {U_min_P2b} mV")
print(f"   Rapport d'extinction = {rapport_extinction_P2:.1f}  ({10*np.log10(rapport_extinction_P2):.1f} dB)")

print("\n" + "=" * 60)
print("c) ÉNERGIE TOTALE (intégrale sur 360°)")
print("=" * 60)
print(f"   P1 seul  : {E_P1:.0f}  mV·°")
print(f"   P1 + P2  : {E_P2b:.0f}  mV·°")
print(f"   Rapport  : {E_P2b/E_P1:.3f} (attendu ≈ 0.5)")

# =============================================================================
# PLOTS SÉPARÉS (4 figures distinctes)
# =============================================================================

# --- PLOT a) P1 seul ---
plt.figure(figsize=(8, 5))
plt.scatter(angle_P1, U_P1, color='royalblue', s=25, label="Expérience", zorder=5)
plt.plot(angle_dense, fit_malus(angle_dense, *popt_P1), 'r--',
         label=f"Fit cos² (φ={popt_P1[2]:.0f}°)", linewidth=1.8)
plt.axhline(U_max_P1, color='green', linestyle=':', alpha=0.7, label=f"Max={U_max_P1} mV")
plt.axhline(U_min_P1, color='orange', linestyle=':', alpha=0.7, label=f"Min={U_min_P1} mV")
plt.title(f"a) P1 seul – Extinction = {rapport_extinction_P1:.0f} ({10*np.log10(rapport_extinction_P1):.1f} dB)")
plt.xlabel("Angle P1 / °")
plt.ylabel("U (mV)")
plt.xlim(0, 350)
plt.grid(alpha=0.4)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("polarisation_a_P1_seul.png", dpi=200)
plt.close()

# --- PLOT b) P1 + P2 ---
plt.figure(figsize=(8, 5))
plt.scatter(angle_P2b, U_P2b, color='royalblue', s=25, label="Expérience", zorder=5)
plt.plot(angle_dense, fit_malus(angle_dense, *popt_P2b), 'r--',
         label=f"Fit cos² (φ={popt_P2b[2]:.0f}°)", linewidth=1.8)
plt.axhline(U_max_P2b, color='green', linestyle=':', alpha=0.7, label=f"Max={U_max_P2b} mV")
plt.axhline(U_min_P2b, color='orange', linestyle=':', alpha=0.7, label=f"Min={U_min_P2b} mV")
plt.title(f"b) P1 + P2 – Extinction = {rapport_extinction_P2:.0f} ({10*np.log10(rapport_extinction_P2):.1f} dB)")
plt.xlabel("Angle P2 / °")
plt.ylabel("U (mV)")
plt.xlim(0, 350)
plt.grid(alpha=0.4)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("polarisation_b_P1_P2.png", dpi=200)
plt.close()

# --- PLOT d) Lame demi-onde ---
plt.figure(figsize=(8, 5))
plt.scatter(angle_lambda2, U_lambda2, color='royalblue', s=25, label="Expérience", zorder=5)
plt.plot(angle_dense, fit_demi_onde(angle_dense, *popt_lbd2), 'r--',
         label=f"Fit sin²(2θ) (φ={popt_lbd2[2]:.0f}°)", linewidth=1.8)
plt.plot(angle_dense, fit_malus(angle_dense, *popt_P2b), 'g:',
         linewidth=1.4, label="P1+P2 (ref. b)", alpha=0.7)
plt.title("d) Lame λ/2 – Période 90° (rotation de polarisation)")
plt.xlabel("Angle lame λ/2 / °")
plt.ylabel("U (mV)")
plt.xlim(0, 350)
plt.grid(alpha=0.4)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("polarisation_d_lame_demi_onde.png", dpi=200)
plt.close()

# --- PLOT e) Lame quart d'onde ---
plt.figure(figsize=(8, 5))
plt.scatter(angle_P2e, U_lambda4, color='royalblue', s=25, label="Expérience", zorder=5)
popt_lbd4, _ = curve_fit(
    lambda x, A, off, phi: off + A*np.cos(np.radians(x) - np.radians(phi)),
    angle_P2e, U_lambda4, p0=[6, 55, 0], maxfev=10000)
plt.plot(angle_dense,
         popt_lbd4[1] + popt_lbd4[0]*np.cos(np.radians(angle_dense) - np.radians(popt_lbd4[2])),
         'r--', label=f"Fit (amplitude={popt_lbd4[0]:.1f} mV)", linewidth=1.8)
plt.axhline(U_max_lambda4, color='green', linestyle=':', alpha=0.7, label=f"Max={U_max_lambda4} mV")
plt.title("e) Lame λ/4 – Polarisation quasi-circulaire")
plt.xlabel("Angle P2 / °")
plt.ylabel("U (mV)")
plt.xlim(0, 350)
plt.grid(alpha=0.4)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("polarisation_e_lame_quart_onde.png", dpi=200)
plt.close()

# =============================================================================
# RÉSUMÉ FINAL
# =============================================================================
print("\n" + "=" * 60)
print("d) LAME DEMI-ONDE")
print("=" * 60)
print(f"   Période observée ≈ 90° (rotation de 2*θ_lame)")
print(f"   → La lame λ/2 tourne la polarisation de 2α")
print(f"   → Permet de repasser du min au max par rotation de 45°")

print("\n" + "=" * 60)
print("e) LAME QUART D'ONDE")
print("=" * 60)
print(f"   U_max = {max(U_lambda4)} mV,  U_min = {min(U_lambda4)} mV")
print(f"   Variation max-min = {max(U_lambda4)-min(U_lambda4)} mV  (vs {U_max_P2b-U_min_P2b} mV sans lame)")
print(f"   → Polarisation quasi-circulaire : intensité quasi indépendante de l'angle de P2")
print(f"   → La lame λ/4 convertit polarisation linéaire → circulaire")
