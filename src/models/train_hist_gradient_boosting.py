from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier

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

hgb = HistGradientBoostingClassifier(
    learning_rate=0.05,
    max_depth=6,
    max_iter=300,
    min_samples_leaf=20,
    random_state=42
)

hgb.fit(
    X_train,
    y_train
)

evaluate_model(
    hgb,
    X_test,
    y_test,
    "HIST GRADIENT BOOSTING"
)