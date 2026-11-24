# bdhs_helpers.py
# Shared helper code for notebooks N00-N04 (BDHS 2022 stunting XAI thesis, plan v2.2).
# Style rule: plain loops and ifs, no dictionaries, no classes, no comprehensions.
# Every leakage-critical step (fit preprocessing, split, same-record training) lives here
# so that all notebooks use exactly the same code.

import os
import sys
import time
import copy
import hashlib
import platform
import math

import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import log_loss
from sklearn.metrics import brier_score_loss


# ----------------------------------------------------------------------
# 1. FIXED SETTINGS (plan v2.2). Change only after updating the plan.
# ----------------------------------------------------------------------
BASE_DIR = os.environ.get("THESIS_BASE_DIR", "/content/drive/MyDrive/THESIS_V2")
DATA_DIR = BASE_DIR + "/my_dataset"
CODE_DIR = BASE_DIR + "/code"
PRIVATE_DIR = BASE_DIR + "/private"     # row-level files. NEVER share or upload.
OUTPUT_DIR = BASE_DIR + "/outputs"      # aggregate tables only
MODEL_DIR = BASE_DIR + "/models"

KR_FILE = DATA_DIR + "/BDKR81FL.DTA"    # original BDHS 2022 Kids Recode

SEED_SPLIT = 42            # plan 5.1: fixed shuffle seed for StratifiedGroupKFold
N_OUTER_FOLDS = 5          # plan 5.1: five-fold grouped assignment
TEST_FOLD = 0              # DECISION D13: fold 0 is the test fold (fixed before any modelling)
N_DEV_FOLDS = 5            # plan 5.2: five-fold grouped CV inside development partition
ES_SEED = 42               # seed for the inner early-stopping split (MLP only)

STUNTING_CUTOFF = -200     # hw70 is in hundredths of SD: stunted if hw70 < -200
MIN_CAT_COUNT = 30         # rare-category rule, counted on TRAINING rows only

# MLP settings (plan section 6 table: fixed batch size and early-stopping rule)
MLP_BATCH = 64
MLP_MAX_EPOCHS = 100
MLP_PATIENCE = 10
MLP_INIT_SEED = 42          # same initial-weight seed for every MLP variant
MLP_DATA_ORDER_SEED = 2026  # same record order in every epoch for every MLP variant

# Model-selection rule (plan 6.1)
TIE_TOLERANCE = 0.002       # AP difference treated as a tie (pre-declared, editable BEFORE running N04)
LOGLOSS_TIE = 0.0001        # log-loss difference treated as a tie for the "simpler model" rule

RF_N_JOBS = 2
XGB_N_JOBS = 2

# Primary predictors (plan 3.3). The frozen list is saved by N02.
PREDICTORS_DEFAULT = ["b19", "b4", "bord", "b11", "v012", "v106", "v445",
                      "v190", "v025", "v024", "v113", "v116", "v701", "v705"]
NUMERIC_VARS = ["b19", "bord", "v012", "v445"]

# Names that must NEVER be a predictor (plan section 4)
FORBIDDEN_PREDICTORS = ["hw70", "hw71", "hw72", "hw73", "stunted", "row_id", "caseid",
                        "v001", "v002", "v003", "v005", "v021", "v022", "v023",
                        "sample_weight", "exclusion_reason", "fold", "partition",
                        "m14", "m15", "v438"]


# ----------------------------------------------------------------------
# 2. SMALL UTILITIES
# ----------------------------------------------------------------------
def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_all_folders():
    make_folder(BASE_DIR)
    make_folder(DATA_DIR)
    make_folder(CODE_DIR)
    make_folder(PRIVATE_DIR)
    make_folder(OUTPUT_DIR)
    make_folder(MODEL_DIR)


def mount_drive_if_colab():
    # On Colab this mounts Google Drive. Anywhere else it just says so.
    try:
        from google.colab import drive
        drive.mount("/content/drive")
        print("Google Drive mounted.")
    except ImportError:
        print("Not running on Colab. Using BASE_DIR =", BASE_DIR)


def set_all_seeds(seed):
    import random
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.set_num_threads(1)   # one thread keeps CPU results repeatable
    except ImportError:
        pass


def print_environment(notebook_name):
    print("Notebook:", notebook_name)
    print("Python:", sys.version.split()[0], "| OS:", platform.platform())
    print("numpy:", np.__version__, "| pandas:", pd.__version__)
    import sklearn
    print("scikit-learn:", sklearn.__version__)
    try:
        import xgboost
        print("xgboost:", xgboost.__version__)
    except ImportError:
        print("xgboost: NOT INSTALLED")
    try:
        import torch
        print("torch:", torch.__version__, "| CUDA available:", torch.cuda.is_available())
    except ImportError:
        print("torch: NOT INSTALLED")
    print("Seeds: split =", SEED_SPLIT, "| early-stop split =", ES_SEED,
          "| MLP init =", MLP_INIT_SEED, "| MLP data order =", MLP_DATA_ORDER_SEED)
    print("Test fold =", TEST_FOLD, "| helper file hash:", file_sha256(CODE_DIR + "/bdhs_helpers.py")[:12])


def file_sha256(path):
    if not os.path.exists(path):
        return "FILE_NOT_FOUND"
    sha = hashlib.sha256()
    f = open(path, "rb")
    while True:
        block = f.read(1024 * 1024)
        if len(block) == 0:
            break
        sha.update(block)
    f.close()
    return sha.hexdigest()


def array_md5(arr):
    return hashlib.md5(np.ascontiguousarray(arr).tobytes()).hexdigest()


def ids_hash(ids):
    # Fingerprint of a SET of record ids (order does not matter).
    sorted_ids = np.sort(np.asarray(ids).astype(np.int64))
    return array_md5(sorted_ids)[:16]


def save_table(df, path):
    df.to_csv(path, index=False)
    print("saved:", path, "| rows:", len(df))


def add_check(check_log, name, passed, detail):
    # check_log is a plain list of [name, "PASS"/"FAIL", detail]
    if passed:
        check_log.append([name, "PASS", detail])
        print("PASS -", name, "|", detail)
    else:
        check_log.append([name, "FAIL", detail])
        print("FAIL -", name, "|", detail)
        raise AssertionError("Leakage check failed: " + name + " | " + detail)


def require_signoff(filename, message):
    path = OUTPUT_DIR + "/" + filename
    if not os.path.exists(path):
        raise RuntimeError("GATE NOT PASSED: " + message + " (missing " + path + ")")
    print("Gate OK:", filename)


# ----------------------------------------------------------------------
# 3. PREDICTOR CLEANING (no fitting here, so it can be applied before the split)
# ----------------------------------------------------------------------
def code_to_text(series):
    # Turns survey codes into text categories. Missing becomes the text "missing".
    result = []
    for value in series:
        if pd.isna(value):
            result.append("missing")
        else:
            try:
                number = float(value)
                if number == int(number):
                    result.append(str(int(number)))
                else:
                    result.append(str(number))
            except (ValueError, TypeError):
                result.append(str(value))
    return pd.Series(result, index=series.index)


def make_b11_text(b11_series, bord_series):
    # DECISION D14 (needs your sign-off): b11 is birth interval in MONTHS.
    # Fixed, pre-declared bins (NOT learned from data): <24, 24-35, 36-47, 48+.
    # Missing with bord == 1  -> "first_birth_NA"  (structurally not applicable)
    # Missing with bord  > 1  -> "missing"         (kept separate, never called first birth)
    result = []
    n = len(b11_series)
    for i in range(n):
        b11 = b11_series.iloc[i]
        bord = bord_series.iloc[i]
        if pd.isna(b11):
            if (not pd.isna(bord)) and bord == 1:
                result.append("first_birth_NA")
            else:
                result.append("missing")
        else:
            months = float(b11)
            if months < 24:
                result.append("lt24")
            elif months < 36:
                result.append("24to35")
            elif months < 48:
                result.append("36to47")
            else:
                result.append("48plus")
    return pd.Series(result, index=b11_series.index)


def clean_predictors(raw_df, predictors):
    # Makes one tidy table. Numeric predictors are floats, categorical predictors are text.
    # Nothing is learned from data in this function, so it is safe before the split.
    out = pd.DataFrame(index=raw_df.index)
    for var in predictors:
        if var == "v445":
            # DHS stores BMI x 100. Codes 9990+ (e.g. 9998) are flags -> missing.
            bmi = raw_df["v445"].astype(float)
            bmi = bmi.where(bmi < 9990)
            out["v445"] = bmi / 100.0
        elif var == "b11":
            known = raw_df["b11"].dropna()
            if len(known) > 0 and known.max() <= 10:
                raise ValueError("b11 looks categorical (max <= 10), not months. Update make_b11_text first.")
            out["b11"] = make_b11_text(raw_df["b11"], raw_df["bord"])
        elif var in NUMERIC_VARS:
            out[var] = raw_df[var].astype(float)
        else:
            out[var] = code_to_text(raw_df[var])
    return out


# ----------------------------------------------------------------------
# 4. PREPROCESSING: FIT ON TRAINING ROWS ONLY, THEN APPLY
# ----------------------------------------------------------------------
def fit_preprocessing(train_clean, train_ids, predictors):
    # Returns a table (spec). It stores everything learned from the training rows:
    #   numeric: median (for imputation), mean and std (for scaling, after imputation)
    #   categorical: levels kept (count >= MIN_CAT_COUNT) and a "__rare__" level if needed
    rows = []
    fit_hash = ids_hash(train_ids)
    n_fit = len(train_ids)
    for var in predictors:
        if var in NUMERIC_VARS:
            values = train_clean[var].astype(float)
            median = float(values.median())
            filled = values.fillna(median)
            mean = float(filled.mean())
            std = float(filled.std(ddof=0))
            if std == 0:
                std = 1.0
            rows.append([var, "num", "", median, mean, std, n_fit, fit_hash])
        else:
            counts = train_clean[var].value_counts()
            levels = sorted(list(counts.index))
            any_rare = False
            for level in levels:
                if counts[level] >= MIN_CAT_COUNT:
                    rows.append([var, "cat", str(level), np.nan, np.nan, np.nan, n_fit, fit_hash])
                else:
                    any_rare = True
            if any_rare:
                rows.append([var, "cat", "__rare__", np.nan, np.nan, np.nan, n_fit, fit_hash])
    columns = ["var", "kind", "level", "median", "mean", "std", "n_fit_rows", "fit_ids_hash"]
    return pd.DataFrame(rows, columns=columns)


def load_spec(path):
    spec = pd.read_csv(path)
    spec["level"] = spec["level"].astype(str)
    return spec


def apply_preprocessing(clean_df, spec, predictors):
    # Returns X (imputed, unscaled: for RF/XGBoost) and Xs (numeric columns scaled: for LR/MLP).
    # Both have exactly the same rows and columns.
    X = pd.DataFrame(index=clean_df.index)
    Xs = pd.DataFrame(index=clean_df.index)
    for var in predictors:
        rows = spec[spec["var"] == var]
        kind = rows["kind"].iloc[0]
        if kind == "num":
            median = float(rows["median"].iloc[0])
            mean = float(rows["mean"].iloc[0])
            std = float(rows["std"].iloc[0])
            values = clean_df[var].astype(float).fillna(median)
            X[var] = values
            Xs[var] = (values - mean) / std
        else:
            levels = list(rows["level"])
            real_levels = []
            has_rare = False
            for level in levels:
                if level == "__rare__":
                    has_rare = True
                else:
                    real_levels.append(level)
            texts = clean_df[var].astype(str)
            for level in real_levels:
                column_name = var + "=" + level
                dummy = (texts == level).astype(float)
                X[column_name] = dummy
                Xs[column_name] = dummy
            if has_rare:
                known = texts.isin(real_levels)
                dummy = (~known).astype(float)
                X[var + "=__rare__"] = dummy
                Xs[var + "=__rare__"] = dummy
    return X, Xs


def make_feature_map(feature_names):
    rows = []
    for name in feature_names:
        source = name.split("=")[0]
        rows.append([name, source])
    return pd.DataFrame(rows, columns=["encoded_column", "source_variable"])


# ----------------------------------------------------------------------
# 5. SPLITS
# ----------------------------------------------------------------------
def make_group_folds(y, groups, n_splits, seed):
    # StratifiedGroupKFold: whole PSUs go to one fold, outcome balance kept as close as possible.
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    fold_id = np.full(len(y), -1, dtype=int)
    k = 0
    for train_index, test_index in splitter.split(np.zeros(len(y)), y, groups):
        fold_id[test_index] = k
        k = k + 1
    return fold_id


def make_es_mask(y_train, groups_train, seed):
    # Inner PSU-disjoint split of the TRAINING rows. About 20% of PSUs become the
    # early-stopping set for the MLP. This keeps the scoring fold clean.
    fold_id = make_group_folds(y_train, groups_train, 5, seed)
    return fold_id == 0


# ----------------------------------------------------------------------
# 6. METRICS
# ----------------------------------------------------------------------
def score_probs(y_true, p):
    ap = average_precision_score(y_true, p)
    auc = roc_auc_score(y_true, p)
    ll = log_loss(y_true, p, labels=[0, 1])
    brier = brier_score_loss(y_true, p)
    return ap, auc, ll, brier


def threshold_metrics(y_true, p, threshold):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for i in range(len(y_true)):
        predicted = 1 if p[i] >= threshold else 0
        if predicted == 1 and y_true[i] == 1:
            tp = tp + 1
        elif predicted == 1 and y_true[i] == 0:
            fp = fp + 1
        elif predicted == 0 and y_true[i] == 1:
            fn = fn + 1
        else:
            tn = tn + 1
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    balanced_accuracy = (recall + specificity) / 2.0
    return precision, recall, f1, balanced_accuracy


def best_f1_threshold(y_true, p):
    # Threshold rule (DECISION D15): the threshold that maximises F1 on the pooled
    # development out-of-fold predictions. Test data is never used for this.
    best_threshold = 0.5
    best_f1 = -1.0
    threshold = 0.05
    while threshold <= 0.95:
        precision, recall, f1, bal = threshold_metrics(y_true, p, threshold)
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
        threshold = round(threshold + 0.01, 2)
    return best_threshold, best_f1


# ----------------------------------------------------------------------
# 7. MLP (PyTorch) - every variant sees the SAME records in the SAME order each epoch
# ----------------------------------------------------------------------
def get_epoch_order(n_rows, epoch, order_seed):
    # The record order for one epoch depends ONLY on (n_rows, epoch, order_seed).
    # It does not depend on the model size, learning rate or weight decay, so every
    # MLP variant trained on the same rows gets exactly the same order in every epoch.
    rng = np.random.RandomState(order_seed * 1000 + epoch)
    return rng.permutation(n_rows)


def build_mlp(n_inputs, hidden_sizes, init_seed):
    import torch
    torch.manual_seed(init_seed)
    layers = []
    previous = n_inputs
    for size in hidden_sizes:
        layers.append(torch.nn.Linear(previous, size))
        layers.append(torch.nn.ReLU())
        previous = size
    layers.append(torch.nn.Linear(previous, 1))
    return torch.nn.Sequential(*layers)


def count_parameters(model):
    total = 0
    for p in model.parameters():
        total = total + p.numel()
    return total


def train_mlp(X_fit, y_fit, X_es, y_es, hidden_sizes, learning_rate, weight_decay, order_seed):
    # Trains with Adam, mini-batches, early stopping on the early-stopping set (log loss).
    # Returns: model, best_epoch, epochs_run, order_hash_10, n_parameters
    import torch
    model = build_mlp(X_fit.shape[1], hidden_sizes, MLP_INIT_SEED)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    loss_function = torch.nn.BCEWithLogitsLoss()

    Xf = torch.tensor(X_fit, dtype=torch.float32)
    yf = torch.tensor(y_fit, dtype=torch.float32)
    Xe = torch.tensor(X_es, dtype=torch.float32)
    ye = torch.tensor(y_es, dtype=torch.float32)
    n_fit = len(y_fit)

    best_loss = 1.0e9
    best_epoch = -1
    best_state = None
    wait = 0
    epochs_run = 0
    order_hashes = []

    for epoch in range(MLP_MAX_EPOCHS):
        order = get_epoch_order(n_fit, epoch, order_seed)
        order_hashes.append(array_md5(order)[:8])
        model.train()
        start = 0
        rows_seen = 0
        while start < n_fit:
            batch_index = torch.from_numpy(order[start:start + MLP_BATCH]).long()
            optimizer.zero_grad()
            logits = model(Xf[batch_index]).reshape(-1)
            loss = loss_function(logits, yf[batch_index])
            loss.backward()
            optimizer.step()
            rows_seen = rows_seen + len(batch_index)
            start = start + MLP_BATCH
        if rows_seen != n_fit:
            raise AssertionError("An epoch did not use every training record exactly once.")
        epochs_run = epoch + 1

        model.eval()
        with torch.no_grad():
            es_logits = model(Xe).reshape(-1)
            es_loss = float(loss_function(es_logits, ye))
        if es_loss < best_loss - 1.0e-6:
            best_loss = es_loss
            best_epoch = epoch + 1
            best_state = copy.deepcopy(model.state_dict())
            wait = 0
        else:
            wait = wait + 1
            if wait >= MLP_PATIENCE:
                break

    model.load_state_dict(best_state)
    model.eval()
    first_ten = "".join(order_hashes[0:10])
    order_hash_10 = hashlib.md5(first_ten.encode()).hexdigest()[:12]
    return model, best_epoch, epochs_run, order_hash_10, count_parameters(model)


def predict_mlp(model, X):
    import torch
    model.eval()
    with torch.no_grad():
        logits = model(torch.tensor(X, dtype=torch.float32)).reshape(-1)
        probs = torch.sigmoid(logits).numpy()
    return probs.astype(float)


# ----------------------------------------------------------------------
# 8. MODEL SELECTION RULE (plan 6.1)
# ----------------------------------------------------------------------
def select_best_config(summary, model_name, tolerance, ll_tie):
    # summary: table with columns model, config, mean_ap, mean_logloss, complexity
    # Rule: best mean AP; configs within `tolerance` of it are tied;
    # among tied, lowest mean log loss; if still tied (within ll_tie), lowest complexity.
    # Returns the row index (label) of the winner and a text explaining the decision.
    part = summary[summary["model"] == model_name]
    best_ap = part["mean_ap"].max()
    tied = part[part["mean_ap"] >= best_ap - tolerance]
    best_ll = tied["mean_logloss"].min()
    tied2 = tied[tied["mean_logloss"] <= best_ll + ll_tie]
    lowest_complexity = tied2["complexity"].min()
    final = tied2[tied2["complexity"] == lowest_complexity]
    winner = final.index[0]
    reason = ("best mean AP = " + str(round(best_ap, 4)) + "; " + str(len(tied)) +
              " config(s) within AP tolerance " + str(tolerance) + "; " +
              str(len(tied2)) + " after log-loss tie-break; simplest chosen")
    return winner, reason


# ----------------------------------------------------------------------
# 9. DESCRIPTIVE HELPERS (N02)
# ----------------------------------------------------------------------
def cramers_v(a, b):
    from scipy.stats import chi2_contingency
    table = pd.crosstab(a, b)
    if table.shape[0] < 2 or table.shape[1] < 2:
        return 0.0
    chi2 = chi2_contingency(table, correction=False)[0]
    n = table.values.sum()
    k = min(table.shape[0], table.shape[1]) - 1
    return math.sqrt(chi2 / (n * k))
