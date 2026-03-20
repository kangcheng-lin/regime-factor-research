from pathlib import Path
import pandas as pd


def main() -> None:
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    ff3_path = raw_dir / "ff3_daily.csv"
    mom_path = raw_dir / "mom_daily.csv"

    # --- Load FF3 ---
    ff3 = pd.read_csv(ff3_path)
    ff3.columns = ["date", "mkt_rf", "smb", "hml", "rf"]

    # --- Load MOM ---
    mom = pd.read_csv(mom_path)
    mom.columns = ["date", "mom"]

    # --- Convert date ---
    ff3["date"] = pd.to_datetime(ff3["date"], format="%Y%m%d")
    mom["date"] = pd.to_datetime(mom["date"], format="%Y%m%d")

    # --- Convert to numeric ---
    for col in ["mkt_rf", "smb", "hml", "rf"]:
        ff3[col] = pd.to_numeric(ff3[col], errors="coerce")

    mom["mom"] = pd.to_numeric(mom["mom"], errors="coerce")

    # --- Handle missing values coded in the French files ---
    for col in ["mkt_rf", "smb", "hml", "rf"]:
        ff3[col] = ff3[col].replace([-99.99, -999], pd.NA)

    mom["mom"] = mom["mom"].replace([-99.99, -999], pd.NA)

    # --- Convert percent to decimal ---
    for col in ["mkt_rf", "smb", "hml", "rf"]:
        ff3[col] = ff3[col] / 100.0

    mom["mom"] = mom["mom"] / 100.0

    # --- Drop missing rows ---
    ff3 = ff3.dropna().reset_index(drop=True)
    mom = mom.dropna().reset_index(drop=True)

    # --- Merge ---
    factors = (
        ff3.merge(mom, on="date", how="inner")
        .sort_values("date")
        .reset_index(drop=True)
    )

    # --- Save ---
    output_path = processed_dir / "ff_factors_daily.csv"
    factors.to_csv(output_path, index=False)

    print(f"Saved factors to {output_path}")
    print(factors.head())
    print(factors.tail())


if __name__ == "__main__":
    main()