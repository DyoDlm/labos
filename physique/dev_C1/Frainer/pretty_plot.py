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


def extract_pseudo_period(params):
    """
    params = [A, gamma, omega, phi]
    Retourne la pseudo période Td et la pulsation amortie lambda_d.
    """
    _, gamma, omega, _ = params

    Td = 2*np.pi / omega
    lambda_d = omega   # dans le modèle sous-amorti

    return Td, lambda_d


##################################
#   Plot
##################################

def plot_fit(name, t, theta, t_fit, theta_fit, params, model_type="under"):
    plt.figure(figsize=(9,4))
    plt.scatter(t, theta, s=15, label="Données")
    plt.plot(t_fit, theta_fit, "r-", label="Fit")

    plt.xlabel("t[s]")
    plt.ylabel("Theta [rad]")
    plt.grid(True)

    if model_type == "under":
        A, gamma, omega, phi = params
        Td, lambda_d = extract_pseudo_period(params)

        eq = (
            r"$\theta(t)=%.3f e^{-%.3f t} \cos(%.3f t + %.3f)$"
            % (A, gamma, omega, phi)
        )

    elif model_type == "critical":
        A, B, lam = params
        eq = (
            r"$\theta(t)=(%.3f + %.3f t)\, e^{-%.3f t}$"
            % (A, B, lam)
        )
    elif model_type == "over":
        A, a, B, b = params
        eq = (
            r"$\theta(t)=%.3f e^{-%.3f t} + %.3f e^{-%.3f t}$"
            % (A, a, B, b)
        )

    plt.text(0.05, 0.95, eq, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(facecolor='white', alpha=0.7))
    # ==============================================

    eq_text = (
        f"$θ(t)=A e^{{-γt}} \\cos(ω t + φ)$\n"
        f"A={params[0]:.3g}, γ={params[1]:.3g}, "
        f"ω={params[2]:.3g}, φ={params[3]:.3g}\n"
        f"T_d={2*np.pi/params[2]:.3g} s"
    )

    plt.text(
        0.52, 0.95, eq_text,
        transform=plt.gca().transAxes,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(facecolor="white", alpha=0.7)
    )
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

    print("name is : ", name)
    if mode == "under":
        params, cov = fit_under(t, theta)
        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_under(t_fit, *params)
        plot_fit(name, t, theta, t_fit, theta_fit, params, model_type="under")

    elif mode == "critical":
        params, cov = fit_critical(t, theta)
        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_critical(t_fit, *params)
        plot_fit(name, t, theta, t_fit, theta_fit, params, model_type="critical")

    elif mode == "over":
        params, cov = fit_over(t, theta)
        t_fit = np.linspace(t.min(), t.max(), 2000)
        theta_fit = model_over(t_fit, *params)
        plot_fit(name, t, theta, t_fit, theta_fit, params, model_type="over")


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

