import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import re

# --- FONT SETTINGS (INCREASED SIZES) ---
plt.rcParams.update({
    'font.size': 16,          # General size
    'axes.labelsize': 18,     # Axis labels (X, Y)
    'axes.titlesize': 20,     # Plot title
    'legend.fontsize': 14,    # Legend
    'xtick.labelsize': 16,    # X-axis tick labels
    'ytick.labelsize': 16     # Y-axis tick labels
})

def parse_latex_data(latex_string):
    data = []
    lines = latex_string.strip().split('\n')
    for line in lines:
        if '&' not in line:
            continue
        parts = [p.strip() for p in line.split('&')]
        if len(parts) < 5:
            continue
        try:
            h0 = float(parts[3])
            err_str = parts[4]
            if '^{' in err_str:
                match = re.search(r'\^\{[+]?([\d.]+)\}_\{-?([\d.]+)\}', err_str)
                if match:
                    err_plus = float(match.group(1))
                    err_minus = float(match.group(2))
                    err = np.sqrt((float(err_plus)**2 + float(err_minus)**2) / 2)
                else:
                    err = float(re.sub(r'[^\d.]', '', err_str.split('}')[0]))
            else:
                err = float(err_str)
            data.append({'h0': h0, 'err': err})
        except:
            continue
    return data

# --- DATA ---
# All Ladder-Independent measurements (Categories 2 + 3 + 4 combined) - 58 measurements
# Sorted chronologically by arXiv ID
latex_data_all = r"""
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
31 & Pogosian & 2024 & 69.37 & 0.65 & BAO-DESI Data (No sound horizon) & {2405.20306}
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
52 & Du & 2025 & 71.59 & 0.94 & inverse dl MAPAge & {2510.26355}
53 & Favale & 2025 & 68.8 & 3.0 & Cosmic Chronometers & {2511.19332}
54 & Garcia & 2025 & 70.03 & 0.97 &  DESI + APS + DES 3×2pt (No sound horizon & {2509.16202}
55 & Zaborowski & 2025 & 70.8 & ^{+2.0}_{-2.2} & DESI Turnover scale+ θ* & {2510.19149}
56 & Krolewski & 2025 & 69.0 & 2.5 & DESI DR1 Densities + CMB (no sound horizon) & {2511.23432}
57 & Paic & 2025 & 64.2 & ^{+5.8}_{-5.0} & Strong lensing (doubly lensed quasar) & {2512.03178}
58 & Oliveira & 2026 & 67.9 & ^{+4.4}_{-4.3} WL/GC + GW sirens & {2601.04774}
"""

# Category 3: Pure Local Ladder-Independent (Model Independent) - 16 measurements
# Sorted chronologically by arXiv ID
latex_data_lcdm_independent = r"""
1 & Kuo & 2012 & 68 & 9 & Megamasers with Keplerian kinematics & {1207.7273}
2 & Gao & 2015 & 66 & 6 & Megamasers with Keplerian kinematics & {1511.08311}
3 & Bulla & 2022 & 69.6 & 5.5 & Standard sirens & {2205.09145}
4 & Zhang & 2022 & 65.9 & ^{+3.0}_{-2.9} & Cosmic Chronometers + HII galaxies & {2208.03960}
5 & Du & 2023 & 71.5 & ^{+4.4}_{-3.0} & Time-delay galaxy lenses + GRBs (model-independent) & {2302.13887}
6 & Palmese & 2023 & 75.46 & ^{+5.34}_{-5.39} & Standard Siren GW170817 + afterglow & {2305.19914}
7 & Sneppen & 2023 & 67.0 & 3.6 & EPM + Kilonovae & {2306.12468}
8 & Liu & 2023 & 72.9 & ^{+2.0}_{-2.3} & Strong lensing + SNe Ia Gaussian process & {2309.13608}
9 & Li & 2024 & 66.3 & ^{+3.8}_{-3.6} & Lensed SNe Ia Refsdal (GP, model-independent) & {2401.12052}
10 & Gonzalez & 2024 & 72.7 & ^{+6.3}_{-5.6} & fgas + SNe Ia + CDDR & {2405.13665}
11 & Jaiswal & 2025 & 66.9 & ^{+10.6}_{-2.1} & FRADO Model + NGC 5548 & {2410.03597}
12 & Vogl & 2024 & 74.9 & 2.7 & SNe II (Tailored EPM) & {2411.04968}
13 & Song & 2025 & 70.40 & ^{+8.03}_{-5.60} & Combined GW + SGL distance calibration & {2503.10346}
14 & Colaco & 2025 & 70.55 & 7.44 & Lensing + SNe (joint) & {2505.17262}
15 & Du & 2025 & 71.59 & 0.94 & inverse dl MAPAge & {2510.26355}
16 & Favale & 2025 & 68.8 & 3.0 & Cosmic Chronometers & {2511.19332}
"""

# Category 2: Local Ladder-Independent (LCDM Assumption) - 33 measurements
# Sorted chronologically by arXiv ID
latex_data_lcdm_dependent = r"""
1 & Wu & 2021 & 68.81 & ^{+4.99}_{-4.33} & Localized FRBs & {2108.00581}
2 & Abbot & 2021 & 68 & ^{+8}_{-6} & Standard sirens & {2111.03604}
3 & Shajib & 2023 & 77.1 & ^{+7.3}_{-7.1} & TD Cosmography & {2301.02656}
4 & Napier & 2023 & 74.1 & 8.0 & TD Cosmography & {2301.11240}
5 & Kelly & 2023 & 66.6 & ^{+4.1}_{-3.3} & TD Cosmography SN Refsdal & {2305.06367}
6 & Dominguez & 2023 & 61.9 & ^{+2.9}_{-2.4} & Gamma-ray attenuation & {2306.09878}
7 & Gao & 2023 & 65.5 & ^{+6.4}_{-5.4} & Fast Radio Bursts + SNe Ia & {2307.08285}
8 & Moresco & 2023 & 66.7 & 5.3 & Cosmic Chronometers & {2307.09501}
9 & Liu & 2023 & 59.1 & ^{+3.6}_{-3.5} & Cluster lensed quasar + TD & {2307.14833}
10 & Fung & 2023 & 86 & ^{+55}_{-46} & Pure GW NSBH (NS mass function) & {2308.02440}
11 & Martinez & 2023 & 74 & ^{+9}_{-13} & TD cosmography & {2309.14776}
12 & Alfradique & 2023 & 68.84 & ^{+15.51}_{-7.74} & Dark sirens LIGO/Virgo & {2310.13695}
13 & Ballard & 2023 & 85.4 & ^{+29.1}_{-33.9} & Dark siren GW190412 & {2311.13062}
14 & Grillo & 2024 & 66.2 & ^{+3.5}_{-3.2} & Lensing TD HFF & {2401.10980}
15 & Pascale & 2024 & 71.8 & ^{+9.2}_{-8.1} & TD Lensed SNe Ia H0pe (JWST) & {2403.18902}
16 & Hernandez & 2024 & 73.0 & ^{+13.7}_{-7.7} & GW Standard sirens GWTC-3 (assuming LCDM) & {2404.02522}
17 & Bom & 2024 & 70.4 & ^{+13.6}_{-11.7} & GW Standard sirens + Kilonovae O4a & {2404.16092}
18 & TDCOSMO XVI & 2024 & 65 & ^{+23}_{-14} & TD COSMO WGD2038 & {2406.02683}
19 & Gao & 2024 & 68.81 & 5.64 & Non-localized FRBs + systematics & {2410.03994}
20 & Li & 2024 & 66 & 5 & Lensing Bias Correction TDCOSMO IV & {2410.16171}
21 & Yang & 2024 & 74.0 & ^{+7.5}_{-7.2} & FRBs with Scattering & {2411.02249}
22 & Piratova-Moreno & 2025 & 65.1 & 7.4 & FRBs (MLE) & {2502.08509}
23 & Barua & 2025 & 73.5 & ^{+3}_{-2.9} & MCP (LCDM angular diameter distance) & {2502.11998}
24 & Zhang & 2024 & 75 & 30 & FRB persistent radio sources & {2504.13132}
25 & Gao & 2025 & 86.18 & ^{+18.03}_{-14.99} & FRBs RM-PRS correlation & {2504.15119}
26 & Beirnaert & 2025 & 79 & 9 & GW Dark Sirens (averaged) & {2505.14077}
27 & Bahr-Kalus & 2025 & 74.0 & ^{+7.2}_{-3.5} & DESI Turnover Scale + BAO & {2505.16153}
28 & Birrer & 2025 & 71.6 & ^{+3.9}_{-3.3} & TDCOSMO 2025 strong lensing & {2506.03023}
29 & Loubser & 2025 & 54.6 & 26.3 & Cosmic chronometers & {2506.03836}
30 & Liu & 2025 & 66.0 & 4.3 & Strong gravitational lensing (JWST improved) & {2509.09979}
31 & Pierel & 2025 & 66.9 & ^{+11.2}_{-8.1} & SN Encore time delays & {2509.12301}
32 & Paic & 2025 & 64.2 & ^{+5.8}_{-5.0} & Strong lensing (doubly lensed quasar) & {2512.03178}
33 & Oliveira & 2026 & 67.9 & ^{+4.4}_{-4.3} WL/GC + GW sirens & {2601.04774}
"""

# Category 4: CMB Sound Horizon Free - 9 measurements
# Sorted chronologically by arXiv ID
latex_data_cmb_dependent = r"""
1 & Reese & 2003 & 61 & 18 & SZ effect & {0306.12345}
2 & Philcox & 2021 & 64.8 & ^{+2.2}_{-2.5} & Standard ruler at matter-radiation equality & {2111.03604}
3 & Colaco & 2023 & 67.22 & 6.07 & SZ + X-ray + SNe Ia & {2310.18711}
4 & Pogosian & 2024 & 68.05 & 0.94 & BAO pre-DESI Data (No sound horizon) & {2405.20306}
5 & Pogosian & 2025 & 69.37 & 0.65 & BAO-DESI DR2 Data (No sound horizon) & {pc}
6 & Garcia & 2025 & 70.03 & 0.97 &  DESI + APS + DES 3×2pt (No sound horizon & {2509.16202}
7 & Bahr-Kalus & 2025 & 65.2 & ^{+4.9}_{-6.2} & DESI Turnover Scale + SNe & {2505.16154}
8 & Zaborowski & 2025 & 70.8 & ^{+2.0}_{-2.2} & DESI Turnover scale+ θ* & {2510.19149}
9 & Krolewski & 2025 & 69.0 & 2.5 & DESI DR1 Densities + CMB (no sound horizon) & {2511.23432}
"""

# Category 1: Distance Ladder - 30 measurements
# Sorted chronologically by publication year
latex_data_distance_ladder = r"""
1 & Huang & 2019 & 73.3 & 4.0
2 & de Jaeger & 2020 & 75.8 & 5.1
3 & Kourkchi & 2020 & 76.0 & 2.5
4 & Khetan & 2021 & 70.50 & 4.13
5 & Blakeslee & 2021 & 73.3 & 2.5
6 & Freedman & 2021 & 69.8 & 1.7
7 & Dhawan & 2022 & 76.94 & 6.4
8 & Kenworthy & 2022 & 73.1 & 2.5
9 & Dhawan & 2022 & 70.92 & 1.88
10 & Dhawan & 2022 & 74.82 & 1.28
11 & Scolnic & 2023 & 73.22 & 2.06
12 & de Jaeger & 2023 & 74.1 & 8.0
13 & Uddin & 2023 & 71.76 & 1.32
14 & Uddin & 2023 & 73.22 & 1.45
15 & Huang & 2023 & 72.37 & 2.97
16 & Li & 2024 & 74.7 & 3.1
17 & Chavez & 2024 & 73.1 & 2.3
18 & Boubel & 2024 & 73.3 & 4.1
19 & Lee & 2024 & 67.80 & 2.72
20 & Freedman & 2024 & 72.05 & 3.60
21 & Said & 2024 & 76.05 & 4.90
22 & Zhang & 2024 & 75.5 & 3.8
23 & Jensen & 2025 & 73.8 & 2.4
24 & Wojtak & 2025 & 70.59 & 1.15
25 & Bhardwaj & 2025 & 73.06 & 2.6
26 & Newman & 2025 & 75.3 & 2.9
27 & Riess & 2025 & 73.49 & 0.93
28 & Kudritzki & 2025 & 76.2 & 6.2
29 & Wagner & 2025 & 68 & 8
30 & Lapuente & 2025 & 72.61 & 1.69
"""

# Parse all datasets
data_all = parse_latex_data(latex_data_all)
data_lcdm_independent = parse_latex_data(latex_data_lcdm_independent)
data_lcdm = parse_latex_data(latex_data_lcdm_dependent)
data_cmb = parse_latex_data(latex_data_cmb_dependent)
data_ladder = parse_latex_data(latex_data_distance_ladder)

def compute_weighted_stats(data):
    h0_vals = np.array([d['h0'] for d in data])
    err_vals = np.array([d['err'] for d in data])
    weights = 1.0 / (err_vals ** 2)
    
    weighted_mean = np.sum(weights * h0_vals) / np.sum(weights)
    sigma_mean = 1.0 / np.sqrt(np.sum(weights))
    sigma_scatter = np.std(h0_vals, ddof=1)
    
    return weighted_mean, sigma_mean, sigma_scatter, len(data)

# Initial statistics dictionary
raw_stats = {
    'Distance Ladder': compute_weighted_stats(data_ladder),
    'All Ladder-Independent': compute_weighted_stats(data_all),
    'ΛCDM Dependent': compute_weighted_stats(data_lcdm),
    'ΛCDM Independent': compute_weighted_stats(data_lcdm_independent),
    'CMB Dependent': compute_weighted_stats(data_cmb),
}

# Label mapping for display names
label_map = {
    'Distance Ladder': 'Distance Ladder',
    'All Ladder-Independent': 'All Ladder-Independent',
    'ΛCDM Dependent': 'ΛCDM Dependent',
    'ΛCDM Independent': 'ΛCDM Independent',
    'CMB Dependent': 'CMB Dependent',
}

# Colors
colors = {
    'Distance Ladder': 'blue',
    'All Ladder-Independent': 'black',
    'ΛCDM Dependent': 'green',
    'ΛCDM Independent': 'red',
    'CMB Dependent': 'goldenrod',
}

# Line styles
linestyles = {
    'Distance Ladder': '-',
    'All Ladder-Independent': '-',
    'ΛCDM Dependent': '--',
    'ΛCDM Independent': '--',
    'CMB Dependent': '--',
}

fig, ax = plt.subplots(figsize=(14, 8))

# X-axis range
x = np.linspace(60, 80, 1000)

legend_text = ""

for old_name, (mean, sigma_mean, sigma_scatter, n) in raw_stats.items():
    new_name = label_map[old_name]
    y = norm.pdf(x, loc=mean, scale=sigma_mean)
    ax.plot(x, y, color=colors[old_name], linestyle=linestyles[old_name], linewidth=2.5, label=new_name)
    
    # Update text for Legend Box
    legend_text += f"{new_name} (N={n})\n"
    legend_text += f"  H₀ = {mean:.2f} ± {sigma_mean:.2f}\n"
    legend_text += f"  σ_scatter = {sigma_scatter:.1f}\n\n"

# --- REFERENCE BANDS ---
# Planck Band
planck_mean = 67.4
planck_err = 0.5
ax.axvspan(planck_mean - planck_err, planck_mean + planck_err, alpha=0.3, color='red', label='Planck18 1σ')

# SH0ES/Riess Band
shoes_mean = 73.04
shoes_err = 1.04
ax.axvspan(shoes_mean - shoes_err, shoes_mean + shoes_err, alpha=0.15, color='blue', label='SH0ES (R22)')

# --- LABELS ---
# Planck Label (Bottom Left)
ax.annotate(f'Planck18 1σ\n{planck_mean} ± {planck_err}', 
            xy=(planck_mean, 0.2), xycoords='data',
            xytext=(62, 0.15), textcoords='data',
            arrowprops=dict(facecolor='red', shrink=0.05, alpha=0.5),
            fontsize=14, ha='center',
            bbox=dict(boxstyle='round', facecolor='mistyrose', edgecolor='red'))

# Riess Label (Bottom Right - Symmetric)
ax.annotate(f'Riess2022\n{shoes_mean} ± {shoes_err}',
            xy=(shoes_mean, 0.2), xycoords='data',
            xytext=(78, 0.15), textcoords='data',
            arrowprops=dict(facecolor='blue', shrink=0.05, alpha=0.5),
            fontsize=14, ha='center',
            bbox=dict(boxstyle='round', facecolor='#E6F3FF', edgecolor='blue'))

# --- Stats Box ---
# Top Left with very light red background (#FFF5F5)
ax.text(0.02, 0.98, legend_text.strip(), transform=ax.transAxes, fontsize=12,
        verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle='round', facecolor='#FFF5F5', edgecolor='gray', alpha=0.95),
        family='monospace')

ax.set_xlabel(r'$H_0$ (km s$^{-1}$ Mpc$^{-1}$)')
ax.set_ylabel('Probability Density')
ax.set_title(r'$H_0$ Measurements: Single Gaussian per Category (Weighted Mean ± $\sigma_{mean}$)')
ax.legend(loc='upper right') 
ax.set_xlim(60, 80)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('h0_single_gaussians_ladder_indep.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== SUMMARY ===")
for old_name, (mean, sigma_mean, sigma_scatter, n) in raw_stats.items():

    print(f"{label_map[old_name]} (N={n}): H₀ = {mean:.2f} ± {sigma_mean:.2f}, σ_scatter = {sigma_scatter:.1f}")
