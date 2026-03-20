from pathlib import Path
import pandas as pd


def main() -> None:
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    qmj_path = raw_dir / "aqr_qmj_daily.xlsx"
    output_path = processed_dir / "qmj_daily.csv"

    qmj = pd.read_excel(
        qmj_path,
        sheet_name="QMJ Factors",
        skiprows=18
    )

    qmj = qmj[["DATE", "USA"]].copy()
    qmj = qmj.rename(columns={"DATE": "date", "USA": "QMJ"})

    qmj["date"] = pd.to_datetime(
        qmj["date"],
        format="%m/%d/%Y",
        errors="coerce"
    )

    qmj["QMJ"] = pd.to_numeric(qmj["QMJ"], errors="coerce")

    qmj = (
        qmj.dropna(subset=["date", "QMJ"])
           .sort_values("date")
           .reset_index(drop=True)
    )

    qmj.to_csv(output_path, index=False)

    print(qmj.head())
    print(qmj.tail())
    print(f"Saved cleaned QMJ data to: {output_path}")


if __name__ == "__main__":
    main()