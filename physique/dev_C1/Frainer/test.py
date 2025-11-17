import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_csv(file):
    """Load the CSV file and return a dataframe."""
    print(f"[INFO] Loading {file}")
    return pd.read_csv(file)


def find_two_maxima(df, min_separation=100):
    """
    Trouve les deux maxima du signal, séparés par un nombre minimal d'échantillons.
    - df : le dataframe contenant temps et signal
    - min_separation : nombre minimal d'échantillons entre les deux maxima
    """

    min_separation = 100
    t = df.iloc[:, 0].to_numpy()
    x = df.iloc[:, 1].to_numpy()

    # Trouver l'indice du premier maximum global
    idx1 = np.argmax(x)
    max1 = x[idx1]
    tmax1 = t[idx1]

    # Masquer une zone autour du premier maximum pour éviter son voisinage
    x_masked = x.copy()
    left = max(idx1 - min_separation, 0)
    right = min(idx1 + min_separation, len(x))
    x_masked[left:right] = -np.inf  # impossible d’être maximum

    # Trouver le deuxième maximum
    idx2 = np.argmax(x_masked)
    max2 = x[idx2]
    tmax2 = t[idx2]

    return (max1, max2), (tmax1, tmax2)


def pseudo_period(times):
    """Retourne la pseudo-période = |t2 - t1|."""
    return abs(times[1] - times[0])


# -------------------------
#        MAIN
# -------------------------

files = [
    "Mesure_0_1A.csv",
    "Mesure_0_2A.csv",
    "Mesure_0_3A.csv",
    "Mesure_0_4A.csv",
    "Mesure_0_5A.csv"
]

amperes = [0.1, 0.2, 0.3, 0.4, 0.5]
lambda_arr = []

for I, f in zip(amperes, files):

    df = load_csv(f)
    maxima, times = find_two_maxima(df, min_separation=80)

    print(f"\n[INFO] I = {I} A")
    print(f"Maxima = {maxima}")
    print(f"Temps  = {times}")

    lam = pseudo_period(times)
    print(f"Pseudo-période : {lam}")

    lambda_arr.append(lam)

# Plot
plt.figure()
plt.scatter(amperes, lambda_arr, color="blue")
plt.xlabel("I [A]")
plt.ylabel("Pseudo-période [s]")
plt.title("Pseudo-période en fonction du courant")
plt.grid(True)
plt.show()

