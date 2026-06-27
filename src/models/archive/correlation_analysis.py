from pathlib import Path

import pandas as pd

from load_dataset import load_dataset


ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    ROOT
    / "src"
    / "reports"
    / "high_correlations.csv"
)

CORRELATION_THRESHOLD = 0.85


def main():

    print("\n" + "=" * 60)
    print("CORRELATION ANALYSIS")
    print("=" * 60)

    X, y, features, _ = load_dataset()

    print(
        f"\nCalculando correlaciones para "
        f"{len(features)} features..."
    )

    corr_matrix = X.corr().abs()

    results = []

    for i in range(len(corr_matrix.columns)):

        for j in range(i + 1, len(corr_matrix.columns)):

            corr_value = corr_matrix.iloc[i, j]

            if corr_value >= CORRELATION_THRESHOLD:

                results.append({
                    "feature_a": corr_matrix.columns[i],
                    "feature_b": corr_matrix.columns[j],
                    "correlation": round(
                        corr_value,
                        4
                    )
                })

    results_df = pd.DataFrame(results)

    if len(results_df) == 0:

        print(
            "\nNo se encontraron pares "
            f"con correlación > {CORRELATION_THRESHOLD}"
        )

        return

    results_df = results_df.sort_values(
        "correlation",
        ascending=False
    )

    print("\n" + "=" * 60)
    print("TOP CORRELATIONS")
    print("=" * 60)

    print(
        results_df.head(50)
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nPares encontrados: "
        f"{len(results_df):,}"
    )

    print(
        f"\nArchivo guardado en:\n"
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()