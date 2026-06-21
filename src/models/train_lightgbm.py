from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from lightgbm import LGBMClassifier

from load_dataset import load_dataset
from evaluate_model import evaluate_boosting_model
from log_experiment import log_experiment


print("\nVariables nuevas:")

X, y, features, dataset_modified = load_dataset()

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

print("Entrenando...")

lgbm = LGBMClassifier(
    objective="multiclass",
    num_class=3,
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    random_state=42,
    verbose=-1,
    force_col_wise=True
)

lgbm.fit(
    X_train,
    y_train
)

metrics = evaluate_boosting_model(
    model=lgbm,
    X_test=X_test,
    y_true=y_test,
    label_encoder=encoder,
    model_name="LIGHTGBM"
)

log_experiment(
    dataset="training_dataset.parquet",
    dataset_modified=dataset_modified,
    model="LightGBM",
    f1_macro=metrics["f1_macro"],
    accuracy=metrics["accuracy"],
    precision_macro=metrics["precision_macro"],
    recall_macro=metrics["recall_macro"],
    features=X.shape[1],
    train_rows=len(X_train),
    params=(
        "n_estimators=500,"
        "learning_rate=0.05,"
        "max_depth=6"
    ),
    notes="Feature Engineering v1"
)