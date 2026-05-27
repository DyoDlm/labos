import numpy as np
import matplotlib.pyplot as plt

PHI = 60

def sellmeier_sio2(wavelength):
    l2 = wavelength ** 2
    n_sq = 1 + (0.6961663 * l2 / (l2 - 0.0684043**2)) + \
               (0.4079426 * l2 / (l2 - 0.1162414**2)) + \
               (0.8974794 * l2 / (l2 - 9.896161**2))
    return np.sqrt(n_sq)

def sellmeier_toluene(wavelength):
    l2 = wavelength ** 2
    n_sq = 1 + (1.17477 * l2 / (l2 - 0.01825))
    return np.sqrt(n_sq)

def cauchy_ethyl_cinnamate(wavelength):
    return 1.5269 + (7.43e-3 / wavelength**2) + (1.16e-3 / wavelength**4)

def n_mes(D):
    return np.sin((PHI + D) / 2) / np.sin(PHI/2)

wavelengths = np.linspace(0.3, 1, 600)  


# INDICES
n_sio2 = sellmeier_sio2(wavelengths)
n_toluene = sellmeier_toluene(wavelengths)
n_ethyl_cinnamate = cauchy_ethyl_cinnamate(wavelengths)


# MESURES
#   FLINT (SIO2)
D_flint = [1,2,3]
L_flint = [405, 532, 650]
n_mes_flint = n_mes(D_sio2)
#   CROWN (SIO2)
D_crown = [1,2,3]
L_crown = [405, 532, 650]
n_mes_crown = n_mes(D_sio2)
#   TOLUENE
D_toluene = [1,2,3]
L_toluene = [405,532,650]
n_mes_sio2 = n_mes(D_toluene)
#   ETHYL
D_ethyl = [1,2,3]
L_ethyl = [405,532,650]
n_mes_sio2 = n_mes(D_ethyl)


#   FIT TH.
popt_flint, pcov_flint = curve_fit(n_mes(D_flint), wavelengths)
popt_crown, pcov_crown = curve_fit(n_mes(D_crown), wavelengths)
popt_toluene, pcov_toluene= curve_fit(n_mes(D_toluen), wavelengths)
popt_ethyl, pcov_ethyl = curve_fit(n_mes(D_ethyl), wavelengths)


plt.figure(figsize=(10, 6))

#   PLOT MES
plt.scatter(n_mes_sio2, L_sio2)
plt.scatter(n_mes_toluene, L_toluene)
plt.scatter(n_mes_ethyl, L_ethyl)

#   PLOT SELLMEIER
plt.plot(wavelengths, n_sio2, label="SiO₂ (Malitson)", color="blue")
plt.plot(wavelengths, n_toluene, label="Toluène (Kedenburg)", color="green")
plt.plot(wavelengths, n_ethyl_cinnamate, label="Cinnamate d'éthyle (Krauter)", color="red", linestyle="--")

#   PLOT FIT.


plt.xlim(0.2, 1.0)
plt.ylim(1.4, 1.0)
plt.xlabel("Longueur d'onde (µm)")
plt.ylabel("Indice de réfraction (n)")
plt.title("Indice de réfraction en fonction de la longueur d'onde")
plt.legend()
plt.grid(True)
plt.savefig("sellmeier.png")
