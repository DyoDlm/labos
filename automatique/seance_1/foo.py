import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Paramètres du système
K_bobines = 1e-3  # (N·m)/A
k = 2e-3          # (N·m)/rad
b = 5e-5          # (N·m)/(rad/s)
J_tot = 1e-4      # kg·m²
l = 5e-2          # m
g = 9.81          # m/s²
m = 1e-3          # kg (1 g)

# Perturbation : ajout d'une masse à t = 1 s
def perturbation(t):
    return m * g * l if t >= 1 else 0

# Équation différentielle du système en boucle fermée avec régulateur P
def system_ode(theta, t, Kp):
    dtheta_dt = theta[1]
    # Perturbation (couple dû à la masse)
    tau_perturbation = perturbation(t)
    # Couple des bobines : K_bobines * i, avec i = Kp * (-theta[0])
    tau_bobines = -K_bobines * Kp * theta[0]
    # Équation différentielle : J * d²θ/dt² = -kθ - b dθ/dt + τ_bobines + τ_perturbation
    d2theta_dt2 = (-k * theta[0] - b * theta[1] + tau_bobines + tau_perturbation) / J_tot
    return [dtheta_dt, d2theta_dt2]

# Temps de simulation
t = np.linspace(0, 30, 1000)

# Simulation pour Kp = 1
sol_Kp1 = odeint(system_ode, [0, 0], t, args=(1,))

# Simulation pour Kp = 100
sol_Kp100 = odeint(system_ode, [0, 0], t, args=(100,))

# Tracé des résultats
plt.figure(figsize=(12, 6))
plt.plot(t, sol_Kp1[:, 0], label='Kp = 1')
plt.plot(t, sol_Kp100[:, 0], label='Kp = 100')
plt.axvline(x=1, color='gray', linestyle='--', label='Ajout de la masse (t=1s)')
plt.xlabel('Temps (s)')
plt.ylabel('Position angulaire θ (rad)')
plt.title('Réponse du système pour Kp = 1 et Kp = 100')
plt.legend()
plt.grid(True)
plt.savefig("annexe.pdf")
