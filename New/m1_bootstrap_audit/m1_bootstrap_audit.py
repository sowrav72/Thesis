
import numpy as np
import pandas as pd
from pathlib import Path

# Change this to your downloaded CSV path
INPUT = "m1_per_child_primary.csv"
OUTDIR = Path("m1_bootstrap_audit")

B = 20000
SEED = 20261021

df = pd.read_csv(INPUT)

required = {
    "model", "pair", "fold",
    "C_M0", "N2_M0", "C_M1", "N2_M1"
}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing columns: {missing}")

if df[["C_M0", "N2_M0", "C_M1", "N2_M1"]].isna().any().any():
    raise ValueError("Missing values found in the primary columns.")

groups = list(df.groupby(["model", "pair"], sort=True))

if len(groups) != 7:
    raise ValueError(
        f"Expected 7 model/pair groups, found {len(groups)}"
    )

results = []
fold_results = []

for cell_number, ((model, pair), data) in enumerate(groups):
    data = data.copy().reset_index(drop=True)

    # One paired effect per child
    effect = (
        (data["C_M1"] - data["N2_M1"])
        - (data["C_M0"] - data["N2_M0"])
    ).to_numpy(dtype=float)

    if not np.isfinite(effect).all():
        raise ValueError(f"Non-finite values in {model}, {pair}")

    folds = data["fold"].to_numpy()
    fold_values = [
        effect[folds == f]
        for f in sorted(data["fold"].unique())
    ]

    if len(fold_values) != 5 or any(len(x) == 0 for x in fold_values):
        raise ValueError(f"Unexpected fold structure in {model}, {pair}")

    estimate = effect.mean()
    rng = np.random.RandomState(SEED + cell_number * 10)

    # Method A: pooled-child bootstrap
    pooled = np.empty(B)
    for b in range(B):
        idx = rng.randint(0, len(effect), size=len(effect))
        pooled[b] = effect[idx].mean()

    # Method B: resample within each fold
    stratified = np.empty(B)
    strat_rng = np.random.RandomState(SEED + cell_number * 10 + 1)

    for b in range(B):
        sampled = []
        for values in fold_values:
            idx = strat_rng.randint(0, len(values), size=len(values))
            sampled.extend(values[idx])
        stratified[b] = np.mean(sampled)

    # Ordinary 95% intervals
    pooled_ci = np.quantile(pooled, [0.025, 0.975])
    strat_ci = np.quantile(stratified, [0.025, 0.975])

    # Bonferroni-adjusted intervals across 7 primary comparisons
    alpha = 0.05 / len(groups)
    pooled_adj = np.quantile(
        pooled, [alpha / 2, 1 - alpha / 2]
    )
    strat_adj = np.quantile(
        stratified, [alpha / 2, 1 - alpha / 2]
    )

    results.append({
        "model": model,
        "pair": pair,
        "estimate": estimate,
        "pooled_ci95_low": pooled_ci[0],
        "pooled_ci95_high": pooled_ci[1],
        "stratified_ci95_low": strat_ci[0],
        "stratified_ci95_high": strat_ci[1],
        "pooled_adjusted_low": pooled_adj[0],
        "pooled_adjusted_high": pooled_adj[1],
        "stratified_adjusted_low": strat_adj[0],
        "stratified_adjusted_high": strat_adj[1],
    })

    for fold, values in zip(
        sorted(data["fold"].unique()), fold_values
    ):
        fold_results.append({
            "model": model,
            "pair": pair,
            "fold": fold,
            "n_children": len(values),
            "fold_effect": values.mean(),
        })

OUTDIR.mkdir(exist_ok=True)

results_df = pd.DataFrame(results)
folds_df = pd.DataFrame(fold_results)

results_df.to_csv(
    OUTDIR / "m1_bootstrap_sensitivity_results.csv", index=False
)
folds_df.to_csv(
    OUTDIR / "m1_bootstrap_fold_estimates.csv", index=False
)

print("\nBOOTSTRAP SENSITIVITY RESULTS")
print(results_df.round(5).to_string(index=False))

print("\nFOLD-SPECIFIC ESTIMATES")
print(folds_df.round(5).to_string(index=False))

print("\nSaved results to:", OUTDIR.resolve())
