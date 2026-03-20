from pathlib import Path
import pandas as pd


def main() -> None:
    data_path = Path("data/processed/merged_regime_factors.csv")

    if not data_path.exists():
        raise FileNotFoundError("Run merge_regime_factors.py first.")

    df = pd.read_csv(data_path)

    factor_cols = ["mkt_rf", "smb", "hml", "mom"]

    summary = (
        df.groupby("regime")[factor_cols]
        .agg(["mean", "std", "count"])
    )

    # --- Save ---
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "factor_summary_by_regime.csv"
    summary.to_csv(output_path)

    print("Factor summary by regime:")
    print(summary)


if __name__ == "__main__":
    main()