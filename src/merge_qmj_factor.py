from pathlib import Path
import pandas as pd


def main() -> None:
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    merged_path = processed_dir / "merged_regime_factors.csv"
    qmj_path = processed_dir / "qmj_daily.csv"
    output_path = processed_dir / "merged_regime_factors_qmj.csv"

    merged = pd.read_csv(merged_path)
    qmj = pd.read_csv(qmj_path)

    merged["date"] = pd.to_datetime(merged["date"], errors="coerce")
    qmj["date"] = pd.to_datetime(qmj["date"], errors="coerce")

    merged_qmj = merged.merge(qmj, on="date", how="left")

    merged_qmj.to_csv(output_path, index=False)

    print(merged_qmj[["date", "QMJ"]].head())
    print(merged_qmj[["date", "QMJ"]].tail())
    print(merged_qmj.info())
    print(f"Saved merged file to: {output_path}")

    print(f"Missing QMJ ratio: {merged_qmj['QMJ'].isna().mean():.4%}")
    print(merged_qmj.loc[merged_qmj['QMJ'].isna(), ['date']].tail(10))


if __name__ == "__main__":
    main()