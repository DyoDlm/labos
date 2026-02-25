import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

#   define raw data
exp = "Decharge de condenstateur"
a_names = ["egale_0.csv", "mgra_10_.csv", "mgra_50.csv", "pgra_10.csv", "pgra_35.csv"]
a_is = ["Amortissement faible", "Amortissement fort", "Amortissement critique"]


exp = "Mesure des oscillation d'une bobine de cuivre avec inductances variables"
e_names = ["e_aff.csv", "e_aci.csv", "e_air.csv", "e_alu.csv"]
e_is = ["Oscillation acier feuillete", "Oscillation acier", "Oscillation air", "Oscillation aluminium"]


exp = "Mesures de comparaison pour la bobine d'inductance"
f_names = ["f_aci.csv", "f_aff.csv", "f_air.csv", "f_alu.csv"]
f_is = []


experiences = [a_names,e_names,f_names]
exp_names = ["a", "exp_e", "exp_f"]

#   it returns the new file name
#   somethings to do 
def plot(df, exp: str, name: str) -> str:
    tab = name.split('/')
    tab2 = tab[0].split(".csv")
    fileName = tab2[0] + "_plot"
    print(f"New file name : {fileName}")

    x = pd.to_numeric(df[df.columns[0]], errors='coerce')
    y = pd.to_numeric(df[df.columns[1]], errors='coerce')

    plt.grid()
    if exp == "a":
        #   afficher les valeurs de resistance sur le graph
        plt.title("Decharge d'un condensateur : Uc(t)")
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")
    elif exp == "e":
        #   determiner les parametres recherches
        plt.title("O")
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")
        facteur_amortissement = 0
        pseudo_periode = 0
    elif exp == "f":
        #   comparer avec valeurs theoriques
        plt.title("")
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")
        

    plt.plot(x, y)
    plt.show()
    plt.savefig(fileName)
    return fileName
def underdamped(t, A, alpha, omega, phi):
    return A * np.exp(-alpha * t) * np.cos(omega * t + phi)

def critical(t, A, B, alpha):
    return (A + B * t) * np.exp(-alpha * t)

def overdamped(t, A, alpha, B, beta):
    return A * np.exp(-alpha * t) + B * np.exp(-beta * t)

def smart_plot(df, exp: str, name: str) -> str:
    fileName = name.split(".csv")[0] + "_plot"
    print(f"New file name : {fileName}")

# Conversion en numérique
    x = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    y = pd.to_numeric(df.iloc[:, 1], errors='coerce')

# Suppression des NaN et inf
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask].values
    y = y[mask].values

    plt.figure(figsize=(8, 5))
    plt.grid()

    # Détection des oscillations
    peaks, _ = find_peaks(y, prominence=np.ptp(y) * 0.05)

    if len(peaks) > 2:
        # Régime faiblement amorti
        popt, _ = curve_fit(
            underdamped, x, y,
            p0=[max(y), 1, 10, 0]
        )
        y_fit = underdamped(x, *popt)

        A, alpha, omega, phi = popt
        equation = (
            r"$U(t)=%.2f\,e^{-%.2f t}\cos(%.2f t + %.2f)$"
            % (A, alpha, omega, phi)
        )
        regime = "Faiblement amorti"

    else:
        # Tentative critique
        try:
            popt, _ = curve_fit(
                critical, x, y,
                p0=[max(y), -1, 1]
            )
            y_fit = critical(x, *popt)

            A, B, alpha = popt
            equation = (
                r"$U(t)=(%.2f + %.2f t)e^{-%.2f t}$"
                % (A, B, alpha)
            )
            regime = "Critique"

        except RuntimeError:
            # Fortement amorti
            popt, _ = curve_fit(
                overdamped, x, y,
                p0=[max(y), -max(y), 1, 5]
            )
            y_fit = overdamped(x, *popt)

            A, B, alpha1, alpha2 = popt
            equation = (
                r"$U(t)=%.2f e^{-%.2f t}+%.2f e^{-%.2f t}$"
                % (A, alpha1, B, alpha2)
            )
            regime = "Fortement amorti"

    # Tracés
    plt.plot(x, y, 'o', label="Données expérimentales")
    plt.plot(x, y_fit, '-', label="Fit")

    plt.title(f"Régime détecté : {regime}")
    plt.xlabel("Temps [s]")
    plt.ylabel("Tension [V]")

    # Affichage de l'équation sur le graphique
    plt.text(
        0.05, 0.95,
        equation,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    plt.legend()
    plt.savefig(fileName)
    plt.show()

    return fileName



iteration = 0
for exp in experiences:
    for file in exp:
        dir = exp_names[iteration] + "/"
        df = pd.read_csv(dir + file)
#        df = pd.read_excel(dir + file, engine=".ods")
        new = smart_plot(df, exp_names[iteration], file)
        print(f"New file created : {new} !")
    iteration += 1

