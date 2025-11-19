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

def model_under(t, A, gamma, omega, phi):
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

def model_over(t, A, a, B, b):
    return A * np.exp(-a * t) + B * np.exp(-b * t)

def model_critical(t, A, B, lam):
    return (A + B*t) * np.exp(-lam * t)


##################################
#   Fitting
##################################

def fit_under(t, theta):
    p0 = [theta.max(), 0.1, 2*np.pi, 0.0]
    params, cov = curve_fit(model_under, t, theta, p0=p0, maxfev=20000)
    return params, cov

def fit_over(t, theta):
    p0 = [theta.max(), 0.5, theta.min(), 2.0]
    params, cov = curve_fit(model_over, t, theta, p0=p0)
    return params, cov

def fit_critical(t, theta):
    A0 = theta[0]
    B0 = (theta[1] - theta[0]) / (t[1] - t[0])
    lam0 = 1.0 / (t[-1] - t[0])
    p0 = [A0, B0, lam0]
    params, cov = curve_fit(model_critical, t, theta, p0=p0, maxfev=20000)
    return params, cov


##################################
#   Extraction
##################################

def extract_pseudo_period(params):
    A, gamma, omega, phi = params
    Td = 2*np.pi / omega
    lambda_d = omega
    return Td, lambda_d


##################################
#   Plot (sans équations)
##################################

def plot_fit(name, t, theta, t_fit, theta_fit):
    plt.figure(figsize=(9,4))
    plt.scatter(t, theta, s=15, label="Données")
    plt.plot(t_fit, theta_fit, "r-", label="Fit")
    plt.xlabel("t [s]")
    plt.ylabel("Theta [rad]")
    plt.grid(True)
    plt.legend()
    plt.savefig(name)
    plt.show()


##################################
#   Processus fichier
##################################

def process_file(it, filename=None, mode="under"):
    print("\n=== Traitement :", filename, "===")
    if filename is None:
        return

    t, theta = read_csv(filename)
    name = "libre_frein_0_" + it + "A.png"

    if mode == "under":
        params, cov = fit_under(t, theta)
        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_under(t_fit, *params)

        # --- print paramètres ---
        A, gamma, omega, phi = params
        sigma = np.sqrt(np.diag(cov))
        print("\n--- Paramètres fit sous-amorti ---")
        print(f"A     = {A:.6g} ± {sigma[0]:.3g}")
        print(f"gamma = {gamma:.6g} ± {sigma[1]:.3g}")
        print(f"omega = {omega:.6g} ± {sigma[2]:.3g}")
        print(f"phi   = {phi:.6g} ± {sigma[3]:.3g}")
        print(f"T_d   = {2*np.pi/omega:.6g} s\n")

        plot_fit(name, t, theta, t_fit, theta_fit)

    elif mode == "critical":
        params, cov = fit_critical(t, theta)
        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_critical(t_fit, *params)

        sigma = np.sqrt(np.diag(cov))
        print("\n--- Paramètres fit critique ---")
        print(f"A   = {params[0]:.6g} ± {sigma[0]:.3g}")
        print(f"B   = {params[1]:.6g} ± {sigma[1]:.3g}")
        print(f"λ   = {params[2]:.6g} ± {sigma[2]:.3g}\n")

        plot_fit(name, t, theta, t_fit, theta_fit)

    elif mode == "over":
        params, cov = fit_over(t, theta)
        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_over(t_fit, *params)

        sigma = np.sqrt(np.diag(cov))
        print("\n--- Paramètres fit sur-amorti ---")
        print(f"A = {params[0]:.6g} ± {sigma[0]:.3g}")
        print(f"a = {params[1]:.6g} ± {sigma[1]:.3g}")
        print(f"B = {params[2]:.6g} ± {sigma[2]:.3g}")
        print(f"b = {params[3]:.6g} ± {sigma[3]:.3g}\n")

        plot_fit(name, t, theta, t_fit, theta_fit)


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

it = 1
for filename, mode in files:
    process_file(str(it), filename, mode)
    it += 1

