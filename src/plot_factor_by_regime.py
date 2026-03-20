from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    data_path = Path("data/processed/merged_regime_factors.csv")

    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])

    factors = ["mkt_rf", "smb", "hml", "mom"]

    regime_map = {
        0: "Regime 0 - Neutral",
        1: "Regime 1 - Bull",
        2: "Regime 2 - Bear"
    }

    for factor in factors:
        plt.figure(figsize=(10, 5))

        for regime in sorted(df["regime"].unique()):
            subset = df[df["regime"] == regime]
            plt.hist(
                subset[factor],
                bins=50,
                alpha=0.5,
                label=regime_map[regime]
            )

        plt.title(f"{factor} distribution by regime (HMM classified)")
        plt.legend()
        plt.tight_layout()

        output_dir = Path("plots")
        output_dir.mkdir(exist_ok=True)

        plt.savefig(output_dir / f"{factor}_by_regime.png")
        plt.show()

        plt.close()

    print("Saved factor distribution plots.")


if __name__ == "__main__":
    main()