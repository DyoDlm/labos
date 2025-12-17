import numpy as np
import matplotlib.pyplot as plt

# Données
frequencies = np.array([1.000, 2.000, 5.000, 10.000, 20.000])  # Hz
peaks_C = np.array([140.5, 143.5, 148.6, 150.5, 155.7])         # °C
uncertainties_C = np.array([1.606, 1.594, 1.601, 1.616, 1.518]) # °C

# Conversion en Kelvin
peaks_K = peaks_C + 273.15
inv_T = 1 / peaks_K
ln_f = np.log(frequencies)

# Propagation des incertitudes sur 1/T
# u(1/T) = u(T)/T² (u(T) en K)
uncertainties_K = uncertainties_C  # même valeur en K
u_inv_T = uncertainties_K / (peaks_K**2)

# Régression linéaire pondérée par les incertitudes
A = np.vstack([inv_T, np.ones(len(inv_T))]).T
m, c = np.linalg.lstsq(A, ln_f, rcond=None)[0]

# Matrice de covariance (pour les incertitudes sur m et c)
residuals = ln_f - (m*inv_T + c)
chi2 = np.sum((residuals/u_inv_T)**2)
dof = len(inv_T) - 2  # degrés de liberté
cov_matrix = np.linalg.inv(A.T @ np.diag(1/u_inv_T**2) @ A) * (chi2/dof)

# Incertitudes sur m et c
u_m = np.sqrt(cov_matrix[0, 0])
u_c = np.sqrt(cov_matrix[1, 1])

# Calcul de Ea et son incertitude
R = 8.314  # J/mol·K
Ea = -m * R
u_Ea = u_m * R  # propagation linéaire

# Tracé
plt.errorbar(inv_T, ln_f, xerr=u_inv_T, fmt='o', label='Données expérimentales')
plt.plot(inv_T, m*inv_T + c, 'r-',
         label=f'Ajustement linéaire\n$E_a = {Ea:.2f} \pm {u_Ea:.2f}$ J/mol')
plt.xlabel('1/T (K$^{-1}$)')
plt.ylabel('ln(f) (Hz)')
plt.legend()
plt.grid(True)
plt.savefig("my_arrenius.png")

print(f"Énergie d'activation : {Ea:.2f} ± {u_Ea:.2f} J/mol")
print(f"Ordonnée à l'origine : {c:.4f} ± {u_c:.4f} (ln(Hz))")

