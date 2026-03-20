from pathlib import Path
import pandas as pd


def sharpe_ratio(series: pd.Series) -> float:
    std = series.std()
    if std == 0 or pd.isna(std):
        return float("nan")
    return series.mean() / std


def main() -> None:
    data_path = Path("data/processed/merged_regime_factors_qmj.csv")

    if not data_path.exists():
        raise FileNotFoundError("Run merge_regime_factors.py first.")

    df = pd.read_csv(data_path)

    factors = ["mkt_rf", "smb", "hml", "mom", "QMJ"]

    print(f"Rows before dropna: {len(df)}")
    df = df.dropna(subset=factors)
    print(f"Rows after dropna: {len(df)}")

    grouped = df.groupby("regime")
    summary = pd.DataFrame(index=sorted(df["regime"].unique()))

    for factor in factors:
        summary[f"{factor}_mean"] = grouped[factor].mean()
        summary[f"{factor}_std"] = grouped[factor].std()
        summary[f"{factor}_sharpe"] = grouped[factor].apply(sharpe_ratio)
        summary[f"{factor}_count"] = grouped[factor].count()

    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Full summary table: covers Table 5, 6, and 7 style outputs
    summary_path = output_dir / "factor_summary_by_regime.csv"
    summary.to_csv(summary_path, index=False)

    # Optional Sharpe-only table
    sharpe_cols = [col for col in summary.columns if col.endswith("_sharpe")]
    sharpe_df = summary[sharpe_cols].copy()
    sharpe_path = output_dir / "sharpe_by_regime.csv"
    sharpe_df.to_csv(sharpe_path, index=False)

    print("\nFactor summary by regime:")
    print(summary)

    print(f"\nSaved factor summary to: {summary_path}")
    print(f"Saved Sharpe-only table to: {sharpe_path}")


if __name__ == "__main__":
    main()