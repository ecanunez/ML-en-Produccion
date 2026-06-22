import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance


# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/processed/training_dataset.parquet"
TARGET = "target"

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("PERMUTATION IMPORTANCE")
print("=" * 60)

df = pd.read_parquet(DATA_PATH)

X = df.drop(columns=[TARGET])
y = df[TARGET]

print(f"Dataset shape: {df.shape}")
print(f"Features: {X.shape[1]}")


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y
)


# ============================================================
# MODEL (mismo baseline que venías usando)
# ============================================================

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_leaf=5,
    min_samples_split=2,
    class_weight="balanced",
    random_state=RANDOM_STATE,
    n_jobs=-1
)

print("Entrenando modelo...")
model.fit(X_train, y_train)


# ============================================================
# PERMUTATION IMPORTANCE
# ============================================================

print("Calculando permutation importance...")

result = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=10,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    scoring="f1_macro"
)


# ============================================================
# DATAFRAME RESULTADOS
# ============================================================

importance_df = pd.DataFrame({
    "feature": X_test.columns,
    "importance_mean": result.importances_mean,
    "importance_std": result.importances_std
})


importance_df = importance_df.sort_values(
    by="importance_mean",
    ascending=False
)


# ============================================================
# OUTPUT
# ============================================================

print("\nTOP 20 FEATURES")
print(importance_df.head(20))

print("\nBOTTOM 20 FEATURES")
print(importance_df.tail(20))


# ============================================================
# SAVE
# ============================================================

output_path = "src/reports/permutation_importance.csv"

importance_df.to_csv(output_path, index=False)

print(f"\nArchivo guardado en: {output_path}")
print("Proceso finalizado.")