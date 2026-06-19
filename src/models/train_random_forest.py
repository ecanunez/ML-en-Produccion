from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from load_dataset import load_dataset
from evaluate_model import evaluate_model


X, y, features = load_dataset()

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
)

rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=12,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf.fit(
    X_train,
    y_train
)

evaluate_model(
    rf,
    X_test,
    y_test,
    "RANDOM FOREST"
)