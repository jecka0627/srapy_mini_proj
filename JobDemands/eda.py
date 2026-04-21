# import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
sns.set(color_codes=True)


def load_data(file_path):
    return pd.read_csv(file_path)


def clean_data(jobs):
    # remove duplicates
    jobs = jobs.drop_duplicates()

    # remove null values
    jobs = jobs.dropna()

    return jobs


def remove_outliers(jobs):
    # select numeric columns
    jobs_numeric = jobs.select_dtypes(include=[np.number])

    # calculate Q1, Q3, and IQR
    q1 = jobs_numeric.quantile(0.25)
    q3 = jobs_numeric.quantile(0.75)
    iqr = q3 - q1

    # filter out outliers
    jobs_no_outliers = jobs_numeric[
        ~((jobs_numeric < (q1 - 1.5 * iqr)) |
          (jobs_numeric > (q3 + 1.5 * iqr))).any(axis=1)
    ]

    # merge back with non-numeric columns
    jobs_clean = pd.merge(
        jobs_no_outliers,
        jobs.select_dtypes(exclude=[np.number]),
        left_index=True,
        right_index=True
    )

    return jobs_clean


def visualize_data(jobs):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Percentage of job opening in employment type
    jobs["employment_type"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=axes[0, 0]
    )
    axes[0, 0].set_title("Employment Type")
    axes[0, 0].set_ylabel("")

    # Count of job opening for IT and NON-IT jobs
    jobs["job_category"].value_counts().head(10).plot(
        kind="bar",
        ax=axes[0, 1],
        rot=0
    )
    axes[0, 1].set_title("Job Categories")
    axes[0, 1].set_ylabel("job opening")

    # Top 10 locations with most job opening
    jobs["location"].value_counts().head(10).plot(
        kind="barh",
        ax=axes[1, 0]
    )
    axes[1, 0].set_title("Top Locations")
    axes[1, 0].set_xlabel("job opening")

    # Top 10 companies with most job opening
    jobs["company"].value_counts().head(10).plot(
        kind="barh",
        ax=axes[1, 1]
    )
    axes[1, 1].set_title("Top Companies")
    axes[1, 1].set_xlabel("job opening")

    plt.tight_layout(pad=3.0)
    plt.show()


def main():
    file_path = "jobs.csv"
    jobs = load_data(file_path)
    jobs = clean_data(jobs)
    jobs = remove_outliers(jobs)
    visualize_data(jobs)

if __name__ == "__main__":
    main()