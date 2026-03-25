import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

pi = np.pi
f = 50000  # Hz
w = 2 * pi * f
E0 = 5 
x_offset = 0

def v_theorique(x, E0, k):
    t = 1 
    return 2 * E0 * np.sin(k * x)


def fit_function(x, E0, k):
    return v_theorique(x, E0, k)
Upp = [261,235,181,177,169,193,197,212,240,269,294,323,342,356,354,335,308,271,229,201,181,191,205,223,263,297,324,360,382,406,402,386,358,316,277,241,230,239,255,287,326]
Ueff = [165,143,104,101,97 ,110,118,130,146,162,179,198,207,222,222,214,190,171,139,121,110,111,121,132,154,178,197,220,230,248,246,240,220,197,170,154,144,149,158,177,204]
#pos = np.array[42.7,42.6,42.5,42,4,42,3,42,2,42,1,42,41,9,41,8,41,7,41,6,41,5,41,4,41,3,41,2,41,1,41,40,9,40,8,40,7,40,6,40,5,40,4,40,3,40,2,40,1,40,39,9,39,8,39,7,39,6,39,5,39,4,39,3,39,2,39,1,39,38,9,38,8,38,7]
pos = np.linspace(42.7, 38.7, 41)


popt, pcov = curve_fit(fit_function, pos, Upp, p0=[1, 0.1])

v_fit = fit_function(pos, *popt)

plt.scatter(pos, Upp, label="Valeurs expérimentales", color='blue')
plt.plot(pos, v_fit + 300, label="Fit théorique", color='red')
plt.grid()
plt.xlabel("Position (cm)")
plt.ylabel(r"$\mathrm{U_{pp}} \ (V)$")
plt.legend()
plt.savefig("res.png")
plt.show()

# Résultat
k_opt, E0_opt = popt
lambda_opt = 2 * pi / k_opt
print(f"La longueur d'onde ajustée est : {lambda_opt:.4f} cm")
print(f"E0 ajusté : {E0_opt:.4f}")
