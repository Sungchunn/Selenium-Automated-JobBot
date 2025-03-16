
import os
import pandas as pd
import matplotlib.pyplot as plt


def analyze_data():
    csv_path = os.path.join(os.getcwd(), "data", "job_listings.csv")
    if not os.path.isfile(csv_path):
        print("No job_listings.csv found. Please run scrape_jobs.py first.")
        return

    df = pd.read_csv(csv_path)
    source_counts = df["source"].value_counts()
    source_counts.plot(kind="bar", title="Jobs by Source")
    plt.xlabel("Source")
    plt.ylabel("Count")

    fig_path = os.path.join(os.getcwd(), "data", "job_source_chart.png")
    plt.savefig(fig_path)
    plt.close()

    print(f"Analysis complete. Chart saved to {fig_path}")


if __name__ == "__main__":
    analyze_data()