import latexify

# Chemin vers le fichier TXT

def plot(that, name):
    file_path = that   # à adapter
 
    filename = "plot_" + that
# Lecture :
# - séparateur = virgule
# - on ignore la ligne des unités
    df = pd.read_csv(
        file_path,
        sep=",",
        skiprows=[1]
    )

# Conversion en numérique
    df = df.apply(pd.to_numeric, errors="coerce")

# Extraction des colonnes
    t = df["x-axis"]
    y1 = df["1"]
    y2 = df["2"]

    max1 = y1.max()
    max2 = y2.max()
    min1 = y1.min()
    min2 = y2.min()

    time = max1 - max2
    amplitude1 = max1 - min1
    amplitude2 = max2 - min2

    print("----------------------")
    print(f"Resistances are : {file_path}")
    print(f"max generateur 1 : {max1}")
    print(f"max cable 2 : {max2}")
    print(f"min generateur 1 : {min1}")
    print(f"min cable 2 : {min2}")
    print(f"amplitude generateur1 : {amplitude1}")
    print(f"amplitude cable2 : {amplitude2}")
    print(f"Time between : {time}")
    print("----------------------")


# Plot
    plt.figure()
    plt.plot(t, y1, label="CH 1 (generateur)")
    plt.plot(t, y2, label="CH 2 (cable coaxial)")

    plt.xlabel(r"Temps t \ s")
    plt.ylabel("Tension U \ V")
    plt.legend()
    plt.grid(True)
    plt.savefig(name)
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analyze_csv(file_path, name,
                t_inc=(0e-6, 0.25e-6),
                t_trans=(0.45e-6, 0.75e-6),
                t_ref=(1.0e-6, 1.4e-6)):

    # Lecture du CSV
    df = pd.read_csv(file_path, sep=",", skiprows=[1])
    df = df.apply(pd.to_numeric, errors="coerce")

    t = df["x-axis"].values
    ch1 = df["1"].values   # générateur
    ch2 = df["2"].values   # câble

    # Fenêtres temporelles
    inc = (t > t_inc[0]) & (t < t_inc[1])
    trans = (t > t_trans[0]) & (t < t_trans[1])
    ref = (t > t_ref[0]) & (t < t_ref[1])

    # Amplitudes
    Ui = (ch1[inc].max() - ch1[inc].min()) / 2
    Ut = (ch2[trans].max() - ch2[trans].min()) / 2
    Ur = (ch1[ref].max() - ch1[ref].min()) / 2

    # Coefficients
    rho = Ur / Ui
    tau = Ut / Ui

    # Affichage
    print("================================")
    print(f"Résistance : {name}")
    print(f"Ui (incident)    = {Ui:.3f} V")
    print(f"Ur (réfléchie)   = {Ur:.3f} V")
    print(f"Ut (transmise)   = {Ut:.3f} V")
    print(f"ρ = Ur/Ui        = {rho:.3f}")
    print(f"τ = Ut/Ui        = {tau:.3f}")
    print(f"1 + ρ            = {1 + rho:.3f}")
    print("================================")

    # Plot
    plt.figure(figsize=(7,4))
    plt.plot(t, ch1, label="CH1 – Générateur")
    plt.plot(t, ch2, label="CH2 – Câble")

    # Fenêtres visibles
    plt.axvspan(*t_inc, color="green", alpha=0.2, label="Incident")
    plt.axvspan(*t_trans, color="orange", alpha=0.2, label="Transmis")
    plt.axvspan(*t_ref, color="red", alpha=0.2, label="Réfléchi")

    plt.xlabel("t \ s")
    plt.ylabel("U \ V")
    plt.legend()
    plt.grid(True)
    plt.title(name)
#    plt.savefig(name)

    #plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_extrema(file_path, name):

    # Intervalles (en secondes)
    t_inc   = (0.00e-6, 0.25e-6)
    t_trans = (0.50e-6, 0.75e-6)
    t_ref   = (1.05e-6, 1.40e-6)

    #t = df["x-axis"]
    #y1 = df["1"]
    #y2 = df["2"]
    df = pd.read_csv(
        file_path,
        sep=",",
        skiprows=[1]
    )

# Conversion en numérique
    df = df.apply(pd.to_numeric, errors="coerce")

    t = df["x-axis"].values
    ch1 = df["1"].values   # Générateur
    ch2 = df["2"].values   # Câble

    # Suppression offset DC (avant impulsion)
 #   baseline = t < -0.05e-6
    #ch1 -= np.mean(ch1[baseline])
#    ch2 -= np.mean(ch2[baseline])

    # Fenêtres
    inc = (t > t_inc[0]) & (t < t_inc[1])
    trans = (t > t_trans[0]) & (t < t_trans[1])
    ref = (t > t_ref[0]) & (t < t_ref[1])

    print("================================")
    print(name)

    print("Incident (CH1)")
    print(f"  max = {ch1[inc].max():.3f} V")
    print(f"  min = {ch1[inc].min():.3f} V")

    print("Transmis (CH2)")
    print(f"  max = {ch2[trans].max():.3f} V")
    print(f"  min = {ch2[trans].min():.3f} V")

    print("Réfléchi (CH1)")
    print(f"  max = {ch1[ref].max():.3f} V")
    print(f"  min = {ch1[ref].min():.3f} V")

    print("================================")

    # Plot (optionnel mais utile pour vérification)
    plt.figure(figsize=(7,4))
    plt.plot(t, ch1, label="CH1 – Générateur")
    plt.plot(t, ch2, label="CH2 – Câble")

    plt.axvspan(*t_inc, color="green", alpha=0.25, label="Incident")
    plt.axvspan(*t_trans, color="orange", alpha=0.25, label="Transmis")
    plt.axvspan(*t_ref, color="red", alpha=0.25, label="Réfléchi")

    plt.xlabel("t \ s")
    plt.ylabel("U \ V")
    plt.legend()
    plt.grid(True)
    plt.savefig(name)

resistances = ["s1500_14.csv", "s2500_15.csv", "s40pe_11.csv","s15pe_6.csv", "s25pe_8.csv", "s500e_13.csv", "s100e_12.csv", "s2000_16.csv", "s30pe_9.csv", "s5ope_4.csv", "s10pe_5.csv","s20pe_7.csv", "s35pe_10.csv"]

names = ["r1500", "r2500", "r40", "r15", "r25", "r500", "r100", "r2000", "r30", "r5", "r10", "r20", "r35"]

#resistances = ["whatisdat/scope_0.csv"]

c = 0
for i in resistances:
    print(i)
    
    extract_extrema(i, names[c])#plot(i, names[c])
    c += 1
