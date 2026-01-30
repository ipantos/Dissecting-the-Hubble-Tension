import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# --- FONT SETTINGS ---
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 22,     
    'legend.fontsize': 12,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14
})

# --- DATA ---
# Format: (H0_value, sigma) where sigma = sqrt((sigma_plus^2 + sigma_minus^2) / 2)

# ΛCDM-dependent (33 measurements)
data_lcdm = [
    (68.81, 4.67),   # Wu 2021
    (68, 7.07),      # Abbott 2021
    (77.1, 7.20),    # Shajib 2023
    (74.1, 8.0),     # Napier 2023
    (66.6, 3.72),    # Kelly 2023
    (61.9, 2.66),    # Dominguez 2023
    (65.5, 5.92),    # Gao 2023
    (59.1, 3.55),    # Liu 2023a
    (86, 50.70),     # Fung 2023
    (74, 11.18),     # Martinez 2023
    (85.4, 31.59),   # Ballard 2023
    (66.7, 5.3),     # Moresco 2023
    (68.84, 12.26),  # Alfradique 2024
    (66.2, 3.35),    # Grillo 2024
    (71.8, 8.67),    # Pascale 2024
    (73.0, 11.11),   # Hernandez 2024
    (70.4, 12.69),   # Bom 2024
    (65, 19.04),     # TDCOSMO XVI
    (68.81, 5.64),   # Gao 2024
    (66, 5.0),       # Li 2024b
    (74.0, 7.35),    # Yang 2024
    (65.1, 7.4),     # Piratova 2025
    (73.5, 2.95),    # Barua 2025
    (75, 30.0),      # Zhang 2025
    (86.18, 16.58),  # Gao 2025
    (54.6, 26.3),    # Loubser 2025
    (79, 9.0),       # Beirnaert 2025
    (74.0, 5.66),    # Bahr-Kalus 2025
    (71.6, 3.61),    # Birrer 2025
    (66.0, 4.3),     # Liu 2025
    (66.9, 9.77),    # Pierel 2025
    (64.2, 5.42),    # Paic 2025
    (67.9, 4.4),     # Oliveira
]

# Model-independent (16 measurements)
data_indep = [
    (68, 9.0),       # Kuo 2013
    (66, 6.0),       # Gao 2015
    (69.6, 5.5),     # Bulla 2022
    (65.9, 2.95),    # Zhang 2022
    (71.5, 3.77),    # Du 2023
    (75.46, 5.37),   # Palmese 2023
    (67.0, 3.6),     # Sneppen 2023
    (72.9, 2.16),    # Liu 2023b
    (72.7, 5.96),    # Gonzalez 2024
    (66.3, 3.70),    # Li 2024a
    (66.9, 7.64),    # Jaiswal 2024
    (74.9, 2.7),     # Vogl 2024
    (70.40, 6.92),   # Song 2025
    (70.55, 7.44),   # Colaco 2025
    (71.49, 0.94),   # Du 2025
    (68.8, 3.0),     # Favale 2025
]

# --- COMBINE DATA ---
all_data = data_lcdm + data_indep
values = np.array([d[0] for d in all_data])
errors = np.array([d[1] for d in all_data])
categories = ['LCDM'] * len(data_lcdm) + ['Indep'] * len(data_indep)

# --- CALCULATE WEIGHTS ---
weights = 1 / errors**2
weights_norm = weights / np.sum(weights)

# --- WEIGHTED MEANS ---
def weighted_mean(vals, errs):
    w = 1 / errs**2
    return np.sum(w * vals) / np.sum(w)

lcdm_vals = np.array([d[0] for d in data_lcdm])
lcdm_errs = np.array([d[1] for d in data_lcdm])
indep_vals = np.array([d[0] for d in data_indep])
indep_errs = np.array([d[1] for d in data_indep])

mean_lcdm = weighted_mean(lcdm_vals, lcdm_errs)
mean_indep = weighted_mean(indep_vals, indep_errs)

print(f"Weighted mean (ΛCDM):        {mean_lcdm:.2f} km/s/Mpc")
print(f"Weighted mean (Independent): {mean_indep:.2f} km/s/Mpc")
print(f"Separation:                  {abs(mean_indep - mean_lcdm):.2f} km/s/Mpc")

# --- SILVERMAN BANDWIDTH ---
def silverman_bandwidth(values, weights):
    """Calculate Silverman's rule of thumb for weighted data"""
    n_eff = (np.sum(weights))**2 / np.sum(weights**2)
    w_norm = weights / np.sum(weights)
    weighted_mean = np.sum(w_norm * values)
    weighted_var = np.sum(w_norm * (values - weighted_mean)**2)
    weighted_std = np.sqrt(weighted_var)
    
    # Weighted IQR
    sorted_idx = np.argsort(values)
    cumsum = np.cumsum(w_norm[sorted_idx])
    q25_idx = np.searchsorted(cumsum, 0.25)
    q75_idx = np.searchsorted(cumsum, 0.75)
    weighted_iqr = values[sorted_idx[min(q75_idx, len(values)-1)]] - values[sorted_idx[min(q25_idx, len(values)-1)]]
    
    h = 0.9 * min(weighted_std, weighted_iqr / 1.34) * n_eff**(-1/5)
    return h, n_eff

h_silverman, n_eff = silverman_bandwidth(values, weights)
print(f"\nSilverman bandwidth: h = {h_silverman:.2f}")
print(f"Effective sample size: n_eff = {n_eff:.1f}")

# --- KDE FUNCTION ---
def weighted_kde(x, values, weights_norm, bandwidth):
    """Calculate weighted KDE at points x"""
    density = np.zeros_like(x)
    for i, (val, w) in enumerate(zip(values, weights_norm)):
        density += w * np.exp(-0.5 * ((x - val) / bandwidth)**2) / (bandwidth * np.sqrt(2 * np.pi))
    return density

# --- PLOTTING ---
# Choose bandwidth (adjust as needed)
bandwidth = 1.5  # Below Silverman to reveal bimodal structure

x = np.linspace(55, 85, 1000)
density = weighted_kde(x, values, weights_norm, bandwidth)

fig, ax = plt.subplots(figsize=(12, 7))

# Create color gradient for fill
from matplotlib.colors import LinearSegmentedColormap
colors_gradient = ['#3b82f6', '#8b5cf6', '#ef4444']
n_segments = len(x) - 1

# Plot filled area with gradient effect (approximate)
ax.fill_between(x, density, alpha=0.3, color='#8b5cf6')
ax.plot(x, density, color='#7c3aed', linewidth=2.5, label=f'Weighted KDE (h={bandwidth})')

# Reference bands
# Planck
planck_mean, planck_err = 67.4, 0.5
ax.axvspan(planck_mean - planck_err, planck_mean + planck_err, 
           alpha=0.2, color='blue', label=f'Planck ({planck_mean}±{planck_err})')
ax.axvline(planck_mean, color='blue', linestyle='--', linewidth=1.5, alpha=0.7)

# SH0ES
shoes_mean, shoes_err = 73.04, 1.04
ax.axvspan(shoes_mean - shoes_err, shoes_mean + shoes_err, 
           alpha=0.15, color='red', label=f'SH0ES ({shoes_mean}±{shoes_err})')
ax.axvline(shoes_mean, color='red', linestyle='--', linewidth=1.5, alpha=0.7)

# Find and mark peaks
peaks_idx, properties = find_peaks(density, height=max(density)*0.1, distance=20)
peaks_x = x[peaks_idx]
peaks_y = density[peaks_idx]

# Sort peaks by height
sorted_peaks = sorted(zip(peaks_x, peaks_y), key=lambda p: -p[1])[:3]

for i, (px, py) in enumerate(sorted_peaks):
    color = '#3b82f6' if px < 69 else '#ef4444'
    ax.plot(px, py, 'o', markersize=10, color=color, markeredgecolor='white', 
            markeredgewidth=2, zorder=5)
    ax.annotate(f'{px:.1f}', xy=(px, py), xytext=(px, py + max(density)*0.05),
                fontsize=12, fontweight='bold', ha='center', color='#333')

# Data ticks at bottom
for i, (val, cat) in enumerate(zip(values, categories)):
    color = '#3b82f6' if cat == 'LCDM' else '#ef4444'
    ax.plot([val, val], [-max(density)*0.02, -max(density)*0.005], 
            color=color, linewidth=2, alpha=0.7)

# Labels and formatting
ax.set_xlabel(r'$H_0$ (km s$^{-1}$ Mpc$^{-1}$)')
ax.set_ylabel('Probability Density')
ax.set_title(r'Weighted KDE of $H_0$ Measurements (Ladder-Independent-no CMB)')
ax.set_xlim(55, 85)
ax.set_ylim(-max(density)*0.03, max(density)*1.15)

# Legend
ax.legend(loc='upper right', framealpha=0.95)

# Add info text - fontsize increased by 50% (14 -> 18)
info_text = (f'N = {len(values)} (ΛCDM: {len(data_lcdm)}, Indep: {len(data_indep)})\n'
             f'Weighted means: {mean_lcdm:.1f} vs {mean_indep:.1f} km/s/Mpc\n'
             f'Bandwidth: h = {bandwidth} (Silverman: {h_silverman:.2f})')
ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=18,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# Grid
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig('h0_weighted_kde.png', dpi=300, bbox_inches='tight')
plt.savefig('h0_weighted_kde.pdf', bbox_inches='tight')
plt.show()

# --- PRINT SUMMARY ---
print(f"\n{'='*60}")
print("SUMMARY")
print('='*60)
print(f"Bandwidth used: h = {bandwidth}")
print(f"Silverman optimal: h = {h_silverman:.2f}")
print(f"Reduction from optimal: {(h_silverman - bandwidth)/h_silverman*100:.0f}%")
print(f"\nPeaks found at: {[f'{p[0]:.1f}' for p in sorted_peaks]}")
print(f"Number of peaks: {len(sorted_peaks)}")
if len(sorted_peaks) >= 2:
    print(f"\n✓ BIMODAL distribution detected")
else:
    print(f"\n✗ Unimodal distribution")
