

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def generate_report(df, output_prefix="report"):
    sns.set_style("whitegrid")
    num_cols = df.select_dtypes(include='number').columns

    # --- Summary statistics ---
    summary = df.describe(include='all')
    summary.to_csv(f"{output_prefix}_summary_{datetime.now():%Y%m%d}.csv")

    # --- Distribution charts ---
    if len(num_cols) > 0:
        fig, axes = plt.subplots(1, len(num_cols), figsize=(5 * len(num_cols), 4))
        if len(num_cols) == 1:
            axes = [axes]
        for ax, col in zip(axes, num_cols):
            sns.histplot(df[col], kde=True, ax=ax)
            ax.set_title(f"Distribution: {col}")
        plt.tight_layout()
        plt.savefig(f"{output_prefix}_distributions.png")
        plt.close()

    # --- Correlation heatmap ---
    if len(num_cols) > 1:
        plt.figure(figsize=(8, 6))
        sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig(f"{output_prefix}_correlation.png")
        plt.close()

    # --- Multi-sheet Excel report ---
    with pd.ExcelWriter(f"{output_prefix}.xlsx", engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)
        summary.to_excel(writer, sheet_name="Summary Stats")

    print(f"Report generated: {output_prefix}.xlsx, distributions.png, correlation.png")


if __name__ == "__main__":
    df = pd.read_csv("cleaned_data.csv")
    generate_report(df)