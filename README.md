# E-commerce Customer Segmentation and Marketing Strategy Analysis

## Project Overview

This project analyzes customer purchasing behavior from the UCI Online Retail dataset. The goal is to clean transaction data, explore sales patterns, segment customers using RFM analysis and K-Means clustering, and translate the results into practical marketing recommendations.

The project is designed as a portfolio project for business analyst, marketing analyst, data analyst, operations, and consulting internship applications.

## Business Problem

An online retailer wants to understand which customers are most valuable, which customers may become loyal buyers, and which customers may need reactivation. By segmenting customers based on purchase recency, frequency, and monetary value, the business can create more targeted and cost-effective marketing strategies.

## Dataset Description

The dataset is the UCI Online Retail dataset, which contains transactional records for a UK-based online retailer from December 1, 2010 to December 9, 2011.

Columns used:

- `InvoiceNo`: Invoice number for each transaction
- `StockCode`: Product code
- `Description`: Product description
- `Quantity`: Number of units purchased
- `InvoiceDate`: Date and time of the invoice
- `UnitPrice`: Price per unit
- `CustomerID`: Customer identifier
- `Country`: Customer country

After cleaning, the dataset contains 397,884 transaction rows, 18,532 orders, 4,338 customers, and $8,911,407.90 in revenue.

Source: [UCI Machine Learning Repository - Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

## Tools Used

- Python
- pandas
- numpy
- matplotlib
- scikit-learn
- Jupyter Notebook

## Project Structure

```text
.
|-- README.md
|-- data
|   |-- raw
|   |   `-- Online Retail.xlsx
|   `-- processed
|       |-- online_retail_cleaned.csv
|       |-- rfm_segments.csv
|       `-- segment_summary.csv
|-- notebooks
|   `-- ecommerce_customer_segmentation.ipynb
|-- outputs
|   `-- figures
|       |-- active_customers_by_month.png
|       |-- kmeans_elbow_plot.png
|       |-- monthly_revenue_trend.png
|       |-- order_value_distribution.png
|       |-- top_10_countries_by_revenue.png
|       `-- top_10_products_by_revenue.png
|-- reports
|   |-- business_report.md
|   `-- executive_summary.md
|-- requirements.txt
`-- scripts
    `-- customer_segmentation_analysis.py
```

## Methodology

1. Load the UCI Online Retail dataset from `data/raw/Online Retail.xlsx`.
2. Clean the data by removing missing customer IDs, cancelled orders, non-positive quantities, and non-positive prices.
3. Create a `Revenue` column using `Quantity * UnitPrice`.
4. Conduct exploratory data analysis using revenue, customers, countries, products, and order values.
5. Build RFM features:
   - Recency: days since the customer's latest purchase
   - Frequency: number of unique invoices
   - Monetary: total customer spending
6. Standardize RFM features.
7. Test K-Means values from 2 to 8 and review the elbow plot.
8. Use 4 clusters and assign business-friendly segment names.
9. Develop marketing recommendations for each segment.

## Key Findings

- Total cleaned revenue is $8.91M across 18,532 orders and 4,338 customers.
- Revenue peaks in November 2011, which suggests a strong late-year sales period.
- The United Kingdom contributes 82.0% of cleaned revenue, making it the dominant market.
- The top 10 countries contribute 96.9% of revenue, showing strong geographic concentration.
- Average order value is $480.87, while median order value is $303.04, meaning larger orders pull the average upward.
- The top product by revenue is `PAPER CRAFT , LITTLE BIRDIE`.
- The top 10 products contribute 9.9% of revenue, so product revenue is less concentrated than country revenue.

## Customer Segments

| Segment | Customers | Avg Recency | Avg Frequency | Avg Monetary | Revenue Share |
|---|---:|---:|---:|---:|---:|
| Low-Value or One-Time Buyers | 3,052 | 43.9 | 3.7 | $1,350.14 | 46.2% |
| Potential Loyal Customers | 211 | 15.7 | 22.0 | $12,453.23 | 29.5% |
| High-Value Loyal Customers | 13 | 7.4 | 82.5 | $127,338.31 | 18.6% |
| At-Risk Customers | 1,062 | 248.6 | 1.6 | $478.11 | 5.7% |

## Business Recommendations

- **High-Value Loyal Customers**: Protect this small but very valuable group with loyalty rewards, early access, and personalized recommendations.
- **Potential Loyal Customers**: Encourage repeat purchases with bundles, product recommendations, and targeted campaigns.
- **At-Risk Customers**: Use win-back emails, limited-time discounts, and reminders based on past purchases.
- **Low-Value or One-Time Buyers**: Use low-cost lifecycle campaigns and cross-sell messages. This group is large, so small improvements in repeat purchase behavior could matter, but expensive discounts should be used carefully.

## What I Learned

This project helped me practice a complete analytics workflow:

- Turning raw transaction data into clean analysis-ready data
- Creating exploratory charts for business interpretation
- Building RFM customer features
- Applying K-Means clustering in a practical marketing context
- Interpreting segment quality using both customer count and revenue contribution
- Translating data outputs into clear business recommendations
- Organizing an analytics project for a professional portfolio

## How to Run the Project

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Make sure the dataset is saved at:

```text
data/raw/Online Retail.xlsx
```

3. Run the full analysis script:

```bash
python scripts/customer_segmentation_analysis.py
```

4. Review the outputs:

- Cleaned data: `data/processed/online_retail_cleaned.csv`
- Customer segments: `data/processed/rfm_segments.csv`
- Segment summary: `data/processed/segment_summary.csv`
- Charts: `outputs/figures`
- Business report: `reports/business_report.md`
- Executive summary: `reports/executive_summary.md`
- Notebook: `notebooks/ecommerce_customer_segmentation.ipynb`
