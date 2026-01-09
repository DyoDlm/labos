import numpy as np
import matplotlib.pyplot as plt

# Données
R = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 100, 500, 1500, 2000, 2500])
Gamma = np.array([
    -0.900,
    -0.834,
    -0.694,
    -0.573,
    -0.469,
    -0.377,
    -0.297,
    -0.225,
    -0.161,
    -0.096,
     0.288,
     0.801,
     0.929,
     0.946,
     0.957
])

# Tracé
plt.figure(figsize=(8,5))
plt.scatter(R, Gamma)
plt.axhline(0, color='black', linewidth=0.8)

plt.xlabel(r"$Z_L$ \ $\omega$")
plt.ylabel(r"$rho")
plt.grid(True)

plt.savefig("rho")
