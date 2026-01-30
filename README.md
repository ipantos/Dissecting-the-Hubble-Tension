# Hubble Tension Analysis: Sound-Horizon-Independent H₀ Measurements (Version 2)

[![DOI](https://img.shields.io/badge/arXiv-2601.00650-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the data and analysis scripts accompanying the updated paper (Version 2):

**"Dissecting the Hubble tension: Insights from a diverse set of Sound Horizon-free H₀ measurements"**

by Ioannis Pantos and Leandros Perivolaropoulos  
Department of Physics, University of Ioannina, Greece

---

## 📝 Abstract

In this updated analysis (Version 2), we incorporate **88 Sound-Horizon-independent H₀ measurements** (5 additional measurements compared to Version 1). The data are categorized into four primary classes:
- **Category 1**: Distance Ladder
- **Category 2**: Local One-Step ΛCDM
- **Category 3**: Pure Local One-Step
- **Category 4**: CMB Sound Horizon Free

Our results confirm a persistent and significant tension (approx. 6.7σ) between the Distance Ladder and combined One-Step/CMB-free measurements.

---

## 📊 Methodology & Key Innovations

This version introduces refined statistical checks and responds to feedback regarding categorization:

*   **Gaussian Kernel Density Estimation (KDE):** Construction of probability density functions (PDFs) for heterogeneous datasets.
*   **Reduced Bandwidth KDE:** Specifically implemented in `h0_bimodality_kde.py` to highlight the underlying bimodal nature of the One-Step distribution.
*   **Sensitivity Analysis:** A new diagnostic script (`h0_sensitivity_analysis.py`) to evaluate the robustness of our conclusions against variations in measurement categorization.
*   **Statistical Weighting:** Full incorporation of individual measurement errors to represent the statistical weight of each data point accurately.

---

## 📂 Repository Contents

```text
├── scripts/
│   ├── h0_single_gaussians.py      # Figure 2: Updated Category Distributions (88 measurements)
│   ├── h0_pdf_plot.py              # Figure 3: Distance Ladder vs One-Step Comparison
│   ├── h0_bimodality_kde.py        # Figure 4: Refined KDE Bimodality Analysis (Reduced Bandwidth)
│   └── h0_sensitivity_analysis.py  # New: Sensitivity check for data categorization
├── requirements.txt                 # Python dependencies
└── README.md                        # This file

pip install -r requirements.txt
python scripts/h0_single_gaussians.py
python scripts/h0_bimodality_kde.py
@article{Pantos2026_v2,
  author = {Pantos, Ioannis and Perivolaropoulos, Leandros},
  title = {Dissecting the Hubble tension: Insights from a diverse set of Sound Horizon-free H₀ measurements},
  journal = {arXiv preprint},
  year = {2026},
  eprint = {2601.00650},
  note = {Version 2 with 88 measurements},
  archivePrefix = {arXiv},
  primaryClass = {astro-ph.CO}
}
