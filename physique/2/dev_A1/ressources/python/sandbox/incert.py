import numpy as np
import matplotlib.pyplot as plt

# Données expérimentales
frequencies = np.array([14.8, 18.0, 20.9, 31.0, 40.6, 49.6, 61.1, 70.1, 79.2])
D = np.array([0.040, 0.053, 0.048, 0.047, 0.060, 0.060, 0.045, 0.049, 0.050])
N = np.array([2, 3, 3, 4, 5, 6, 5, 6, 7])
delta_D = 0.001
delta_N = 0.5

# Facteur de grossissement
g = 1.67
delta_g = 0.15

# Calcul de lambda et ses incertitudes
lambda_vals = D / N
delta_lambda = lambda_vals * np.sqrt((delta_D/D)**2 + (delta_N/N)**2)

# Calcul de lambda_c et ses incertitudes
lambda_c = lambda_vals / g
delta_lambda_c = lambda_c * np.sqrt((delta_lambda/lambda_vals)**2 + (delta_g/g)**2)

# Tracé de Δλ_c en fonction de la fréquence
plt.figure(figsize=(10, 6))
plt.errorbar(frequencies, delta_lambda_c, yerr=0.00005, fmt='o', capsize=5,
             label='Incertitudes sur $\lambda_c$')
plt.xlabel('f \\ Hz')
plt.ylabel('$\Delta \lambda_c$ \\ m')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('incertitudes_lambda_c.png', dpi=300, bbox_inches='tight')
