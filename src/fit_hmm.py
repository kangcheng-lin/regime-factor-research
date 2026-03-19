from pathlib import Path
import pandas as pd
import numpy as np
from hmmlearn.hmm import GaussianHMM


def main() -> None:
    data_path = Path("data/spy_features.csv")

    if not data_path.exists():
        raise FileNotFoundError("Feature file not found. Run build_features.py first.")

    df = pd.read_csv(data_path)

    # --- Prepare data ---
    X = df[["return", "volatility"]].values

    # --- Fit HMM ---
    model = GaussianHMM(
        n_components=3,
        covariance_type="full",
        n_iter=5000,
        random_state=42
    )

    model.fit(X)

    # --- Predict regimes ---
    hidden_states = model.predict(X)

    df["regime"] = hidden_states

    # --- Save results ---
    output_path = Path("data/spy_regimes.csv")
    df.to_csv(output_path, index=False)

    print("Model fitted successfully.")
    print("Regime counts:")
    print(df["regime"].value_counts())

    print("\nMeans by regime:")
    print(df.groupby("regime")[["return", "volatility"]].mean())


if __name__ == "__main__":
    main()