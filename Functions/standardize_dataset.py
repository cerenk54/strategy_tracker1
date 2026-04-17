def standardize_dataset(df, column_mapping=None):
    """
    Fully user-friendly standardization.

    1) Optionally rename columns using column_mapping
    2) Ensure required columns exist
    3) Convert numeric encodings to toolbox standard format:
       Choice -> 'left'/'right'
       CuePosition -> 'left'/'right'
       Reward -> 'yes'/'no'

    NOTE:
    If your dataset is a .mat file, load it first using:
        from scipy.io import loadmat
        data = loadmat("your_file.mat")
    Then convert the relevant structure to a pandas DataFrame
    before passing it to this function.
    """

    # -----------------------------------------
    # 1) Optional column renaming
    # -----------------------------------------
    if column_mapping is not None:
        df = df.rename(columns=column_mapping)

    required_columns = ["TrialIndex", "Choice", "CuePosition", "Reward"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Dataset must contain column '{col}' after renaming.\n"
                f"Current columns: {list(df.columns)}"
            )

    # -----------------------------------------
    # 2) Standardize Choice
    # -----------------------------------------
    unique_vals = set(df["Choice"].dropna().unique())
    if not unique_vals.issubset({"left", "right", "omission", "Omission", "OMISSION"}):
        if unique_vals.issubset({0, 1}):
            df["Choice"] = df["Choice"].map({0: "left", 1: "right"})
        elif unique_vals.issubset({1, 2}):
            df["Choice"] = df["Choice"].map({1: "left", 2: "right"})
        else:
            raise ValueError(
                f"Unsupported numeric encoding in 'Choice': {unique_vals}"
            )

    # -----------------------------------------
    # 3) Standardize CuePosition
    # -----------------------------------------
    unique_vals = set(df["CuePosition"].dropna().unique())
    if not unique_vals.issubset({"left", "right"}):
        if unique_vals.issubset({0, 1}):
            df["CuePosition"] = df["CuePosition"].map({0: "left", 1: "right"})
        elif unique_vals.issubset({1, 2}):
            df["CuePosition"] = df["CuePosition"].map({1: "left", 2: "right"})
        else:
            raise ValueError(
                f"Unsupported numeric encoding in 'CuePosition': {unique_vals}"
            )

    # -----------------------------------------
    # 4) Standardize Reward
    # -----------------------------------------
    unique_vals = set(df["Reward"].dropna().unique())
    if not unique_vals.issubset({"yes", "no"}):
        if unique_vals.issubset({0, 1}):
            df["Reward"] = df["Reward"].map({0: "no", 1: "yes"})
        else:
            raise ValueError(
                f"Unsupported numeric encoding in 'Reward': {unique_vals}"
            )

    # -----------------------------------------
    # 5) Remove omission trials
    # -----------------------------------------
    omission_mask = df["Choice"].isin(["omission", "Omission", "OMISSION"])
    if omission_mask.any():
        n_removed = omission_mask.sum()
        print(f"[standardize_dataset] Removed {n_removed} omission trial(s) from 'Choice'.")
        df = df[~omission_mask].reset_index(drop=True)

    return df
