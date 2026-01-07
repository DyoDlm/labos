import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# =====================
# Données expérimentales
# =====================
theta_deg = np.array([90, 75, 60, 45, 30, 15, 0, -15, -30, -45, -60, -75, -90])
U = np.array([0.13, 0.18, 0.28, 0.44, 0.91, 1.95, 2.5,
              1.45, 0.54, 0.16, 0.08, 0.06, 0.05])

# Incertitude sur la tension (exemple : oscilloscope)
dU = 0.05 * np.ones_like(U)  # ±50 mV (à adapter)

# Conversion en radians
theta_rad = np.deg2rad(theta_deg)

# =====================
# Modèle de régression
# =====================
def U_model(theta, U0, n):
    return U0 * np.abs(np.cos(theta))**n

# =====================
# Ajustement avec incertitudes
# =====================
popt, pcov = curve_fit(
    U_model,
    theta_rad,
    U,
    sigma=dU,
    absolute_sigma=True,
    p0=[2.5, 2]  # valeurs initiales
)

U0_fit, n_fit = popt
dU0_fit, dn_fit = np.sqrt(np.diag(pcov))

# =====================
# Affichage des résultats
# =====================
print("Résultats de la régression :")
print(f"U0 = {U0_fit:.2f} ± {dU0_fit:.2f} V")
print(f"n  = {n_fit:.2f} ± {dn_fit:.2f}")

# =====================
# Tracé polaire
# =====================
theta_plot = np.linspace(-np.pi/2, np.pi/2, 400)
U_fit = U_model(theta_plot, U0_fit, n_fit)

plt.figure(figsize=(6, 6))
ax = plt.subplot(111, projection="polar")

# Points expérimentaux
ax.errorbar(theta_rad, U, yerr=dU, fmt='o', label="Mesures", capsize=3)

# Courbe ajustée
#ax.plot(theta_plot, U_fit, label="Régression $U_0|\cos(\\theta)|^n$")

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_thetalim(-np.pi/2, np.pi/2)


plt.savefig("angle.png")
plt.show()

