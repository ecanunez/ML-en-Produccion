from pathlib import Path
import pandas as pd

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[3]

IMPORTANCE_FILE = ROOT / "src/reports/feature_importance_rf_v2.csv"

OUTPUT_DIR = ROOT / "src/reports"

RANKING_FILE = OUTPUT_DIR / "feature_importance_ranking.csv"

TOPS = [10, 20, 30, 40, 50]


# =========================================================
# MAIN
# =========================================================

def main():

    print("\n" + "=" * 60)
    print("FEATURE SET BUILDER")
    print("=" * 60)

    importance = pd.read_csv(IMPORTANCE_FILE)

    importance = (
        importance
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    # -------------------------
    # SAVE RANKING
    # -------------------------

    importance.to_csv(RANKING_FILE, index=False)

    print(f"\nRanking guardado en: {RANKING_FILE}")

    # -------------------------
    # SAVE TOP N
    # -------------------------

    for n in TOPS:

        features = importance.head(n)["feature"].tolist()

        out = OUTPUT_DIR / f"top{n}_features.csv"

        pd.DataFrame({"feature": features}).to_csv(out, index=False)

        print(f"Top{n} guardado en: {out}")

    print("\nFeature sets generados correctamente.")


if __name__ == "__main__":
    main()