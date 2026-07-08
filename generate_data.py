"""
Generates a realistic synthetic monthly business-performance dataset for the
KPI Dashboard: revenue, profit, and customer growth across regions and
segments, with seasonality and steady customer-base growth built in.
"""
import numpy as np
import pandas as pd

np.random.seed(21)

regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
segments = ["Enterprise", "SMB", "Consumer"]

# Relative scale per region (some regions are simply bigger markets)
region_scale = {"North America": 1.3, "Europe": 1.1, "Asia Pacific": 1.0, "Latin America": 0.7}
segment_scale = {"Enterprise": 1.4, "SMB": 1.0, "Consumer": 0.6}
segment_margin = {"Enterprise": 0.28, "SMB": 0.22, "Consumer": 0.15}

months = pd.date_range("2024-01-01", "2025-12-01", freq="MS")  # 24 months
seasonality = {1: 0.85, 2: 0.85, 3: 0.95, 4: 1.0, 5: 1.0, 6: 0.95,
               7: 0.95, 8: 1.0, 9: 1.05, 10: 1.15, 11: 1.3, 12: 1.4}

rows = []
# running customer base per region/segment, grows steadily over time
running_customers = {(r, s): np.random.randint(400, 900) for r in regions for s in segments}

for i, month in enumerate(months):
    growth_trend = 1 + (i * 0.015)  # ~1.5% base monthly business growth trend
    season = seasonality[month.month]

    for region in regions:
        for segment in segments:
            base = 60000 * region_scale[region] * segment_scale[segment]
            noise = np.random.normal(1, 0.06)
            revenue = round(base * growth_trend * season * noise, 2)
            margin = segment_margin[segment] + np.random.normal(0, 0.015)
            profit = round(revenue * margin, 2)

            new_customers = int(np.random.poisson(
                lam=15 * region_scale[region] * segment_scale[segment] * growth_trend * season))
            running_customers[(region, segment)] += new_customers
            total_customers = running_customers[(region, segment)]

            rows.append({
                "Date": month.strftime("%Y-%m-%d"),
                "Region": region,
                "Segment": segment,
                "Revenue": revenue,
                "Profit": profit,
                "New_Customers": new_customers,
                "Total_Customers": total_customers,
            })

df = pd.DataFrame(rows)
df.to_csv("data.csv", index=False)
print(f"Generated {len(df)} rows across {len(months)} months -> data.csv")
print(df.head())
