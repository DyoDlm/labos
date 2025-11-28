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




















































##################################
#   Fichiers à traiter
##################################

it = 1
for filename, mode in files:
    process_file(str(it), filename, mode)
    it += 1

