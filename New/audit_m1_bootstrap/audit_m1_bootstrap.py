#!/usr/bin/env python3
"""Fold-stratified bootstrap sensitivity audit for M1. Non-destructive."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

DEFAULT = Path('result/bdhs_xai_m1_shared_reference_v1_1/m1_per_child_primary.csv')
B = 20000
SEED = 20261022
ALPHA = 0.05
PAIRS = [
    ('LR', 'SHAP vs LIME'), ('LR', 'SHAP vs IG'), ('LR', 'LIME vs IG'),
    ('RF', 'SHAP vs LIME'), ('MLP', 'SHAP vs LIME'),
    ('MLP', 'SHAP vs IG'), ('MLP', 'LIME vs IG'),
]
REQUIRED = {'model','pair','fold','C_M0','N2_M0','C_M1','N2_M1','C_C1','N2_C1'}


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not src.exists():
        raise FileNotFoundError(f'Cannot find {src}. Run from repo root or pass the CSV path.')
    df = pd.read_csv(src)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    df['fold'] = pd.to_numeric(df['fold'], errors='raise')
    numeric = ['C_M0','N2_M0','C_M1','N2_M1','C_C1','N2_C1']
    df[numeric] = df[numeric].apply(pd.to_numeric, errors='raise')
    if df[numeric].isna().any().any():
        raise ValueError('Missing numeric values in required columns.')

    print(f'Input CSV: {src}\nTotal rows: {len(df)}')
    print('\nRows per model/pair:')
    print(df.groupby(['model','pair']).size().to_string())
    print('\nRows per fold within each model/pair:')
    print(df.groupby(['model','pair','fold']).size().to_string())

    # Bonferroni-adjusted percentile intervals across the seven planned comparisons.
    tail = ALPHA / (2 * len(PAIRS))
    results, folds_out = [], []
    for idx, (model, pair) in enumerate(PAIRS):
        g = df[(df.model == model) & (df.pair == pair)].copy()
        if g.empty:
            raise ValueError(f'Missing expected group: {model} / {pair}')
        sizes = g.groupby('fold').size()
        if len(sizes) != 5 or not (sizes == 40).all():
            print(f'WARNING {model}/{pair}: fold sizes {sizes.to_dict()} (expected five folds × 40).')

        # Per-row delta: (C-N2) in M1 minus (C-N2) in M0.
        fold_deltas = []
        for fold, part in g.groupby('fold', sort=True):
            d = ((part.C_M1 - part.N2_M1) - (part.C_M0 - part.N2_M0)).to_numpy(float)
            d = d[np.isfinite(d)]
            if len(d) == 0:
                raise ValueError(f'No finite values for {model}/{pair}, fold {fold}')
            fold_deltas.append((fold, d))
            folds_out.append({'model': model, 'pair': pair, 'fold': fold,
                              'n_rows': len(d), 'mean_delta_fold': float(d.mean())})

        # Stratified resampling: preserve each fold's sample size and weight folds equally.
        rng = np.random.default_rng(SEED + idx)
        boot_fold_means = []
        for _, d in fold_deltas:
            sampled = rng.integers(0, len(d), size=(B, len(d)))
            boot_fold_means.append(d[sampled].mean(axis=1))
        boot = np.vstack(boot_fold_means).mean(axis=0)
        point = float(np.mean([d.mean() for _, d in fold_deltas]))
        lo95, hi95 = np.quantile(boot, [ALPHA/2, 1-ALPHA/2])
        lo_adj, hi_adj = np.quantile(boot, [tail, 1-tail])
        results.append({
            'model': model, 'pair': pair, 'delta_mean_fold_weighted': point,
            'bootstrap_ci95': f'[{lo95:.6f}, {hi95:.6f}]',
            'bonferroni_adjusted_ci': f'[{lo_adj:.6f}, {hi_adj:.6f}]',
            'adjusted_ci_low': float(lo_adj), 'adjusted_ci_high': float(hi_adj),
            'bootstrap_replicates': B, 'seed': SEED + idx,
        })

    out1 = src.parent / 'm1_bootstrap_sensitivity_results_recomputed.csv'
    out2 = src.parent / 'm1_bootstrap_fold_estimates_recomputed.csv'
    pd.DataFrame(results).to_csv(out1, index=False)
    pd.DataFrame(folds_out).to_csv(out2, index=False)
    print(f'\nSaved results: {out1}')
    print(f'Saved fold estimates: {out2}')
    print('\nCaution: this assumes each row is correctly paired across M0 and M1.')
    print('The CSV has no child ID, so row alignment must be confirmed from notebook construction.')
    print('This bootstrap does not propagate reference-draw uncertainty.')

if __name__ == '__main__':
    main()
