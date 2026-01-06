# Hubble Tension Analysis: Sound-Horizon-Independent H₀ Measurements

[![DOI](https://img.shields.io/badge/arXiv-2601.00650-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the data and analysis scripts accompanying the paper:

**"Dissecting the Hubble tension: Insights from a diverse set of Sound Horizon-free H₀ measurements"**

by Ioannis Pantos and Leandros Perivolaropoulos

Department of Physics, University of Ioannina, Greece

---

## Abstract

We analyze 83 Sound-Horizon-independent H₀ measurements categorized into four classes:
- **Category 1**: Distance Ladder (29 measurements)
- **Category 2**: Local One-Step ΛCDM (32 measurements)
- **Category 3**: Pure Local One-Step (15 measurements)
- **Category 4**: CMB Sound Horizon Free (7 measurements)

Our analysis reveals a **6.7σ tension** between the Distance Ladder (H₀ = 72.74 ± 0.40 km s⁻¹ Mpc⁻¹) and combined One-Step measurements (H₀ = 68.67 ± 0.46 km s⁻¹ Mpc⁻¹).

---

## Repository Contents

```
├── scripts/
│   ├── h0_single_gaussians.py    # Figure 2: Single Gaussian per category
│   ├── h0_pdf_plot.py            # Figure 3: Distance Ladder vs One-Step
│   └── h0_bimodality.py          # Figure 4: Bimodality analysis
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Requirements

- Python 3.8+
- NumPy
- Matplotlib
- SciPy

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

### Generate Figure 2 (Category Distributions)
```bash
python scripts/h0_single_gaussians.py
```

### Generate Figure 3 (Distance Ladder vs One-Step)
```bash
python scripts/h0_pdf_plot.py
```

### Generate Figure 4 (Bimodality Analysis)
```bash
python scripts/h0_bimodality.py
```

---

## Key Results

| Category | N | H₀ (km s⁻¹ Mpc⁻¹) | χ²/dof | Tension vs Cat. 1 |
|----------|---|-------------------|--------|-------------------|
| 1. Distance Ladder | 29 | 72.74 ± 0.40 | 0.74 | — |
| 2. Local One-Step (ΛCDM) | 32 | 67.59 ± 0.98 | 0.84 | 4.9σ |
| 3. Pure Local One-Step | 15 | 70.38 ± 1.00 | 0.78 | 2.2σ |
| 4. CMB Sound Horizon Free | 7 | 68.44 ± 0.61 | 0.73 | 5.9σ |
| **Combined (2+3+4)** | **54** | **68.67 ± 0.46** | **0.85** | **6.7σ** |

---

## Citation

If you use this code or data, please cite:
```bibtex
@article{Pantos2026,
  author = {Pantos, Ioannis and Perivolaropoulos, Leandros},
  title = {Dissecting the Hubble tension: Insights from a diverse set of Sound Horizon-free H₀ measurements},
  journal = {arXiv preprint},
  year = {2026},
  eprint = {2601.00650},
  archivePrefix = {arXiv},
  primaryClass = {astro-ph.CO}
}
```

---

## Contact

- Ioannis Pantos: [i.pantos@uoi.gr](mailto:i.pantos@uoi.gr)
- Leandros Perivolaropoulos: [leandros@uoi.gr](mailto:leandros@uoi.gr)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
