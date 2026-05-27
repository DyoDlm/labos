import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, differential_evolution

pi = np.pi

Upp = [261,235,181,177,169,193,197,212,240,269,294,323,342,356,354,335,308,271,229,201,181,191,205,223,263,297,324,360,382,406,402,386,358,316,277,241,230,239,255,287,326]
pos = np.linspace(42.7, 38.7, 41)

x0 = np.mean(pos)

def fit_function(x, lambda_, E0, offset, beta, phi):
    """
    offset + beta*(x-x0) : ligne de base qui varie linéairement (offset décroît avec x)
    E0 * sin(k*x + phi)  : oscillation d'amplitude constante
    """
    k = 2 * pi / lambda_
    return (offset + beta * (x - x0)) + E0 * np.sin(k * x + phi)

def residuals(params):
    try:
        return np.sum((fit_function(pos, *params) - Upp)**2)
    except:
        return 1e18

bounds = [
    (1.5, 2.5),    # lambda_
    (50, 200),     # E0
    (150, 400),    # offset (valeur en x0)
    (-100, 100),   # beta  (pente de l'offset en mV/cm)
    (-pi, pi),     # phi
]

result = differential_evolution(residuals, bounds, seed=42, maxiter=5000, tol=1e-12, polish=True)
p0 = result.x
print("Paramètres initiaux (evol. diff.) :", p0)

popt, pcov = curve_fit(fit_function, pos, Upp, p0=p0, maxfev=50000)
perr = np.sqrt(np.diag(pcov))

lambda_opt, E0_opt, offset_opt, beta_opt, phi_opt = popt
print(f"\nλ       = {lambda_opt:.4f} ± {perr[0]:.4f} cm")
print(f"E0      = {E0_opt:.2f}  ± {perr[1]:.2f} mV")
print(f"offset  = {offset_opt:.2f}  ± {perr[2]:.2f} mV  (en x = x0 = {x0:.2f} cm)")
print(f"beta    = {beta_opt:.3f}  ± {perr[3]:.3f} mV/cm  (pente de l'offset)")
print(f"phi     = {phi_opt:.4f} ± {perr[4]:.4f} rad")

residual_rms = np.sqrt(np.mean((fit_function(pos, *popt) - Upp)**2))
print(f"\nRMS résidus = {residual_rms:.2f} mV")

x_dense = np.linspace(pos.min(), pos.max(), 500)
v_fit = fit_function(x_dense, *popt)
baseline = offset_opt + beta_opt * (x_dense - x0)


plt.scatter(pos, Upp, label="Expérience", color='steelblue', zorder=5)
plt.plot(x_dense, v_fit, label=f"Fit expérimental", color='red', linewidth=2)
plt.plot(x_dense, baseline, label=f"Offset linéaire", color='orange', linestyle='--', linewidth=1.5)
plt.grid()
plt.ylabel(r"$U_{pp}$ $\pm$ 4 mV)")
plt.xlabel(r"x $\pm$ 0.1 cm")
plt.legend()

plt.tight_layout()
plt.savefig("res3.png", dpi=150)
print("Saved res3.png")
