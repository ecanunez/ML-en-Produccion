from pathlib import Path
import pandas as pd

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[2]

IMPORTANCE_FILE = (
    ROOT / "src" / "reports" / "feature_importance_rf_v2.csv"
)

OUTPUT_FILE = (
    ROOT / "src" / "reports" / "feature_importance_ranking.csv"
)

# =========================================================
# MAIN
# =========================================================

def main():

    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE RANKING GENERATOR (STEP 1)")
    print("=" * 60)

    # --------------------------------------------------------
    # LOAD IMPORTANCE
    # --------------------------------------------------------

    importance = pd.read_csv(IMPORTANCE_FILE)

    importance = (
        importance
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # SAVE RANKING ONLY
    # --------------------------------------------------------

    importance.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nRanking guardado en:")
    print(OUTPUT_FILE)

    print("\nTop 10 features:")
    print(importance.head(10))


if __name__ == "__main__":
    main()