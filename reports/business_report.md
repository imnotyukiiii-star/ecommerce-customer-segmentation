# Business Report: E-commerce Customer Segmentation

## Executive Summary

- The cleaned dataset covers 2010-12-01 to 2011-12-09 and contains 18,532 orders from 4,338 customers.
- Total revenue after cleaning is $8,911,407.90.
- Revenue is highly concentrated in United Kingdom, which contributes 82.0% of cleaned revenue.
- Revenue and active customers both peak in 2011-11, showing a strong late-year sales period.
- RFM segmentation separates customers into four groups with different retention and marketing priorities.

## Key EDA Findings

- Average order value is $480.87, while the median order value is $303.04. This means larger orders pull the average upward.
- The top revenue market is United Kingdom; the top 10 countries together contribute 96.9% of revenue.
- The top product by revenue is "PAPER CRAFT , LITTLE BIRDIE".
- The top 10 products contribute 9.9% of revenue, so revenue is less concentrated by product than by country.
- Active customers peak in 2011-11, with 1,664 active customers.

## Segment Summary

| Segment | Customers | Avg Recency | Avg Frequency | Avg Monetary | Total Revenue | Revenue % |
|---|---:|---:|---:|---:|---:|---:|
| Low-Value or One-Time Buyers | 3,052 | 43.9 | 3.7 | $1,350.14 | $4,120,628.90 | 46.2% |
| Potential Loyal Customers | 211 | 15.7 | 22.0 | $12,453.23 | $2,627,630.67 | 29.5% |
| High-Value Loyal Customers | 13 | 7.4 | 82.5 | $127,338.31 | $1,655,398.08 | 18.6% |
| At-Risk Customers | 1,062 | 248.6 | 1.6 | $478.11 | $507,750.25 | 5.7% |

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
