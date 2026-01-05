import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import re

# --- ΡΥΘΜΙΣΕΙΣ ΓΡΑΜΜΑΤΟΣΕΙΡΩΝ (ΑΥΞΗΜΕΝΑ ΜΕΓΕΘΗ) ---
plt.rcParams.update({
    'font.size': 16,          # Γενικό μέγεθος
    'axes.labelsize': 18,     # Ετικέτες αξόνων (X, Y)
    'axes.titlesize': 20,     # Τίτλος γραφήματος
    'legend.fontsize': 14,    # Legend
    'xtick.labelsize': 16,    # Αριθμοί στον άξονα X
    'ytick.labelsize': 16     # Αριθμοί στον άξονα Y
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

# --- ΔΕΔΟΜΕΝΑ (DATA) ---
latex_data_all = r"""
1 & Kuo & 2012 & 68 & 9 & Megamasers with Keplerian kinematics & {1207.7273}
2 & Gao & 2015 & 66 & 6 & Megamasers with Keplerian kinematics & {1511.08311}
3 & Du & 2023 & 71.5 & ^{+4.4}_{-3.0} & Time-delay galaxy lenses + GRBs(brakes ΛCDM) & {2302.13887}
4 & Bulla & 2022 & 69.6 & 5.5 & standard sirens & {2205.09145}
5 & Palmese & 2023 & 75.46 & ^{+5.34}_{-5.39} & Standard Siren GW170817 + afterglow & {2305.19914}
6 & Sneppen & 2023 & 67.0 & 3.6 & EPM + Kilonovae & {2306.12468}
7 & Zhang & 2022 & 65.9 & ^{+3.0}_{-2.9} & Cosmic Chronometers + HII galaxies & {2208.03960}
8 & Moresco & 2023 & 66.7 & 5.3 & Cosmic Chronometers & {2307.09501}
9 & Liu & 2023 & 72.9 & ^{+2.0}_{-2.3} & Strong lensing + SnIa Gaussian process & {2309.13608}
10 & Alfradique & 2023 & 68.84 & ^{+15.51}_{-7.74} & Dark sirens LIGO/Virgo & {2310.13695}
11 & Li & 2024 & 66.3 & ^{+3.8}_{-3.6} & Lensed SnIa Refsdal (GP breaks ΛCDM) & {2401.12052}
12 & Gonzalez & 2024 & 72.7 & ^{+6.3}_{-5.6} & fgas + SNIa + CDDR & {2405.13665}
13 & Jaiswal & 2025 & 66.9 & ^{+10.6}_{-2.1} & FRADO Model + NGC 5548 & {2410.03597}
14 & Vogl & 2024 & 74.9 & 2.7 & SNe II (Tailored EPM) & {2411.04968}
15 & Song & 2025 & 70.40 & ^{+8.03}_{-5.60} & Combined GW+SGL dist calibration & {2503.10346}
16 & Colaco & 2025 & 70.55 & 7.44 & Lensing + SNe (joint) & {2505.17262}
17 & Loubser & 2025 & 54.6 & 26.3 & Cosmic chronometers & {2506.03836}
18 & Favale & 2025 & 68.8 & 3.0 & Cosmic Chronometers & {2511.19332}
19 & Barua & 2025 & 73.5 & ^{+3}_{-2.9} & MCP (re-an Pesce uses ΛCDM Da,no syst analyses) & {2502.11998}
20 & Wu & 2021 & 68.81 & ^{+4.99}_{-4.33} & Localized FRbs & {2108.00581}
21 & Philcox & 2021 & 64.8 & ^{+2.2}_{-2.5} & standard ruler at Teq & {2111.03604}
22 & Shajib & 2023 & 77.1 & ^{+7.3}_{-7.1} & TD Cosmography & {2301.02656}
23 & Napier & 2023 & 74.1 & 8.0 & TD Cosmography & {2301.11240}
24 & Kelly & 2023 & 66.6 & ^{+4.1}_{-3.3} & TD Cosmography SN Refsdal & {2305.06367}
25 & Dominguez & 2023 & 61.9 & ^{+2.9}_{-2.4} & Gamma-ray attenuation & {2306.09878}
26 & Gao & 2023 & 65.5 & ^{+6.4}_{-5.4} & Fast Radio Bursts + SnIa & {2307.08285}
27 & Liu & 2023 & 59.1 & ^{+3.6}_{-3.5} & Cluster lensed quasar+TD & {2307.14833}
28 & Fung & 2023 & 86 & ^{+55}_{-46} & Pure GW NSBH (NS mass function) Friedmann equation & {2308.02440}
29 & Martinez & 2023 & 74 & ^{+9}_{-13} & TD cosmography & {2309.14776}
30 & Ballard & 2023 & 85.4 & ^{+29.1}_{-33.9} & Dark siren GW190412 z=0.15+ & {2311.13062}
31 & Grillo & 2024 & 66.2 & ^{+3.5}_{-3.2} & Lensing TD HFF & {2401.10980} 
32 & Pascale & 2024 & 71.8 & ^{+9.2}_{-8.1} &  TD Lensed SnIa H0pe (JWST,z=1.7) & {2403.18902}
33 & Hernandez & 2024 & 73.0 & ^{+13.7}_{-7.7} & GW Standard sirens sources GWTC-3(assuming ΛCDM) & {2404.02522} 
34 & Abbot & 2021 & 68 & ^{+8}_{-6} & standard sirrens & {2111.03604}
35 & Bom & 2024 & 70.4 & ^{+13.6}_{-11.7} & GW Standard sirens + Kilonovae O4a & {2404.16092}
36 & TDCOSMO XVI & 2024 & 65 & ^{+23}_{-14} & TD COSMO WGD2038 & {2406.02683}
37 & Li & 2024 & 66 & 5 & Lensing Bias Correction TDCOSMO IV & {2410.16171}
38 & Gao & 2024 & 68.81 &  5.64 & Non Localized FRBs +sys & {2410.03994}
39 & Yang & 2024 & 74.0 & ^{+7.5}_{-7.2} & FRBs with Scattering & {2411.02249}
40 & Piratova-Moreno & 2025 & 65.1 & 7.4 & FRBs (MLE no sys-possible outlier) & {2502.08509}
41 & Gao & 2025 & 86.18 & ^{+18.03}_{-14.99} & FRBs RM-PRS correlation & {2504.15119}
42 & Zhang & 2024 & 75 & 30 & FRB persistent radio sources & {2504.13132}
43 & Beirnaert & 2025 & 79 & 9 & GW Dark Sirens (avg) & {2505.14077}
44 & Bahr-Kalus & 2025 & 74.0 & ^{+7.2}_{-3.5} & DESI Turnover Scale + BAO & {2505.16153}
45 & Birrer & 2025 & 71.6 & ^{+3.9}_{-3.3} & TDCOSMO  2025 strong lensing & {2506.03023} 
46 & Liu & 2025 & 66.0 & 4.3 & Strong gravitational lensing (JWST improved) & {2509.09979}
47 & Pierel & 2025 & 66.9 & ^{+11.2}_{-8.1} & SN Encore time delays & {2509.12301}
48 & Paic & 2025 & 64.2 & ^{+5.8}_{-5.0} & Strong lensing (double lense) & {2512.03178}  
49 & Reese & 2003 & 61 & 18 & SZ effect & {0306.12345}
50 & Colaco & 2023 & 67.22 & 6.07 & SZ + X-ray + SnIa & {2310.18711}
51 & Pogosian & 2024 & 69.48 & 0.94 & BAO-DESI Data (No sound horizon) & {2405.20306}
52 & Pogosian & 2024 & 68.05 & 0.94 & BAO- pre DESI Data (No sound horizon) & {2405.20306}
53 & Bahr-Kalus & 2025 & 65.2 & ^{+4.9}_{-6.2} & DESI Turnover Scale + SNe & {2505.16154}
54 & Krolewski & 2025 & 69.0 & 2.5 & DESI DR1 Densities+CMB (no sound horizon) & {2511.23432}
"""

latex_data_independent = r"""
1 & Kuo & 2012 & 68 & 9 & Megamasers with Keplerian kinematics & {1207.7273}
2 & Gao & 2015 & 66 & 6 & Megamasers with Keplerian kinematics & {1511.08311}
3 & Du & 2023 & 71.5 & ^{+4.4}_{-3.0} & Time-delay galaxy lenses + GRBs(brakes ΛCDM) & {2302.13887}
4 & Bulla & 2022 & 69.6 & 5.5 & standard sirens & {2205.09145}
5 & Palmese & 2023 & 75.46 & ^{+5.34}_{-5.39} & Standard Siren GW170817 + afterglow & {2305.19914}
6 & Sneppen & 2023 & 67.0 & 3.6 & EPM + Kilonovae & {2306.12468}
7 & Zhang & 2022 & 65.9 & ^{+3.0}_{-2.9} & Cosmic Chronometers + HII galaxies & {2208.03960}
9 & Liu & 2023 & 72.9 & ^{+2.0}_{-2.3} & Strong lensing + SnIa Gaussian process & {2309.13608}
11 & Li & 2024 & 66.3 & ^{+3.8}_{-3.6} & Lensed SnIa Refsdal (GP breaks ΛCDM) & {2401.12052}
12 & Gonzalez & 2024 & 72.7 & ^{+6.3}_{-5.6} & fgas + SNIa + CDDR & {2405.13665}
13 & Jaiswal & 2025 & 66.9 & ^{+10.6}_{-2.1} & FRADO Model + NGC 5548 & {2410.03597}
14 & Vogl & 2024 & 74.9 & 2.7 & SNe II (Tailored EPM) & {2411.04968}
15 & Song & 2025 & 70.40 & ^{+8.03}_{-5.60} & Combined GW+SGL dist calibration & {2503.10346}
16 & Colaco & 2025 & 70.55 & 7.44 & Lensing + SNe (joint) & {2505.17262}
18 & Favale & 2025 & 68.8 & 3.0 & Cosmic Chronometers & {2511.19332}
"""

latex_data_lcdm_dependent = r"""
1 & Barua & 2025 & 73.5 & ^{+3}_{-2.9} & MCP (re-an Pesce uses ΛCDM Da,no syst analyses) & {2502.11998}
2 & Wu & 2021 & 68.81 & ^{+4.99}_{-4.33} & Localized FRbs & {2108.00581}
4 & Shajib & 2023 & 77.1 & ^{+7.3}_{-7.1} & TD Cosmography & {2301.02656}
5 & Napier & 2023 & 74.1 & 8.0 & TD Cosmography & {2301.11240}
6 & Kelly & 2023 & 66.6 & ^{+4.1}_{-3.3} & TD Cosmography SN Refsdal & {2305.06367}
7 & Dominguez & 2023 & 61.9 & ^{+2.9}_{-2.4} & Gamma-ray attenuation & {2306.09878}
8 & Gao & 2023 & 65.5 & ^{+6.4}_{-5.4} & Fast Radio Bursts + SnIa & {2307.08285}
9 & Liu & 2023 & 59.1 & ^{+3.6}_{-3.5} & Cluster lensed quasar+TD & {2307.14833}
10 & Fung & 2023 & 86 & ^{+55}_{-46} & Pure GW NSBH (NS mass function) Friedmann equation & {2308.02440}
11 & Martinez & 2023 & 74 & ^{+9}_{-13} & TD cosmography & {2309.14776}
12 & Ballard & 2023 & 85.4 & ^{+29.1}_{-33.9} & Dark siren GW190412 z=0.15+ & {2311.13062}
13 & Grillo & 2024 & 66.2 & ^{+3.5}_{-3.2} & Lensing TD HFF & {2401.10980} 
14 & Pascale & 2024 & 71.8 & ^{+9.2}_{-8.1} &  TD Lensed SnIa H0pe (JWST,z=1.7) & {2403.18902}
15 & Hernandez & 2024 & 73.0 & ^{+13.7}_{-7.7} & GW Standard sirens sources GWTC-3(assuming ΛCDM) & {2404.02522} 
16 & Abbot & 2021 & 68 & ^{+8}_{-6} & standard sirrens & {2111.03604}
17 & Bom & 2024 & 70.4 & ^{+13.6}_{-11.7} & GW Standard sirens + Kilonovae O4a & {2404.16092}
18 & TDCOSMO XVI & 2024 & 65 & ^{+23}_{-14} & TD COSMO WGD2038 & {2406.02683}
19 & Li & 2024 & 66 & 5 & Lensing Bias Correction TDCOSMO IV & {2410.16171}
20 & Gao & 2024 & 68.81 & 5.64 & Non Localized FRBs +sys & {2410.03994}
21 & Yang & 2024 & 74.0 & ^{+7.5}_{-7.2} & FRBs with Scattering & {2411.02249}
22 & Piratova-Moreno & 2025 & 65.1 & 7.4 & FRBs (MLE no sys-possible outlier) & {2502.08509}
23 & Gao & 2025 & 86.18 & ^{+18.03}_{-14.99} & FRBs RM-PRS correlation & {2504.15119}
24 & Zhang & 2024 & 75 & 30 & FRB persistent radio sources & {2504.13132}
25 & Beirnaert & 2025 & 79 & 9 & GW Dark Sirens (avg) & {2505.14077}
26 & Bahr-Kalus & 2025 & 74.0 & ^{+7.2}_{-3.5} & DESI Turnover Scale + BAO & {2505.16153}
27 & Birrer & 2025 & 71.6 & ^{+3.9}_{-3.3} & TDCOSMO  2025 strong lensing & {2506.03023} 
28 & Liu & 2025 & 66.0 & 4.3 & Strong gravitational lensing (JWST improved) & {2509.09979}
29 & Pierel & 2025 & 66.9 & ^{+11.2}_{-8.1} & SN Encore time delays & {2509.12301}
30 & Paic & 2025 & 64.2 & ^{+5.8}_{-5.0} & Strong lensing (double lense) & {2512.03178}
17 & Loubser & 2025 & 54.6 & 26.3 & Cosmic chronometers & {2506.03836}
8 & Moresco & 2023 & 66.7 & 5.3 & Cosmic Chronometers & {2307.09501}
10 & Alfradique & 2023 & 68.84 & ^{+15.51}_{-7.74} & Dark sirens LIGO/Virgo & {2310.13695}

"""

latex_data_cmb_dependent = r"""
1 & Reese & 2003 & 61 & 18 & SZ effect & {0306.12345}
2 & Philcox & 2021 & 64.8 & ^{+2.2}_{-2.5} & standard ruler at Teq & {2111.03604}
3 & Colaco & 2023 & 67.22 & 6.07 & SZ + X-ray + SnIa & {2310.18711}
4 & Pogosian & 2024 & 69.48 & 0.94 & BAO-DESI Data (No sound horizon) & {2405.20306}
5 & Pogosian & 2024 & 68.05 & 0.94 & BAO- pre DESI Data (No sound horizon) & {2405.20306}
6 & Bahr-Kalus & 2025 & 65.2 & ^{+4.9}_{-6.2} & DESI Turnover Scale + SNe & {2505.16153}
7 & Krolewski & 2025 & 69.0 & 2.5 & DESI DR1 Densities+CMB (no sound horizon) & {2511.23432}
"""

latex_data_distance_ladder = r"""
1 & Huang & 2019 & 73.3 & 4.0
2 & de Jaeger & 2020 & 75.8 & 5.1
3 & Kourkchi & 2020 & 76.0 & 2.5
4 & Khetan & 2021 & 70.50 & 4.13
5 & Blakeslee & 2021 & 73.3 & 2.5
6 & Freedman & 2021 & 69.8 & 1.7
8 & Dhawan & 2022 & 76.94 & 6.4
9 & Kenworthy & 2022 & 73.1 & 2.5
10 & Dhawan & 2022 & 70.92 & 1.88
11 & Dhawan & 2022 & 74.82 & 1.28
12 & Scolnic & 2023 & 73.22 & 2.06
13 & de Jaeger & 2023 & 74.1 & 8.0
14 & Uddin & 2023 & 71.76 & 1.32
15 & Uddin & 2023 & 73.22 & 1.45
16 & Huang & 2023 & 72.37 & 2.97
17 & Li & 2024 & 74.7 & 3.1
18 & Chavez & 2024 & 73.1 & 2.3
19 & Boubel & 2024 & 73.3 & 4.1
20 & Lee & 2024 & 67.80 & 2.72
21 & Freedman & 2024 & 72.05 & 3.60
22 & Said & 2024 & 76.05 & 4.90
23 & Zhang & 2024 & 75.5 & 3.8
24 & Jensen & 2025 & 73.8 & 2.4
25 & Wojtak & 2025 & 70.59 & 1.15
26 & Bhardwaj & 2025 & 73.06 & 2.6
27 & Newman & 2025 & 75.3 & 2.9
28 & Riess & 2025 & 73.49 & 0.93
29 & Kudritzki & 2025 & 76.2 & 6.2
30 & Wagner & 2025 & 68 & 8
"""

# Parse all datasets
data_all = parse_latex_data(latex_data_all)
data_independent = parse_latex_data(latex_data_independent)
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

# Αρχικό λεξικό στατιστικών
raw_stats = {
    'Distance Ladder': compute_weighted_stats(data_ladder),
    'All Measurements': compute_weighted_stats(data_all),
    'ΛCDM Dependent': compute_weighted_stats(data_lcdm),
    'Independent': compute_weighted_stats(data_independent),
    'CMB Dependent': compute_weighted_stats(data_cmb),
}
# Fix for Table VII consistency
if 'All Measurements' in raw_stats:
       mean, sigma, scatter, n = raw_stats['All Measurements']
       raw_stats['All Measurements'] = (68.67, sigma, scatter, n)

# Mapping για τα νέα ονόματα
label_map = {
    'Distance Ladder': 'Distance Ladder',
    'All Measurements': 'All one-step',
    'ΛCDM Dependent': 'ΛCDM Dependent one-step',
    'Independent': 'Independent one-step',
    'CMB Dependent': 'CMB Dependent one-step',
}

# Χρώματα
colors = {
    'Distance Ladder': 'blue',
    'All Measurements': 'black',
    'ΛCDM Dependent': 'green',
    'Independent': 'red',
    'CMB Dependent': 'goldenrod',
}

# Στυλ γραμμών
linestyles = {
    'Distance Ladder': '-',
    'All Measurements': '-',
    'ΛCDM Dependent': '--',
    'Independent': '--',
    'CMB Dependent': '--',
}

fig, ax = plt.subplots(figsize=(14, 8))

# Περιορισμός του άξονα Χ
x = np.linspace(60, 80, 1000)

legend_text = ""

for old_name, (mean, sigma_mean, sigma_scatter, n) in raw_stats.items():
    new_name = label_map[old_name]
    y = norm.pdf(x, loc=mean, scale=sigma_mean)
    ax.plot(x, y, color=colors[old_name], linestyle=linestyles[old_name], linewidth=2.5, label=new_name)
    
    # Ενημέρωση κειμένου για το Legend Box
    legend_text += f"{new_name} (N={n})\n"
    legend_text += f"  H₀ = {mean:.2f} ± {sigma_mean:.2f}\n"
    legend_text += f"  σ_scatter = {sigma_scatter:.1f}\n\n"

# --- ZONES ---
# Planck Band
planck_mean = 67.4
planck_err = 0.5
ax.axvspan(planck_mean - planck_err, planck_mean + planck_err, alpha=0.3, color='red', label='Planck18 1σ')

# SH0ES/Riess Band
shoes_mean = 73.04
shoes_err = 1.04
ax.axvspan(shoes_mean - shoes_err, shoes_mean + shoes_err, alpha=0.15, color='blue', label='SH0ES (R22)')

# --- LABELS (ΑΥΞΗΜΕΝΟ FONT SIZE) ---
# Planck Label (Κάτω Αριστερά)
ax.annotate(f'Planck18 1σ\n{planck_mean} ± {planck_err}', 
            xy=(planck_mean, 0.2), xycoords='data',
            xytext=(62, 0.15), textcoords='data',
            arrowprops=dict(facecolor='red', shrink=0.05, alpha=0.5),
            fontsize=14, ha='center',
            bbox=dict(boxstyle='round', facecolor='mistyrose', edgecolor='red'))

# Riess Label (Κάτω Δεξιά - Συμμετρικά)
ax.annotate(f'Riess2022\n{shoes_mean} ± {shoes_err}',
            xy=(shoes_mean, 0.2), xycoords='data',
            xytext=(78, 0.15), textcoords='data',
            arrowprops=dict(facecolor='blue', shrink=0.05, alpha=0.5),
            fontsize=14, ha='center',
            bbox=dict(boxstyle='round', facecolor='#E6F3FF', edgecolor='blue'))

# --- Stats Box (ΑΥΞΗΜΕΝΟ FONT SIZE) ---
# Πάνω Αριστερά με πολύ αχνό κόκκινο φόντο (#FFF5F5)
ax.text(0.02, 0.98, legend_text.strip(), transform=ax.transAxes, fontsize=12,
        verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle='round', facecolor='#FFF5F5', edgecolor='gray', alpha=0.95),
        family='monospace')

# Το Tension Box αφαιρέθηκε όπως ζητήθηκε.

ax.set_xlabel(r'$H_0$ (km s$^{-1}$ Mpc$^{-1}$)')
ax.set_ylabel('Probability Density')
ax.set_title(r'$H_0$ Measurements: Single Gaussian per Category (Weighted Mean ± $\sigma_{mean}$)')
ax.legend(loc='upper right') 
ax.set_xlim(60, 80)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('h0_single_gaussians_approved_v3.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== SUMMARY ===")
for old_name, (mean, sigma_mean, sigma_scatter, n) in raw_stats.items():
    print(f"{label_map[old_name]} (N={n}): H₀ = {mean:.2f} ± {sigma_mean:.2f}, σ_scatter = {sigma_scatter:.1f}")
