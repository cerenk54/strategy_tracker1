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

## 1️⃣ Install dependencies

pip install numpy pandas matplotlib scipy

---

## 2️⃣ Prepare Your Dataset

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

If your dataset is in MATLAB (.mat) format:
In MATLAB run the following;

from scipy.io import loadmat  
import pandas as pd  

data = loadmat("your_file.mat")  

Convert the relevant structure into a pandas DataFrame, then save as CSV and use normally. 

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
- Omission trials must be removed or handled before analysis  
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
MSc Neuroscience  
University of Nottingham  

