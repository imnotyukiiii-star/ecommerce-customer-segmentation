"""
E-commerce Customer Segmentation and Marketing Strategy Analysis

This script downloads the UCI Online Retail dataset, cleans the data,
creates exploratory charts, builds RFM customer segments with K-Means,
and saves portfolio-ready outputs.
"""

import os
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

os.environ.setdefault("MPLCONFIGDIR", str(Path(".mplconfig").resolve()))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
REPORTS_DIR = PROJECT_ROOT / "reports"

DATA_URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
ZIP_PATH = RAW_DIR / "online_retail.zip"
EXCEL_PATH = RAW_DIR / "Online Retail.xlsx"
CLEANED_PATH = PROCESSED_DIR / "online_retail_cleaned.csv"
RFM_PATH = PROCESSED_DIR / "rfm_segments.csv"
SEGMENT_SUMMARY_PATH = PROCESSED_DIR / "segment_summary.csv"


def prepare_folders():
    """Create all folders needed by the project."""
    for folder in [RAW_DIR, PROCESSED_DIR, FIGURES_DIR, REPORTS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)


def download_dataset():
    """Download and unzip the UCI Online Retail dataset if it is not present."""
    if EXCEL_PATH.exists():
        print("Dataset already exists in data/raw.")
        return

    print("Downloading UCI Online Retail dataset...")
    urlretrieve(DATA_URL, ZIP_PATH)

    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(RAW_DIR)

    print("Dataset downloaded and extracted.")


def load_raw_data():
    """Load the raw Excel file."""
    return pd.read_excel(EXCEL_PATH)


def clean_data(df):
    """Clean transactions and create the Revenue field."""
    cleaned = df.copy()

    cleaned = cleaned.dropna(subset=["CustomerID"])
    cleaned = cleaned[cleaned["Quantity"] > 0]
    cleaned = cleaned[cleaned["UnitPrice"] > 0]
    cleaned = cleaned[~cleaned["InvoiceNo"].astype(str).str.startswith("C")]

    cleaned["InvoiceDate"] = pd.to_datetime(cleaned["InvoiceDate"])
    cleaned["CustomerID"] = cleaned["CustomerID"].astype(int).astype(str)
    cleaned["Revenue"] = cleaned["Quantity"] * cleaned["UnitPrice"]

    cleaned.to_csv(CLEANED_PATH, index=False)
    return cleaned


def save_chart(path):
    """Save a chart with consistent spacing and close the figure."""
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def create_eda_charts(df):
    """Create the exploratory charts required for the portfolio project."""
    monthly_revenue = (
        df.set_index("InvoiceDate")
        .resample("M")["Revenue"]
        .sum()
        .reset_index()
    )
    monthly_customers = (
        df.set_index("InvoiceDate")
        .resample("M")["CustomerID"]
        .nunique()
        .reset_index(name="ActiveCustomers")
    )
    country_revenue = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)
    product_revenue = (
        df.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10)
    )
    order_values = df.groupby("InvoiceNo")["Revenue"].sum()

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_revenue["InvoiceDate"], monthly_revenue["Revenue"], marker="o", color="#1f77b4")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    save_chart(FIGURES_DIR / "monthly_revenue_trend.png")

    plt.figure(figsize=(10, 5))
    country_revenue.sort_values().plot(kind="barh", color="#2ca02c")
    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Country")
    save_chart(FIGURES_DIR / "top_10_countries_by_revenue.png")

    plt.figure(figsize=(10, 6))
    product_revenue.sort_values().plot(kind="barh", color="#ff7f0e")
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Product")
    save_chart(FIGURES_DIR / "top_10_products_by_revenue.png")

    plt.figure(figsize=(9, 5))
    order_values[order_values <= order_values.quantile(0.99)].plot(
        kind="hist", bins=40, color="#9467bd", edgecolor="white"
    )
    plt.title("Distribution of Order Value")
    plt.xlabel("Order Value")
    plt.ylabel("Number of Orders")
    save_chart(FIGURES_DIR / "order_value_distribution.png")

    plt.figure(figsize=(10, 5))
    plt.plot(
        monthly_customers["InvoiceDate"],
        monthly_customers["ActiveCustomers"],
        marker="o",
        color="#d62728",
    )
    plt.title("Active Customers by Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Active Customers")
    plt.xticks(rotation=45)
    save_chart(FIGURES_DIR / "active_customers_by_month.png")

    return monthly_revenue, monthly_customers, order_values


def build_rfm_segments(df):
    """Create RFM features, test k values, and assign customer segments."""
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum"),
    )

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])

    inertias = []
    k_values = range(2, 9)
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(rfm_scaled)
        inertias.append(model.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(list(k_values), inertias, marker="o", color="#1f77b4")
    plt.title("K-Means Elbow Plot")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.xticks(list(k_values))
    save_chart(FIGURES_DIR / "kmeans_elbow_plot.png")

    best_k = 4
    final_model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    rfm["Cluster"] = final_model.fit_predict(rfm_scaled)

    segment_names = create_segment_names(rfm)
    rfm["Segment"] = rfm["Cluster"].map(segment_names)

    total_revenue = rfm["Monetary"].sum()
    summary = (
        rfm.groupby("Segment")
        .agg(
            Customers=("Monetary", "size"),
            AvgRecency=("Recency", "mean"),
            AvgFrequency=("Frequency", "mean"),
            AvgMonetary=("Monetary", "mean"),
            TotalRevenue=("Monetary", "sum"),
        )
        .reset_index()
    )
    summary["RevenuePct"] = summary["TotalRevenue"] / total_revenue
    summary = summary.sort_values("TotalRevenue", ascending=False)

    rfm.reset_index().to_csv(RFM_PATH, index=False)
    summary.to_csv(SEGMENT_SUMMARY_PATH, index=False)

    return rfm, summary


def create_segment_names(rfm):
    """Label clusters using simple business rules based on RFM averages."""
    cluster_stats = rfm.groupby("Cluster").agg(
        Recency=("Recency", "mean"),
        Frequency=("Frequency", "mean"),
        Monetary=("Monetary", "mean"),
    )

    labels = {}
    scoring = cluster_stats.copy()
    scoring["ValueScore"] = (
        scoring["Frequency"].rank(ascending=True)
        + scoring["Monetary"].rank(ascending=True)
        + scoring["Recency"].rank(ascending=False)
    )

    high_value_cluster = scoring["ValueScore"].idxmax()
    labels[high_value_cluster] = "High-Value Loyal Customers"

    remaining = [cluster for cluster in scoring.index if cluster not in labels]
    at_risk_cluster = scoring.loc[remaining, "Recency"].idxmax()
    labels[at_risk_cluster] = "At-Risk Customers"

    remaining = [cluster for cluster in scoring.index if cluster not in labels]
    low_value_cluster = scoring.loc[remaining, "Monetary"].idxmin()
    labels[low_value_cluster] = "Low-Value or One-Time Buyers"

    for cluster in cluster_stats.index:
        if cluster not in labels:
            labels[cluster] = "Potential Loyal Customers"

    return labels


def write_business_report(df, segment_summary):
    """Write a short Markdown business report with findings and recommendations."""
    total_revenue = df["Revenue"].sum()
    total_customers = df["CustomerID"].nunique()
    total_orders = df["InvoiceNo"].nunique()
    date_min = df["InvoiceDate"].min().date()
    date_max = df["InvoiceDate"].max().date()
    country_revenue = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False)
    product_revenue = df.groupby("Description")["Revenue"].sum().sort_values(ascending=False)
    top_country = country_revenue.index[0]
    top_country_pct = country_revenue.iloc[0] / total_revenue
    top_product = product_revenue.index[0]
    top_10_product_pct = product_revenue.head(10).sum() / total_revenue
    order_values = df.groupby("InvoiceNo")["Revenue"].sum()

    monthly = df.copy()
    monthly["Month"] = monthly["InvoiceDate"].dt.to_period("M").astype(str)
    monthly_revenue = monthly.groupby("Month")["Revenue"].sum()
    monthly_customers = monthly.groupby("Month")["CustomerID"].nunique()
    peak_revenue_month = monthly_revenue.idxmax()
    peak_customer_month = monthly_customers.idxmax()

    segment_rows = []
    for _, row in segment_summary.iterrows():
        segment_rows.append(
            f"| {row['Segment']} | {int(row['Customers']):,} | "
            f"{row['AvgRecency']:.1f} | {row['AvgFrequency']:.1f} | "
            f"${row['AvgMonetary']:,.2f} | ${row['TotalRevenue']:,.2f} | "
            f"{row['RevenuePct']:.1%} |"
        )

    report = f"""# Business Report: E-commerce Customer Segmentation

## Executive Summary

- The cleaned dataset covers {date_min} to {date_max} and contains {total_orders:,} orders from {total_customers:,} customers.
- Total revenue after cleaning is ${total_revenue:,.2f}.
- Revenue is highly concentrated in {top_country}, which contributes {top_country_pct:.1%} of cleaned revenue.
- Revenue and active customers both peak in {peak_revenue_month}, showing a strong late-year sales period.
- RFM segmentation separates customers into four groups with different retention and marketing priorities.

## Key EDA Findings

- Average order value is ${order_values.mean():,.2f}, while the median order value is ${order_values.median():,.2f}. This means larger orders pull the average upward.
- The top revenue market is {top_country}; the top 10 countries together contribute {country_revenue.head(10).sum() / total_revenue:.1%} of revenue.
- The top product by revenue is "{top_product}".
- The top 10 products contribute {top_10_product_pct:.1%} of revenue, so revenue is less concentrated by product than by country.
- Active customers peak in {peak_customer_month}, with {monthly_customers.max():,} active customers.

## Segment Summary

| Segment | Customers | Avg Recency | Avg Frequency | Avg Monetary | Total Revenue | Revenue % |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(segment_rows)}

## Recommendations

### High-Value Loyal Customers
These customers have the strongest combined recency, frequency, and monetary behavior. They are a small group but contribute a large amount per customer. The business should protect this group with loyalty rewards, early access to new products, and personalized offers.

### Potential Loyal Customers
These customers purchase recently and frequently, but they are not the highest-value group. Marketing should encourage repeat purchases through product recommendations, bundles, and targeted email campaigns.

### At-Risk Customers
These customers have not purchased recently. The business should use win-back campaigns, limited-time discounts, and reminders based on previous purchase categories.

### Low-Value or One-Time Buyers
This is the largest customer group. Even though total revenue is meaningful because the group is large, average frequency and spending are lower than stronger segments. The business should use low-cost lifecycle marketing, welcome campaigns, and cross-sell messages, while avoiding expensive retention offers.

## Limitations

The dataset covers one online retailer and does not include marketing cost, profit margin, website traffic, or customer demographics. As a result, recommendations focus on transaction behavior rather than full customer lifetime value.
"""
    (REPORTS_DIR / "business_report.md").write_text(report, encoding="utf-8")


def write_executive_summary(df, segment_summary):
    """Write a slide-style executive summary with real project results."""
    total_revenue = df["Revenue"].sum()
    total_customers = df["CustomerID"].nunique()
    total_orders = df["InvoiceNo"].nunique()
    country_revenue = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False)
    top_country = country_revenue.index[0]
    top_country_pct = country_revenue.iloc[0] / total_revenue
    monthly = df.copy()
    monthly["Month"] = monthly["InvoiceDate"].dt.to_period("M").astype(str)
    peak_month = monthly.groupby("Month")["Revenue"].sum().idxmax()
    high_value = segment_summary[segment_summary["Segment"] == "High-Value Loyal Customers"].iloc[0]
    at_risk = segment_summary[segment_summary["Segment"] == "At-Risk Customers"].iloc[0]

    summary = f"""# Slide-Style Executive Summary

- Cleaned {len(df):,} transaction rows, representing {total_orders:,} orders, {total_customers:,} customers, and ${total_revenue:,.2f} in revenue.
- Revenue is concentrated in {top_country}, which contributes {top_country_pct:.1%} of cleaned revenue.
- Monthly revenue peaks in {peak_month}, indicating a strong late-year sales period.
- High-value loyal customers are a small segment of {int(high_value['Customers']):,} customers but contribute {high_value['RevenuePct']:.1%} of revenue.
- At-risk customers represent {int(at_risk['Customers']):,} customers and should be targeted with win-back campaigns before using larger discounts.
"""
    (REPORTS_DIR / "executive_summary.md").write_text(summary, encoding="utf-8")


def main():
    prepare_folders()
    download_dataset()
    raw_data = load_raw_data()
    cleaned_data = clean_data(raw_data)
    create_eda_charts(cleaned_data)
    _, segment_summary = build_rfm_segments(cleaned_data)
    write_business_report(cleaned_data, segment_summary)
    write_executive_summary(cleaned_data, segment_summary)

    print("Analysis complete.")
    print(f"Cleaned data saved to: {CLEANED_PATH}")
    print(f"Figures saved to: {FIGURES_DIR}")
    print(f"Business report saved to: {REPORTS_DIR / 'business_report.md'}")


if __name__ == "__main__":
    main()
