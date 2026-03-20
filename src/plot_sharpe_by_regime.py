from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    data_path = Path("data/results/sharpe_by_regime.csv")

    if not data_path.exists():
        raise FileNotFoundError("Run compute_sharpe_by_regime.py first.")

    df = pd.read_csv(data_path, index_col=0)

    regime_map = {
        0: "Regime 0 - Neutral",
        1: "Regime 1 - Bull",
        2: "Regime 2 - Bear"
    }

    # Keep only Sharpe columns
    sharpe_cols = [col for col in df.columns if col.endswith("_sharpe")]
    plot_df = df[sharpe_cols].copy()
    plot_df.columns = [col.replace("_sharpe", "") for col in plot_df.columns]

    # Rename index for readability
    plot_df.index = [regime_map.get(int(idx), f"Regime {idx}") for idx in plot_df.index]

    ax = plot_df.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Factor Sharpe Ratios by Regime")
    ax.set_xlabel("Regime")
    ax.set_ylabel("Sharpe Ratio")
    ax.tick_params(axis="x", rotation=0)
    ax.axhline(0, linewidth=1)

    plt.tight_layout()

    output_dir = Path("plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_dir / "sharpe_by_regime.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

    print("Saved Sharpe-by-regime plot to plots/sharpe_by_regime.png")


if __name__ == "__main__":
    main()