# StrategyTracker (Python)

A user-friendly Python toolbox for Bayesian tracking of behavioural strategies across trials in choice tasks.

Based on the Strategy Tracker paper (eLife):  
https://doi.org/10.7554/eLife.86491  

Tested with Python 3.9+

(A MATLAB version is available here: https://github.com/Humphries-Lab/Bayesian_Strategy_Analysis_MATLAB)

---

# What This Toolbox Does

This toolbox:

- Computes posterior probability of behavioural strategies trial-by-trial  
- Uses Beta-Bernoulli conjugate Bayesian updating  
- Estimates MAP probability and posterior precision  
- Reproduces Figure 1-style multi-strategy analysis  
- Detects learning using three different criteria  
- Automatically standardizes user datasets  
- Is fully config-driven (no need to edit notebooks)

---

# Project Structure

.
├── config.py  
├── strategymodels.py  
├── Convert_matlab_file_to_csv.py  
├── Functions/  
│   ├── standardize_dataset.py  
│   ├── set_Beta_prior.py  
│   ├── update_strategy_posterior_probability.py  
│   ├── Summaries_of_Beta_distribution.py  
│   ├── interpolate_null_trials.py  
│   └── plotSessionStructure.py  
├── NOTEBOOKS/  
│   ├── 1_Demonstrate_Bayesian.ipynb   
│   ├── 2_Replicate_Figure1.ipynb  
│   ├── 3_LearningSequenceCriterion.ipynb 
│   ├── 4_LearningCriteriaComparison.ipynb 
└── README.md  

---

# Quick Start

## 1️⃣ Clone the repository

git clone https://github.com/your-username/strategy_tracker1.git
cd strategy_tracker1

## 2️⃣ Install dependencies

pip install numpy pandas matplotlib scipy

Or if using conda:

conda install numpy pandas matplotlib scipy

---

## 2️⃣ Prepare Your Dataset
To use this toolbox, provide your own dataset as a CSV file and update `data_path` in `config.py`. Place your CSV file in the project folder. If you are using a .mat format, first check the next step.

Your dataset must contain the following columns:

| Column       | Required Format      |
|-------------|---------------------|
| TrialIndex  | integer             |
| Choice      | "left" / "right"    |
| CuePosition | "left" / "right"    |
| Reward      | "yes" / "no"        |

If your dataset uses numeric encodings (e.g. 0/1 or 1/2), the toolbox automatically converts them using:

standardize_dataset()

---

## 📌 Using a .mat file

If your dataset is in MATLAB (.mat) format, use the included conversion script:

**`Convert_matlab_file_to_csv.py`**

Run this script from the terminal:

    python Convert_matlab_file_to_csv.py

A file dialog will open. Select one or more `.mat` files. The script will:

1. Load each `.mat` file (supports both MATLAB v7.3 and older formats)
2. Convert all data structures to tables
3. Save one `.csv` file per data structure in the **same folder as the selected `.mat` file**

The output filename follows the pattern: `<original_name>_<field_name>.csv`

After conversion, place the resulting CSV in the project folder, update `data_path` in `config.py`, and run the notebooks as normal.

**Required packages for conversion** — run this in your terminal before using the script:

    pip install mat73 scipy numpy pandas

---

# Configuration

All parameters are defined in:

config.py

Example:

data_path = "your_dataset.csv"  
prior_type = "Uniform"  
decay_rate = 0.9  

You do NOT need to modify the notebooks.

To run analysis on a new dataset:

1. Place your CSV in the project folder  
2. Change only data_path in config.py  
3. Run the notebooks  

---

# Notebooks
Run the notebooks in order:

## 1️⃣ Demonstrate Bayesian Strategy Analysis

Runs Bayesian updating for a single strategy.  
Outputs:
- MAP probability across trials  
- Posterior precision  

---

## 2️⃣ Replicate Figure 1

Runs multi-strategy analysis.

Outputs:
- Rule strategies (MAP probability)
- Posterior precision
- Exploratory strategies
- Automatic dominant rule detection
- Dynamic session summary

This notebook adapts automatically to the dataset provided.

---

## 3️⃣ Learning Detection

Implements three learning criteria:

Strategy 1 — Sequence Criterion  
First trial where MAP remains above chance (0.5).

Strategy 2 — Sequence + Precision  
Sequence criterion plus precision dominance over competing strategies.

Strategy 3 — Expert Criterion  
Posterior probability excludes chance with high confidence.

Outputs:
- Learning trial for each method  
- Comparison table  
- Visual overlay on MAP plot  

---

# Mathematical Framework

Strategies are modeled using a Beta-Bernoulli conjugate update:

p(θ | data) ~ Beta(α, β)

Where:

α = successes + prior  
β = failures + prior  

MAP estimate:

(α - 1) / (α + β - 2)

Precision reflects posterior confidence.

---

# Supported Strategies

- go_left  
- go_right  
- go_cued  
- win_stay_spatial  
- lose_shift_cued  
- lose_shift_spatial  

Custom strategies can be added to strategymodels.py.

---

# Things To Be Aware Of

- Dataset must represent one session per file  
- Omission trials (Choice = "omission") are automatically removed by `standardize_dataset()`  
- Large raw data files should not be committed to GitHub  

---

# Problems?

Raise an Issue on the GitHub repository with:

- The error message  
- The notebook used  
- A small example of your dataset format  

---

# Author

Ceren Kimyonok  
MSc Computational Neuroscience 
University of Nottingham  

