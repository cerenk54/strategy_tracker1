# config.py
# Central configuration shared across notebooks

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, "Rat_2.csv")        # user data path
strategy_name ="go_right"        # e.g., "go_left", "go_right", "go_cued", ...
prior_type = "Uniform"           # "Uniform" / "Optimistic" / "Pessimistic"
decay_rate = 0.9                 # 1.0 = no decay, <1.0 discounts older trials
save_output_csv = False          # True if you want to save Output.csv

COLUMN_MAPPING = {
    "trial": "TrialIndex",
    "choice_side": "Choice",
    "cue_side": "CuePosition",
    "rewarded": "Reward"
}

VALUE_MAPPING = {
    "Choice": {0: "left", 1: "right"},
    "CuePosition": {0: "left", 1: "right"},
    "Reward": {0: "no", 1: "yes"}
}