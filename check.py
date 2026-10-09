import pandas as pd
import numpy as np

# Load datasets
df_market = pd.read_csv('Global_EV_Market_Dataset_2020_2026.csv')
df_insights = pd.read_csv('EV_vs_Fuel_Engines_and_Customer_Insights.csv')

print("--- INITIAL PREPROCESSING CHECK ---")
print("Dataset 1 Missing Values:", df_market.isnull().sum().sum())
print("Dataset 2 Missing Values:", df_insights.isnull().sum().sum())

# Feature Engineering Example: Calculate Total Revenue or Cost Metrics
df_market['Total_Market_Revenue'] = df_market['Sales_Volume'] * df_market['Average_Price_USD']
df_insights['Total_Segment_Revenue'] = df_insights['Sales_Volume'] * df_insights['Average_Price_USD']

print("\nFeature engineering complete! Added 'Total_Market_Revenue' and 'Total_Segment_Revenue'.")
print(df_market[['Year', 'Country', 'Vehicle_Type', 'Sales_Volume', 'Total_Market_Revenue']].head(2))