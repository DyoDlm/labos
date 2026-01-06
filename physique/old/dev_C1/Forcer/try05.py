# Retry: parse the provided text manually (skip header) and build DataFrame robustly.

import numpy as np, pandas as pd, io, os, math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

raw = """
Freq [Hz]	Incertitude [Hz]	Amplitude [°]	Incertitude [°]	Phase [°]	Insertitude [°]
0,1794	0,0002	4,16	0,05	-13,4	0,3
0,6984	0,0006	4,74	0,05	-170,9	0,4
0,5405	0,0002	24,45	0,05	-126,9	0,2
0,3957	0,0005	9,18	0,07	-21,9	0,6
0,3207	0,0004	6,38	0,05	-16,7	0,4
0,2430	0,0001	5,04	0,05	-12,5	0,2
0,4709	0,0003	18,40	0,20	-40,4	0,2
0,6390	0,0010	6,23	0,06	-165,5	0,8
0,6968	0,0005	4,79	0,05	-170,6	0,4
1,1311	0,0006	1,08	0,05	-175,0	0,3
"""

# prepare rows by splitting lines and skipping header
lines = [ln.strip() for ln in raw.strip().splitlines() if ln.strip()!='']
data_lines = [ln for ln in lines if not any(c.isalpha() for c in ln.split())==False]  # hack
# Better: skip first line explicitly
data_lines = lines[1:]

rows = []
for ln in data_lines:
    parts = [p.replace(',', '.') for p in ln.split()]
    if len(parts) != 6:
        # try splitting by multiple spaces
        parts = [p.replace(',', '.') for p in ln.split() if p!='']
    if len(parts) != 6:
        raise ValueError(f"Could not parse line into 6 tokens: '{ln}' -> {parts}")
    rows.append(parts)

df = pd.DataFrame(rows, columns=['Freq_Hz','Freq_err_Hz','Amp_deg','Amp_err_deg','Phase_deg','Phase_err_deg']).astype(float)

# Duplicate for sheets 0.5A and 0.9A as user provided single table
sheets = {'0.5A': df.copy(), '0.9A': df.copy()}

# Define models
def amp_model_w(f, A0, f0, gamma):
    w = 2*np.pi*f
    w0 = 2*np.pi*f0
    return A0 / np.sqrt((w0**2 - w**2)**2 + (2*gamma*w)**2)

def phase_model_w(f, f0, gamma, phi0):
    w = 2*np.pi*f
    w0 = 2*np.pi*f0
    return np.degrees(phi0 + np.arctan2(2*gamma*w, (w0**2 - w**2)))

def power_model(f, f0, Q):
    return 1.0 / (1.0 + Q**2 * (f/f0 - f0/f)**2)

# Analysis functions (same as previous, encapsulated)
def analyze_gamma(df_sheet, label):
    f = df_sheet['Freq_Hz'].values
    A = df_sheet['Amp_deg'].values
    A_err = df_sheet['Amp_err_deg'].values
    P = df_sheet['Phase_deg'].values
    P_err = df_sheet['Phase_err_deg'].values
    idx = np.argsort(f)
    f = f[idx]; A = A[idx]; A_err = A_err[idx]; P = P[idx]; P_err = P_err[idx]
    p0 = [A.max(), f[np.argmax(A)], 0.05]
    pars, cov = curve_fit(amp_model_w, f, A, p0=p0, sigma=A_err, absolute_sigma=True, maxfev=200000)
    A0, f0, gamma = pars
    perr = np.sqrt(np.diag(cov))
    sigma_A0, sigma_f0, sigma_gamma = perr[0], perr[1], perr[2]
    omega_d = 2*np.pi*f0; omega_d_err = 2*np.pi*sigma_f0
    omega0 = np.sqrt(omega_d**2 + gamma**2)
    # propagate uncertainty
    d_omega0_df0 = ((2*np.pi)**2 * f0) / (2*omega0)
    d_omega0_dgamma = gamma / omega0
    omega0_err = np.sqrt((d_omega0_df0*sigma_f0)**2 + (d_omega0_dgamma*sigma_gamma)**2)
    # phase fit fixing f0,gamma
    def phase_model_fixed(f, phi0):
        return phase_model_w(f, f0, gamma, phi0)
    pars_phi, cov_phi = curve_fit(phase_model_fixed, f, P, p0=[0.0], sigma=P_err, absolute_sigma=True, maxfev=200000)
    phi0 = pars_phi[0]; phi0_err = np.sqrt(np.diag(cov_phi))[0]
    return {'label':label,'f':f,'A':A,'A_err':A_err,'P':P,'P_err':P_err,
            'amp_fit':{'A0':A0,'f0':f0,'gamma':gamma,'cov':cov,'perr':perr},
            'omega_d':omega_d,'omega_d_err':omega_d_err,
            'omega0':omega0,'omega0_err':omega0_err,
            'phase_fit':{'phi0':phi0,'phi0_err':phi0_err}}

def analyze_Q(df_sheet, label):
    f = df_sheet['Freq_Hz'].values
    A = df_sheet['Amp_deg'].values
    idx = np.argsort(f)
    f = f[idx]; A = A[idx]
    P_norm = (A / A.max())**2
    p0 = [f[np.argmax(P_norm)], 5.0]
    pars, cov = curve_fit(power_model, f, P_norm, p0=p0, maxfev=200000)
    f0_fit, Q_fit = pars; perr = np.sqrt(np.diag(cov))
    sigma_f0, sigma_Q = perr[0], perr[1]
    P_shift = P_norm - 0.5
    roots = []
    for i in range(len(f)-1):
        if P_shift[i] == 0:
            roots.append(f[i])
        elif P_shift[i]*P_shift[i+1] < 0:
            r = f[i] + (f[i+1]-f[i]) * abs(P_shift[i])/(abs(P_shift[i]) + abs(P_shift[i+1]))
            roots.append(r)
    fwhm = abs(roots[1]-roots[0]) if len(roots)>=2 else np.nan
    if not np.isnan(fwhm) and fwhm>0:
        Q_exp = f0_fit / fwhm
        # estimate sigma_fwhm via varying f0 by sigma_f0
        f0_plus = f0_fit + sigma_f0; f0_minus = f0_fit - sigma_f0
        P_plus = power_model(f, f0_plus, Q_fit) - 0.5
        P_minus = power_model(f, f0_minus, Q_fit) - 0.5
        roots_plus, roots_minus = [], []
        for arr, store in [(P_plus, roots_plus),(P_minus, roots_minus)]:
            for i in range(len(f)-1):
                if arr[i]*arr[i+1] < 0:
                    r = f[i] + (f[i+1]-f[i]) * abs(arr[i])/(abs(arr[i])+abs(arr[i+1]))
                    store.append(r)
        if len(roots_plus)>=2 and len(roots_minus)>=2:
            fwhm_plus = abs(roots_plus[1]-roots_plus[0])
            fwhm_minus = abs(roots_minus[1]-roots_minus[0])
            sigma_fwhm = 0.5*abs(fwhm_plus - fwhm_minus)
        else:
            sigma_fwhm = np.nan
        if not np.isnan(sigma_fwhm):
            sigma_Qexp = Q_exp * math.sqrt( (sigma_f0/f0_fit)**2 + (sigma_fwhm/fwhm)**2 )
        else:
            sigma_Qexp = np.nan
    else:
        Q_exp = np.nan; sigma_fwhm=np.nan; sigma_Qexp=np.nan
    return {'label':label,'f':f,'A':A,'P_norm':P_norm,'power_fit':{'f0':f0_fit,'Q_fit':Q_fit,'cov':cov,'perr':perr},
            'FWHM':fwhm,'sigma_FWHM':sigma_fwhm,'Q_exp':Q_exp,'sigma_Qexp':sigma_Qexp}

results_gamma={}; results_Q={}
for lab, df_sheet in sheets.items():
    results_gamma[lab] = analyze_gamma(df_sheet, lab)
    results_Q[lab] = analyze_Q(df_sheet, lab)

# Print clean summary
for lab in sheets.keys():
    rg = results_gamma[lab]; rq = results_Q[lab]
    A0 = rg['amp_fit']['A0']; sigma_A0 = rg['amp_fit']['perr'][0]
    f0 = rg['amp_fit']['f0']; sigma_f0 = rg['amp_fit']['perr'][1]
    gamma = rg['amp_fit']['gamma']; sigma_gamma = rg['amp_fit']['perr'][2]
    omega0 = rg['omega0']; omega0_err = rg['omega0_err']
    print(f"=== Sheet {lab} ===")
    print("Gamma-based fit (amplitude):")
    print(f"  A0    = {A0:.4f} ± {sigma_A0:.4f} deg")
    print(f"  f0    = {f0:.6f} ± {sigma_f0:.6f} Hz")
    print(f"  gamma = {gamma:.6f} ± {sigma_gamma:.6f} rad/s")
    print(f"  omega0 = {omega0:.6f} ± {omega0_err:.6f} rad/s")
    print("Q/FWHM analysis (power):")
    print(f"  f0 (power fit) = {rq['power_fit']['f0']:.6f} ± {rq['power_fit']['perr'][0]:.6f} Hz")
    print(f"  Q (fit)        = {rq['power_fit']['Q_fit']:.4f} ± {rq['power_fit']['perr'][1]:.4f}")
    print(f"  FWHM (num)     = {rq['FWHM']:.6f} ± {rq['sigma_FWHM'] if not np.isnan(rq['sigma_FWHM']) else float('nan'):.6f} Hz")
    print(f"  Q (exp) = f0/FWHM = {rq['Q_exp']:.4f} ± {rq['sigma_Qexp'] if not np.isnan(rq['sigma_Qexp']) else float('nan'):.4f}")
    print()

# Save plots
os.makedirs('labo_outputs', exist_ok=True)
for lab in sheets.keys():
    rg = results_gamma[lab]
    f = rg['f']; A = rg['A']; P = rg['P']
    A0 = rg['amp_fit']['A0']; f0 = rg['amp_fit']['f0']; gamma = rg['amp_fit']['gamma']
    ffit = np.linspace(f.min(), f.max(), 400)
    A_fit = amp_model_w(ffit, A0, f0, gamma)
    plt.figure(figsize=(8,4))
    plt.scatter(f, A)
    plt.plot(ffit, A_fit, linestyle='--')
    plt.xlabel('f [Hz]'); plt.ylabel('Amplitude [deg]'); plt.title(f'Amplitude vs f - {lab}')
    plt.grid(); plt.savefig(f'labo_outputs/amplitude_{lab}.png'); plt.close()
    # phase
    phi0 = rg['phase_fit']['phi0']
    P_fit = phase_model_w(ffit, f0, gamma, phi0)
    plt.figure(figsize=(8,4))
    plt.scatter(f, rg['P'])
    plt.plot(ffit, P_fit, linestyle='--')
    plt.xlabel('f [Hz]'); plt.ylabel('Phase [deg]'); plt.title(f'Phase vs f - {lab}')
    plt.grid(); plt.savefig(f'labo_outputs/phase_{lab}.png'); plt.close()
    # power
    rq = results_Q[lab]
    f = rq['f']; Pnorm = rq['P_norm']
    ffit = np.linspace(f.min(), f.max(), 800)
    f0_q = rq['power_fit']['f0']; Qfit = rq['power_fit']['Q_fit']
    plt.figure(figsize=(8,4))
    plt.scatter(f, Pnorm)
    plt.plot(ffit, power_model(ffit, f0_q, Qfit), linestyle='--')
    plt.axhline(0.5, linestyle=':')
    plt.xlabel('f [Hz]'); plt.ylabel('P / P0'); plt.title(f'Normalized power - {lab}')
    plt.grid(); plt.savefig(f'labo_outputs/power_{lab}.png'); plt.close()

print('Plots saved to labo_outputs directory (amplitude_*.png, phase_*.png, power_*.png).')

def fit_f0_from_phase(df):
    f = df["Freq_Hz"].values
    P = df["Phase_deg"].values
    P_err = df["Phase_err_deg"].values

    # tri par fréquence
    idx = np.argsort(f)
    f, P, P_err = f[idx], P[idx], P_err[idx]

    # modèle complet
    def phase_model_fit(f, f0, gamma, phi0):
        w = 2*np.pi*f
        w0 = 2*np.pi*f0
        return np.degrees(phi0 + np.arctan2(2*gamma*w, (w0**2 - w**2)))

    # Estimation initiale
    f0_guess = f[np.argmin(np.abs(P + 90))] if np.any(P < -90) else f[len(f)//2]
    p0 = [f0_guess, 0.05, 0.0]

    pars, cov = curve_fit(
        phase_model_fit, f, P, p0=p0,
        sigma=P_err, absolute_sigma=True, maxfev=3000000
    )

    f0_phase, gamma_phase, phi0 = pars
    sigma_f0, sigma_gamma, sigma_phi0 = np.sqrt(np.diag(cov))

    return {
        "f": f,
        "P": P,
        "f0_phase": f0_phase,
        "sigma_f0_phase": sigma_f0,
        "gamma_phase": gamma_phase,
        "sigma_gamma_phase": sigma_gamma,
        "phi0": phi0,
        "sigma_phi0": sigma_phi0,
        "pars": pars,
        "cov": cov,
    }
phase_result = fit_f0_from_phase(df)

print("=== f0 obtenu depuis la phase ===")
print(f"f0_phase = {phase_result['f0_phase']:.6f} ± {phase_result['sigma_f0_phase']:.6f} Hz")
print(f"gamma_phase = {phase_result['gamma_phase']:.6f} ± {phase_result['sigma_gamma_phase']:.6f} rad/s")
print(f"phi0 = {phase_result['phi0']:.3f} ± {phase_result['sigma_phi0']:.3f} deg")

