import matplotlib.pyplot as plt
import pandas as pd


a_names = ["egale_0.csv", "mgra_10_.csv", "mgra_50.csv", "pgra_10.csv", "pgra_35.csv"]
e_names = ["e_aff.csv", "e_aci.csv", "e_air.csv", "e_alu.csv"]
f_names = ["f_aci.csv", "f_aff.csv", "f_air.csv", "f_alu.csv"]

experiences = [a_names,e_names,f_names]
exp_names = ["a", "exp_e", "exp_f"]

def plot(df, exp: str, name: str) -> str:
    tab = name.split('/')
    tab2 = tab[0].split(".csv")
    fileName = tab2[0] + "_plot"
    print(f"New file name : {fileName}")

    x = df.iloc[:,0]
    y = df.iloc[:,1]
    plt.grid()
    if exp == "a":
        plt.title("")
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")
    elif exp == "e":
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")
    elif exp == "f":
        plt.ylabel("Volt +/- ? [V]")
        plt.xlabel("Time +/- ? [s]")


    plt.plot(y, x)
    plt.show()
#    plt.save(fileName)
    return fileName

iteration = 0
for exp in experiences:
    for file in exp:
        dir = exp_names[iteration] + "/"
        df = pd.read_csv(dir + file)
        new = plot(df, exp_names[iteration], file)
        print(f"New file created : {new} !")
    iteration += 1

exit(1)















a_names = ["egale_0.csv", "mgra_10_.csv", "mgra_50.csv", "pgra_10.csv", "pgra_35.csv"]
e_names = ["e_aff.csv", "e_aci.csv", "e_air.csv", "e_alu.csv"]
f_names = ["f_aci.csv", "f_aff.csv", "f_air.csv", "f_alu.csv"]

experiences = [a_names,e_names,f_names]
exp_names = ["a", "exp_e", "exp_f"]

def plot(df, exp: str, x_label: str, y_label: str) -> str:
    tab = exp.split('/')
    tab2 = tab[0].split(".csv")
    fileName = tab2[0] + "_plot"
    print(f"New file name : {fileName}")

    x = df.iloc[:,0]
    y = df.iloc[:,1]
    plt.grid()
    plt.title("")
    plt.ylabel(y_label)
    plt.xlabel(x_label)

    plt.plot(y, x)
    plt.show()
    # plt.save(fileName)
    return fileName

for exp in experiences:
    for file in exp:
        dir = exp_names[-1] + "/"  # Assuming all experiments are in one directory
        df = pd.read_csv(dir + file)
        new = plot(df, exp, "Time +/- ? [s]", "Volt +/- ? [V]")
        print(f"New file created : {new} !")
