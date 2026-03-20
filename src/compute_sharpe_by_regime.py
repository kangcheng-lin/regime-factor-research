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

    summary = pd.DataFrame(index=sorted(df["regime"].unique()))

    for factor in factors:
        summary[f"{factor}_mean"] = df.groupby("regime")[factor].mean()
        summary[f"{factor}_std"] = df.groupby("regime")[factor].std()
        summary[f"{factor}_sharpe"] = df.groupby("regime")[factor].apply(sharpe_ratio)
        summary[f"{factor}_count"] = df.groupby("regime")[factor].count()

    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "sharpe_by_regime.csv"
    summary.to_csv(output_path)

    print("Sharpe ratio by regime:")
    print(summary)


if __name__ == "__main__":
    main()