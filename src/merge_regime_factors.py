from pathlib import Path
import pandas as pd


def main() -> None:
    regimes_path = Path("data/spy_regimes.csv")
    factors_path = Path("data/processed/ff_factors_daily.csv")

    if not regimes_path.exists():
        raise FileNotFoundError("Run fit_hmm.py first.")

    if not factors_path.exists():
        raise FileNotFoundError("Run build_ff_factors.py first.")

    regimes = pd.read_csv(regimes_path)
    factors = pd.read_csv(factors_path)

    regimes["date"] = pd.to_datetime(regimes["date"])
    factors["date"] = pd.to_datetime(factors["date"])

    merged = (
        regimes.merge(factors, on="date", how="inner")
        .sort_values("date")
        .reset_index(drop=True)
    )

    output_path = Path("data/processed/merged_regime_factors.csv")
    merged.to_csv(output_path, index=False)

    print(f"Saved merged data to {output_path}")
    print(merged.head())
    print(merged.tail())
    print(f"\nNumber of rows: {len(merged)}")


if __name__ == "__main__":
    main()