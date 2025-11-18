import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def read_csv(filename):
    print("filename is : ", filename)
    data = np.loadtxt(filename, delimiter=",", skiprows=1)
    t = data[:, 0]
    theta = data[:, 1]
    return t, theta


##################################
#   Modèles
##################################

# MODELE PSEUDO-PERIODIQUE
def model_under(t, A, gamma, omega, phi):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

# MODELE APERIODIQUE
def model_over(t, A, a, B, b):
    return A * np.exp(-a * t) + B * np.exp(-b * t)

# MODELE CRITIQUE
def model_critical(t, A, B, lam):
    return (A + B*t) * np.exp(-lam * t)



##################################
#   Fitting
##################################

# FIT PSEUDO-PERIODIQUE
def fit_under(t, theta):
    p0 = [theta.max(), 0.1, 2*np.pi, 0.0]
    params, cov = curve_fit(model_under, t, theta, p0=p0)
    return params, cov

# FIT APERIODIQUE
def fit_over(t, theta):
    p0 = [theta.max(), 0.5, theta.min(), 2.0]
    params, cov = curve_fit(model_over, t, theta, p0=p0)
    return params, cov

# FIT CRITIQUE
def fit_critical(t, theta):
    A0 = theta[0]
    B0 = (theta[1] - theta[0]) / (t[1] - t[0])
    lam0 = 1.0 / (t[-1] - t[0])
    p0 = [A0, B0, lam0]
    params, cov = curve_fit(model_critical, t, theta, p0=p0, maxfev=20000)
    return params, cov


##################################
#   Plot
##################################

def plot_fit(t, theta, t_fit, theta_fit, title):
    plt.figure(figsize=(9,4))
    plt.scatter(t, theta, s=15, label="Données")
    plt.plot(t_fit, theta_fit, "r-", label="Fit")
    plt.xlabel("Temps (s)")
    plt.ylabel("Angle (rad)")
    plt.grid(True)
    plt.legend()
    plt.show()


##################################
#   Processus fichier
##################################

def process_file(filename=None, mode="under"):
    print("\n=== Traitement :", filename, "===")
    if filename is None:
        return
    
    t, theta = read_csv(filename)

    if mode == "under":
        params, cov = fit_under(t, theta)
        A, gamma, omega, phi = params
        print(f"A={A:.4g}, gamma={gamma:.4g}, omega={omega:.4g}, phi={phi:.4g}")
        print("Pseudo-période Td =", 2*np.pi/omega)

        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_under(t_fit, *params)

    elif mode == "critical":
        params, cov = fit_critical(t, theta)
        A, B, lam = params
        print(f"A={A:.4g}, B={B:.4g}, lambda={lam:.4g}")
        print(">> Amortissement critique : pas de pseudo-période")

        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_critical(t_fit, *params)

    else:
        params, cov = fit_over(t, theta)
        A, a, B, b = params
        print(f"A={A:.4g}, a={a:.4g}, B={B:.4g}, b={b:.4g}")

        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_over(t_fit, *params)

    plot_fit(t, theta, t_fit, theta_fit, f"Fit : {filename}")


##################################
#   Fichiers à traiter
##################################

files = [
    ("Mesure_0_1A.csv", "under"),
    ("Mesure_0_2A.csv", "under"),
    ("Mesure_0_3A.csv", "under"),
    ("Mesure_0_4A.csv", "under"),
    ("Mesure_0_5A.csv", "under"),
    ("Mesure_0_9A.csv", "under")
]

for filename, mode in files:
    process_file(filename, mode)

