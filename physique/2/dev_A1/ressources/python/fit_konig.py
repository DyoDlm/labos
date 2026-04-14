import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

frequencies = np.array([900, 1300, 1700, 2150, 2550, 3000, 3500, 4000, 4500, 5000])
lambdas = np.array([0.384, 0.270, 0.206, 0.162, 0.136, 0.114, 0.098, 0.086, 0.076, 0.068])

def linear_fit(x, a, b):
    return a * x + b

popt, pcov = curve_fit(linear_fit, 1/frequencies, lambdas)
a, b = popt
i_a, i_b = np.sqrt(np.diag(pcov))

print(f"(a) : {a:.3f} ± {i_a:.3f} m/s")
print(f"(b) : {b:.3f} ± {i_b:.7f} m")

# Tracé
plt.figure(figsize=(10, 6))
plt.scatter(1/frequencies, lambdas, color='red', label='Données expérimentales')
x_fit = np.linspace(min(1/frequencies), max(1/frequencies), 100)
plt.plot(x_fit, linear_fit_with_offset(x_fit, *popt),
         color='blue',
         label=f'Fit linéaire : $\lambda = ({a:.2f} \pm {i_a:.2f})\
                 \cdot (1/f) + ({b:.3f} \pm {i_b:.3f})$'
         )

plt.xlabel("$1/f$ \ s", fontsize=12)
plt.ylabel("$\lambda$ \ m", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("konig.png")

