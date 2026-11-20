# PorosityP

## Correlating Emulsion Optical Properties with the Percolation in Solvent-Cast PLA/PVP Membranes

This repository contains the data processing and visualization scripts used to obtain the figures and statistical results for the paper *"Correlating Emulsion Optical Properties with the Percolation in Solvent-Cast PLA/PVP Membranes"*.

## Repository Structure

* **`data` (`porogen_content` and CSV files)** — Raw experimental datasets archived in an external Zenodo repository: [DOI: 10.5281/zenodo.22864555].
* **`scripts`** — Independent scripts and notebooks for data processing and figure plotting, [GitHub](https://github.com/IbragimovAlmaz/PorosityP):
  * **Surface porosity analysis:** `pores_preprocessing.py`, `pore_areas.py`, `cumulative_porosity.py` (requires `combined_porogen_data.csv`, processed from raw `porogen_content` images via manual FIJI/ImageJ thresholding).
  * **Volumetric porosity analysis:** `volumetric-porosity.py` (contains embedded calculated data from gravimetric measurements).
  * **Basic optical density processing:** `curves_od.py`, `od800.py` (requires `spectroturbidimetry.csv`).
  * **Wavelength exponent estimation:** `od-lambda-heller.py` (requires `spectroturbidimetry.csv`), `alpha_calculation.ipynb` (contains pre-calculated $\alpha$ values for statistical analysis and plotting).
  * **Franz cell permeation assays:** `franz_auto.py` (requires `FranzPLA75_n123.csv`, `FranzPLA80_n123.csv`, `FranzPLA85_n123.csv` and processes them into final tables), `plotting_franz.py` (requires the processed CSV outputs from `franz_auto.py`).

## Requirements

The code was tested with **Python 3.9**. To install all required dependencies, run:

```bash
pip install -r requirements.txt
```
Alternatively, install the core libraries via `pip`:
```bash
pip install numpy pandas scikit-learn scipy pingouin scikit-posthocs statannotations matplotlib seaborn plotly
```

## Usage

1. Download the porogen_content and `.csv` dataset files from the Zenodo archive linked above and place them in the same directory as the scripts.
2. Run any script or notebook independently to reproduce the corresponding figures and statistical analyses.

`Note:` Please note that some of the images in the `porogen_content` dataset were made after the ModuleSci software (PICO SMART PE) update.
