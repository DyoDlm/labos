import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filename="Mesure_0_9A.csv"

# --- 1) Charger le fichier CSV ---
# Le CSV doit contenir deux colonnes : t, theta
# Exemple d’appel : python script.py
data = np.loadtxt(filename, delimiter=",", skiprows=1)
t = data[:, 0]
theta = data[:, 1]

# --- 2) Modèle d'oscillation amortie ---
def oscillation_amortie(t, A, gamma, omega, phi):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

# --- 3) Ajustement des paramètres ---
# Estimations initiales (à affiner si nécessaire)
A0 = theta.max()
gamma0 = 0.1
omega0 = 2*np.pi
phi0 = 0

p0 = [A0, gamma0, omega0, phi0]

params, cov = curve_fit(oscillation_amortie, t, theta, p0=p0)

A_fit, gamma_fit, omega_fit, phi_fit = params

print("Paramètres ajustés :")
print(f"A      = {A_fit}")
print(f"gamma  = {gamma_fit}")
print(f"omega  = {omega_fit}")
print(f"phi    = {phi_fit}")

# --- 4) Tracer les données et la courbe ---
t_fit = np.linspace(t.min(), t.max(), 2000)
theta_fit = oscillation_amortie(t_fit, *params)

plt.figure(figsize=(10,5))
plt.scatter(t, theta, s=15, label="Données expérimentales")
plt.plot(t_fit, theta_fit, 'r-', linewidth=2, label="Ajustement (curve_fit)")

plt.xlabel("Temps t (s)")
plt.ylabel("Angle θ (rad)")
plt.legend()
plt.grid(True)
plt.savefig("graph_0_9A.png")

#plt.show()

