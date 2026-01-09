import numpy as np
import pandas as pd

# Impédance caractéristique du câble
Z0 = 55.3  # ohms

# Données expérimentales
R = np.array([5, 10, 15, 20, 25, 30, 35, 40, 100, 500, 1500, 2000, 2500])
VG = np.array([10.65, 9.65, 9.65, 8.84, 9.05, 8.19, 8.44, 8.04,
               7.84, 8.24, 7.64, 8.04, 7.84])
VC = np.array([9.73, 7.48, 8.44, 6.43, 7.56, 5.95, 7.08, 5.39,
               6.27, 8.68, 9.33, 9.49, 9.43])

# Calcul du coefficient de réflexion
Gamma = (R - Z0) / (R + Z0)

# Mise en forme des résultats
results = pd.DataFrame({
    "R (ohms)": R,
    "V_G_pp (V)": VG,
    "V_C_pp (V)": VC,
    "Gamma": Gamma
})

# Affichage
print(results.to_string(index=False))

