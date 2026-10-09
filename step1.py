import pandas as pd

# Load Dataset 1: Global EV Market Trend (CSV)
df_market = pd.read_csv('Global_EV_Market_Dataset_2020_2026.csv')
print("--- DATASET 1 LOADED SUCCESSFULLY ---")
print("Shape (Rows, Columns):", df_market.shape)
print(df_market.head(2))

# Load Dataset 2: EV vs. Fuel Engines & Customer Insights (CSV)
df_insights = pd.read_csv('EV_vs_Fuel_Engines_and_Customer_Insights.csv')
print("\n--- DATASET 2 LOADED SUCCESSFULLY ---")
print("Shape (Rows, Columns):", df_insights.shape)
print(df_insights.head(2))