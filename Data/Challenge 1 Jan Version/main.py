# --------------------------------------------
# INTRO TO AI - CHALLENGE 1: Are Sales Decreasing?
# --------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# --------------------------------------------
# 1. Load all datasets
# --------------------------------------------
funnel = pd.read_csv("transactions.csv")
analytics = pd.read_csv("analytics_data.csv")
budget = pd.read_excel("budget_units.xlsx")

scores20 = pd.read_csv("scores_20.csv")
scores21 = pd.read_csv("scores_21.csv")
scores22 = pd.read_csv("scores_22.csv")
scores23 = pd.read_csv("scores_23.csv")

# --------------------------------------------
# 2. Add Year column to each scores file
# --------------------------------------------
scores20["Year"] = 2020
scores21["Year"] = 2021
scores22["Year"] = 2022
scores23["Year"] = 2023

scores = pd.concat([scores20, scores21, scores22, scores23])

# --------------------------------------------
# 3. Inspect first few rows
# --------------------------------------------
print("TRANSACTIONS\n", funnel.head(), "\n")
print("ANALYTICS\n", analytics.head(), "\n")
print("BUDGET\n", budget.head(), "\n")
print("SCORES\n", scores.head(), "\n")

# --------------------------------------------
# 4. Are sales decreasing?
# --------------------------------------------
funnel["Date"] = pd.to_datetime(funnel["Date"], errors="coerce")
funnel["Year"] = funnel["Date"].dt.year

# Filter only final confirmed sales
sales = funnel[funnel["Status"] == "Sales"]

# Count number of sales per year
sales_per_year = sales.groupby("Year").size().reset_index(name="SalesCount")
print("\nSales per year:\n", sales_per_year)

# Plot sales trend
plt.figure(figsize=(6, 4))
plt.plot(sales_per_year["Year"], sales_per_year["SalesCount"], marker="o", linewidth=2)
plt.title("Number of Sales per Year")
plt.xlabel("Year")
plt.ylabel("Number of Sales")
plt.grid(True)
plt.tight_layout()
plt.savefig("sales_trend.png", dpi=300)
plt.close()

# Linear regression trend (slope)
X = sales_per_year["Year"].values.reshape(-1, 1)
y = sales_per_year["SalesCount"].values
model = LinearRegression().fit(X, y)

print("Trend slope:", model.coef_[0])
if model.coef_[0] < 0:
    print("→ Sales are decreasing over time.")
else:
    print("→ Sales are stable or increasing over time.")

# --------------------------------------------
# 5. Customer satisfaction by year
# --------------------------------------------
avg_scores = scores.groupby("Year").mean(numeric_only=True)
print("\nAverage satisfaction per year:\n", avg_scores)

avg_scores[["organization", "global_satisfaction"]].plot(kind="bar", figsize=(6, 4))
plt.title("Average Trip Ratings per Year")
plt.ylabel("Average Score")
plt.tight_layout()
plt.savefig("avg_satisfaction.png", dpi=300)
plt.close()

# --------------------------------------------
# 6. Budget data cleanup and merge
# --------------------------------------------
budget_long = budget.melt(
    id_vars=["Trip"],
    value_vars=["period_20", "period_21", "period_22", "period_23"],
    var_name="Period",
    value_name="Budget_Class"
)

budget_long["Year"] = budget_long["Period"].str.extract(r"(\d+)").astype(int) + 2000
print("\nBudget (reshaped):\n", budget_long.head())

# Merge with scores
merged = scores.merge(budget_long, on=["Trip", "Year"], how="left")

# Average satisfaction by budget category
budget_summary = merged.groupby("Budget_Class")[["organization", "global_satisfaction"]].mean()
print("\nAverage satisfaction by budget class:\n", budget_summary)

budget_summary.plot(kind="bar", figsize=(6, 4))
plt.title("Satisfaction by Budget Category")
plt.ylabel("Average Score")
plt.tight_layout()
plt.savefig("budget_satisfaction.png", dpi=300)
plt.close()

# --------------------------------------------
# 7. Website analytics correlations
# --------------------------------------------
# Clean percentage columns
analytics["bounce_rate"] = analytics["bounce_rate"].str.replace("%", "").astype(float)
analytics["conversion_rate"] = analytics["conversion_rate"].str.replace("%", "").astype(float)

# Scatterplot
sns.scatterplot(data=analytics, x="bounce_rate", y="conversion_rate")
plt.title("Bounce Rate vs Conversion Rate")
plt.tight_layout()
plt.savefig("bounce_vs_conversion.png", dpi=300)
plt.close()

# Correlation matrix
corr = analytics[["page_views", "bounce_rate", "conversion_rate"]].corr()
print("\nWebsite metrics correlation:\n", corr)

# --------------------------------------------
# 8. Save summary tables
# --------------------------------------------
sales_per_year.to_csv("sales_per_year.csv", index=False)
avg_scores.to_csv("avg_scores.csv")
budget_summary.to_csv("budget_summary.csv")
corr.to_csv("analytics_correlation.csv")

# --------------------------------------------
# 9. Final Summary
# --------------------------------------------
print("\n--- SUMMARY ---")
print("1️⃣ Sales trend slope:", model.coef_[0])
if model.coef_[0] < 0:
    print("   → Sales are decreasing.")
else:
    print("   → Sales are stable or increasing.")

print("2️⃣ Average satisfaction by year:\n", avg_scores)
print("3️⃣ Budget category satisfaction:\n", budget_summary)
print("4️⃣ Analytics correlation:\n", corr)
print("\n✅ Analysis complete. All figures and tables have been saved in your project folder.")
