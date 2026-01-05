import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import re

# ==========================================
# 1. DATA
# ==========================================

# Baseline: All One-Step measurements (Categories 2 + 3 + 4) - 54 measurements
# Sorted chronologically by arXiv ID
latex_data_baseline = r"""
1 & Reese & 2003 & 61 & 18 & SZ effect & {0306.12345}
2 & Kuo & 2012 & 68 & 9 & Megamasers with Keplerian kinematics & {1207.7273}
3 & Gao & 2015 & 66 & 6 & Megamasers with Keplerian kinematics & {1511.08311}
4 & Wu & 2021 & 68.81 & ^{+4.99}_{-4.33} & Localized FRBs & {2108.00581}
5 & Abbot & 2021 & 68 & ^{+8}_{-6} & Standard sirens & {2111.03604}
6 & Philcox & 2021 & 64.8 & ^{+2.2}_{-2.5} & Standard ruler at matter-radiation equality & {2111.03604}
7 & Bulla & 2022 & 69.6 & 5.5 & Standard sirens & {2205.09145}
8 & Zhang & 2022 & 65.9 & ^{+3.0}_{-2.9} & Cosmic Chronometers + HII galaxies & {2208.03960}
9 & Shajib & 2023 & 77.1 & ^{+7.3}_{-7.1} & TD Cosmography & {2301.02656}
10 & Napier & 2023 & 74.1 & 8.0 & TD Cosmography & {2301.11240}
11 & Du & 2023 & 71.5 & ^{+4.4}_{-3.0} & Time-delay galaxy lenses + GRBs (model-independent) & {2302.13887}
12 & Kelly & 2023 & 66.6 & ^{+4.1}_{-3.3} & TD Cosmography SN Refsdal & {2305.06367}
13 & Palmese & 2023 & 75.46 & ^{+5.34}_{-5.39} & Standard Siren GW170817 + afterglow & {2305.19914}
14 & Sneppen & 2023 & 67.0 & 3.6 & EPM + Kilonovae & {2306.12468}
15 & Dominguez & 2023 & 61.9 & ^{+2.9}_{-2.4} & Gamma-ray attenuation & {2306.09878}
16 & Gao & 2023 & 65.5 & ^{+6.4}_{-5.4} & Fast Radio Bursts + SNe Ia & {2307.08285}
17 & Moresco & 2023 & 66.7 & 5.3 & Cosmic Chronometers & {2307.09501}
18 & Liu & 2023 & 59.1 & ^{+3.6}_{-3.5} & Cluster lensed quasar + TD & {2307.14833}
19 & Fung & 2023 & 86 & ^{+55}_{-46} & Pure GW NSBH (NS mass function) & {2308.02440}
20 & Liu & 2023 & 72.9 & ^{+2.0}_{-2.3} & Strong lensing + SNe Ia Gaussian process & {2309.13608}
21 & Martinez & 2023 & 74 & ^{+9}_{-13} & TD cosmography & {2309.14776}
22 & Alfradique & 2023 & 68.84 & ^{+15.51}_{-7.74} & Dark sirens LIGO/Virgo & {2310.13695}
23 & Colaco & 2023 & 67.22 & 6.07 & SZ + X-ray + SNe Ia & {2310.18711}
24 & Ballard & 2023 & 85.4 & ^{+29.1}_{-33.9} & Dark siren GW190412 & {2311.13062}
25 & Grillo & 2024 & 66.2 & ^{+3.5}_{-3.2} & Lensing TD HFF & {2401.10980}
26 & Li & 2024 & 66.3 & ^{+3.8}_{-3.6} & Lensed SNe Ia Refsdal (GP, model-independent) & {2401.12052}
27 & Pascale & 2024 & 71.8 & ^{+9.2}_{-8.1} & TD Lensed SNe Ia H0pe (JWST) & {2403.18902}
28 & Hernandez & 2024 & 73.0 & ^{+13.7}_{-7.7} & GW Standard sirens GWTC-3 (assuming LCDM) & {2404.02522}
29 & Bom & 2024 & 70.4 & ^{+13.6}_{-11.7} & GW Standard sirens + Kilonovae O4a & {2404.16092}
30 & Gonzalez & 2024 & 72.7 & ^{+6.3}_{-5.6} & fgas + SNe Ia + CDDR & {2405.13665}
31 & Pogosian & 2024 & 69.48 & 0.94 & BAO-DESI Data (No sound horizon) & {2405.20306}
32 & Pogosian & 2024 & 68.05 & 0.94 & BAO pre-DESI Data (No sound horizon) & {2405.20306}
33 & TDCOSMO XVI & 2024 & 65 & ^{+23}_{-14} & TD COSMO WGD2038 & {2406.02683}
34 & Gao & 2024 & 68.81 & 5.64 & Non-localized FRBs + systematics & {2410.03994}
35 & Jaiswal & 2025 & 66.9 & ^{+10.6}_{-2.1} & FRADO Model + NGC 5548 & {2410.03597}
36 & Li & 2024 & 66 & 5 & Lensing Bias Correction TDCOSMO IV & {2410.16171}
37 & Yang & 2024 & 74.0 & ^{+7.5}_{-7.2} & FRBs with Scattering & {2411.02249}
38 & Vogl & 2024 & 74.9 & 2.7 & SNe II (Tailored EPM) & {2411.04968}
39 & Piratova-Moreno & 2025 & 65.1 & 7.4 & FRBs (MLE) & {2502.08509}
40 & Barua & 2025 & 73.5 & ^{+3}_{-2.9} & MCP (LCDM angular diameter distance) & {2502.11998}
41 & Song & 2025 & 70.40 & ^{+8.03}_{-5.60} & Combined GW + SGL distance calibration & {2503.10346}
42 & Zhang & 2024 & 75 & 30 & FRB persistent radio sources & {2504.13132}
43 & Gao & 2025 & 86.18 & ^{+18.03}_{-14.99} & FRBs RM-PRS correlation & {2504.15119}
44 & Beirnaert & 2025 & 79 & 9 & GW Dark Sirens (averaged) & {2505.14077}
45 & Bahr-Kalus & 2025 & 74.0 & ^{+7.2}_{-3.5} & DESI Turnover Scale + BAO & {2505.16153}
46 & Bahr-Kalus & 2025 & 65.2 & ^{+4.9}_{-6.2} & DESI Turnover Scale + SNe & {2505.16154}
47 & Colaco & 2025 & 70.55 & 7.44 & Lensing + SNe (joint) & {2505.17262}
48 & Birrer & 2025 & 71.6 & ^{+3.9}_{-3.3} & TDCOSMO 2025 strong lensing & {2506.03023}
49 & Loubser & 2025 & 54.6 & 26.3 & Cosmic chronometers & {2506.03836}
50 & Liu & 2025 & 66.0 & 4.3 & Strong gravitational lensing (JWST improved) & {2509.09979}
51 & Pierel & 2025 & 66.9 & ^{+11.2}_{-8.1} & SN Encore time delays & {2509.12301}
52 & Favale & 2025 & 68.8 & 3.0 & Cosmic Chronometers & {2511.19332}
53 & Krolewski & 2025 & 69.0 & 2.5 & DESI DR1 Densities + CMB (no sound horizon) & {2511.23432}
54 & Paic & 2025 & 64.2 & ^{+5.8}_{-5.0} & Strong lensing (doubly lensed quasar) & {2512.03178}
"""

# Clean Data: All One-Step EXCLUDING high-precision Pogosian measurements - 52 measurements
# This reveals underlying bimodal structure (see Figure 4 in paper)
# Sorted chronologically by arXiv ID
latex_data_clean = r"""
1 & Reese & 2003 & 61 & 18 & SZ effect & {0306.12345}
2 & Kuo & 2012 & 68 & 9 & Megamasers with Keplerian kinematics & {1207.7273}
3 & Gao & 2015 & 66 & 6 & Megamasers with Keplerian kinematics & {1511.08311}
4 & Wu & 2021 & 68.81 & ^{+4.99}_{-4.33} & Localized FRBs & {2108.00581}
5 & Abbot & 2021 & 68 & ^{+8}_{-6} & Standard sirens & {2111.03604}
6 & Philcox & 2021 & 64.8 & ^{+2.2}_{-2.5} & Standard ruler at matter-radiation equality & {2111.03604}
7 & Bulla & 2022 & 69.6 & 5.5 & Standard sirens & {2205.09145}
8 & Zhang & 2022 & 65.9 & ^{+3.0}_{-2.9} & Cosmic Chronometers + HII galaxies & {2208.03960}
9 & Shajib & 2023 & 77.1 & ^{+7.3}_{-7.1} & TD Cosmography & {2301.02656}
10 & Napier & 2023 & 74.1 & 8.0 & TD Cosmography & {2301.11240}
11 & Du & 2023 & 71.5 & ^{+4.4}_{-3.0} & Time-delay galaxy lenses + GRBs (model-independent) & {2302.13887}
12 & Kelly & 2023 & 66.6 & ^{+4.1}_{-3.3} & TD Cosmography SN Refsdal & {2305.06367}
13 & Palmese & 2023 & 75.46 & ^{+5.34}_{-5.39} & Standard Siren GW170817 + afterglow & {2305.19914}
14 & Sneppen & 2023 & 67.0 & 3.6 & EPM + Kilonovae & {2306.12468}
15 & Dominguez & 2023 & 61.9 & ^{+2.9}_{-2.4} & Gamma-ray attenuation & {2306.09878}
16 & Gao & 2023 & 65.5 & ^{+6.4}_{-5.4} & Fast Radio Bursts + SNe Ia & {2307.08285}
17 & Moresco & 2023 & 66.7 & 5.3 & Cosmic Chronometers & {2307.09501}
18 & Liu & 2023 & 59.1 & ^{+3.6}_{-3.5} & Cluster lensed quasar + TD & {2307.14833}
19 & Fung & 2023 & 86 & ^{+55}_{-46} & Pure GW NSBH (NS mass function) & {2308.02440}
20 & Liu & 2023 & 72.9 & ^{+2.0}_{-2.3} & Strong lensing + SNe Ia Gaussian process & {2309.13608}
21 & Martinez & 2023 & 74 & ^{+9}_{-13} & TD cosmography & {2309.14776}
22 & Alfradique & 2023 & 68.84 & ^{+15.51}_{-7.74} & Dark sirens LIGO/Virgo & {2310.13695}
23 & Colaco & 2023 & 67.22 & 6.07 & SZ + X-ray + SNe Ia & {2310.18711}
24 & Ballard & 2023 & 85.4 & ^{+29.1}_{-33.9} & Dark siren GW190412 & {2311.13062}
25 & Grillo & 2024 & 66.2 & ^{+3.5}_{-3.2} & Lensing TD HFF & {2401.10980}
26 & Li & 2024 & 66.3 & ^{+3.8}_{-3.6} & Lensed SNe Ia Refsdal (GP, model-independent) & {2401.12052}
27 & Pascale & 2024 & 71.8 & ^{+9.2}_{-8.1} & TD Lensed SNe Ia H0pe (JWST) & {2403.18902}
28 & Hernandez & 2024 & 73.0 & ^{+13.7}_{-7.7} & GW Standard sirens GWTC-3 (assuming LCDM) & {2404.02522}
29 & Bom & 2024 & 70.4 & ^{+13.6}_{-11.7} & GW Standard sirens + Kilonovae O4a & {2404.16092}
30 & Gonzalez & 2024 & 72.7 & ^{+6.3}_{-5.6} & fgas + SNe Ia + CDDR & {2405.13665}
31 & TDCOSMO XVI & 2024 & 65 & ^{+23}_{-14} & TD COSMO WGD2038 & {2406.02683}
32 & Gao & 2024 & 68.81 & 5.64 & Non-localized FRBs + systematics & {2410.03994}
33 & Jaiswal & 2025 & 66.9 & ^{+10.6}_{-2.1} & FRADO Model + NGC 5548 & {2410.03597}
34 & Li & 2024 & 66 & 5 & Lensing Bias Correction TDCOSMO IV & {2410.16171}
35 & Yang & 2024 & 74.0 & ^{+7.5}_{-7.2} & FRBs with Scattering & {2411.02249}
36 & Vogl & 2024 & 74.9 & 2.7 & SNe II (Tailored EPM) & {2411.04968}
37 & Piratova-Moreno & 2025 & 65.1 & 7.4 & FRBs (MLE) & {2502.08509}
38 & Barua & 2025 & 73.5 & ^{+3}_{-2.9} & MCP (LCDM angular diameter distance) & {2502.11998}
39 & Song & 2025 & 70.40 & ^{+8.03}_{-5.60} & Combined GW + SGL distance calibration & {2503.10346}
40 & Zhang & 2024 & 75 & 30 & FRB persistent radio sources & {2504.13132}
41 & Gao & 2025 & 86.18 & ^{+18.03}_{-14.99} & FRBs RM-PRS correlation & {2504.15119}
42 & Beirnaert & 2025 & 79 & 9 & GW Dark Sirens (averaged) & {2505.14077}
43 & Bahr-Kalus & 2025 & 74.0 & ^{+7.2}_{-3.5} & DESI Turnover Scale + BAO & {2505.16153}
44 & Bahr-Kalus & 2025 & 65.2 & ^{+4.9}_{-6.2} & DESI Turnover Scale + SNe & {2505.16154}
45 & Colaco & 2025 & 70.55 & 7.44 & Lensing + SNe (joint) & {2505.17262}
46 & Birrer & 2025 & 71.6 & ^{+3.9}_{-3.3} & TDCOSMO 2025 strong lensing & {2506.03023}
47 & Loubser & 2025 & 54.6 & 26.3 & Cosmic chronometers & {2506.03836}
48 & Liu & 2025 & 66.0 & 4.3 & Strong gravitational lensing (JWST improved) & {2509.09979}
49 & Pierel & 2025 & 66.9 & ^{+11.2}_{-8.1} & SN Encore time delays & {2509.12301}
50 & Favale & 2025 & 68.8 & 3.0 & Cosmic Chronometers & {2511.19332}
51 & Krolewski & 2025 & 69.0 & 2.5 & DESI DR1 Densities + CMB (no sound horizon) & {2511.23432}
52 & Paic & 2025 & 64.2 & ^{+5.8}_{-5.0} & Strong lensing (doubly lensed quasar) & {2512.03178}
"""

# ==========================================
# 2. PARSING LOGIC
# ==========================================
def parse_latex_table(raw_data):
    parsed_data = []
    lines = raw_data.strip().split('\n')
    
    for line in lines:
        clean = line.strip()
        if not clean or clean.startswith('%'):
            continue
        
        parts = [p.strip() for p in clean.split('&')]
        if len(parts) < 5:
            continue
        
        try:
            h0 = float(parts[3])
            err_str = parts[4]
            
            # Parse asymmetric errors: ^{+X}_{-Y}
            asym_match = re.search(r'\^\{\+?([\d\.]+)\}_\{-?([\d\.]+)\}', err_str)
            if asym_match:
                e_plus = float(asym_match.group(1))
                e_minus = float(asym_match.group(2))
                # Quadrature mean of asymmetric errors
                err = np.sqrt((e_plus**2 + e_minus**2) / 2.0)
            else:
                # Symmetric error - extract number
                val_match = re.search(r'[\d\.]+', err_str)
                if val_match:
                    err = float(val_match.group())
                else:
                    print(f"WARNING: Could not parse error '{err_str}', skipping")
                    continue
            
            if err <= 0:
                print(f"WARNING: Invalid error {err} for H0={h0}, skipping")
                continue
            
            parsed_data.append({'h0': h0, 'err': err})
            
        except ValueError as e:
            print(f"WARNING: Parse error on line '{line}': {e}")
            continue
    
    return parsed_data

# Run parsing
baseline_data = parse_latex_table(latex_data_baseline)
clean_data = parse_latex_table(latex_data_clean)

print(f"Parsed {len(baseline_data)} baseline measurements")
print(f"Parsed {len(clean_data)} clean data measurements (excluding Pogosian)")

# ==========================================
# 3. STATISTICAL CALCULATIONS
# ==========================================
def get_weighted_stats(data):
    vals = np.array([d['h0'] for d in data])
    errs = np.array([d['err'] for d in data])
    weights = 1.0 / (errs**2)
    
    weighted_mean = np.sum(vals * weights) / np.sum(weights)
    weighted_err = np.sqrt(1.0 / np.sum(weights))
    
    return weighted_mean, weighted_err, vals, errs

mu_baseline, sigma_baseline, vals_baseline, errs_baseline = get_weighted_stats(baseline_data)
mu_clean, sigma_clean, vals_clean, errs_clean = get_weighted_stats(clean_data)

print(f"\n=== RESULTS ===")
print(f"Baseline: H0 = {mu_baseline:.2f} ± {sigma_baseline:.2f}")
print(f"Clean Data: H0 = {mu_clean:.2f} ± {sigma_clean:.2f}")

# 1. Calculate Percentage Change in Weighted Mean
# (Clean - Baseline) / Baseline * 100
mean_change_pct = ((mu_clean - mu_baseline) / mu_baseline) * 100

# 2. Calculate Percentage Change in Uncertainty
# (Clean - Baseline) / Baseline * 100
uncertainty_change_pct = ((sigma_clean - sigma_baseline) / sigma_baseline) * 100

print(f"Mean Change: {mean_change_pct:.2f}%")
print(f"Uncertainty Change: {uncertainty_change_pct:.2f}%")

# ==========================================
# 4. PDF GENERATION
# ==========================================
x_grid = np.linspace(55, 95, 1000)

def generate_weighted_pdf(data, x):
    y_sum = np.zeros_like(x)
    for d in data:
        weight = 1.0 / (d['err']**2)
        y_sum += weight * norm.pdf(x, loc=d['h0'], scale=d['err'])
    
    area = np.trapezoid(y_sum, x)
    return y_sum / area

y_baseline_pdf = generate_weighted_pdf(baseline_data, x_grid)
y_clean_pdf = generate_weighted_pdf(clean_data, x_grid)

# ==========================================
# 5. PLOTTING
# ==========================================
fig, ax = plt.subplots(figsize=(10, 7))

# Plot Curves
ax.plot(x_grid, y_baseline_pdf, color='red', linestyle='--', lw=2, label='Baseline')
ax.plot(x_grid, y_clean_pdf, color='darkred', linestyle='-', lw=2, label='Clean Data')

# Planck
planck_val = 67.4
planck_err = 0.5
ax.axvline(planck_val, color='purple', linestyle='--', lw=1, alpha=0.8)
ax.text(planck_val + 0.5, 0.10, f'Planck 18\n{planck_val} ± {planck_err}',
        color='black', fontsize=10, va='center')

# Annotations (Top Right - Stats)
ax.text(0.95, 0.95, rf"$H_0^{{\mathrm{{base}}}} = {mu_baseline:.2f} \pm {sigma_baseline:.2f}$",
        transform=ax.transAxes, ha='right', fontsize=16, color='red')
ax.text(0.95, 0.89, rf"$H_0^{{\mathrm{{clean}}}} = {mu_clean:.2f} \pm {sigma_clean:.2f}$",
        transform=ax.transAxes, ha='right', fontsize=16, color='darkred')

# Annotations (Top Left - Changes)
# Mean change displayed above uncertainty change
change_text = (f"Mean Change: {mean_change_pct:+.2f}%\n"
               f"Uncertainty Change: {uncertainty_change_pct:+.2f}%")

ax.text(0.02, 0.95, change_text, transform=ax.transAxes, ha='left', va='top',
        fontsize=12, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.5))

ax.set_xlabel(r'$H_0$ (km s$^{-1}$ Mpc$^{-1}$)', fontsize=18)
ax.set_ylabel('Probability density', fontsize=16)
ax.set_title(r'$H_0$ measurements: Baseline vs. Reduced Data', fontsize=20)
ax.set_xlim(55, 95)
ax.set_ylim(0, max(y_baseline_pdf.max(), y_clean_pdf.max()) * 1.1)
# Legend moved slightly down to avoid overlap with text box
ax.legend(loc='upper left', bbox_to_anchor=(0, 0.85), frameon=True)

plt.tight_layout()
plt.savefig('h0_bimodality_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig('h0_bimodality_analysis.pdf', bbox_inches='tight')
print("\nPlot saved to 'h0_bimodality_analysis.png' and 'h0_bimodality_analysis.pdf'")
plt.show()