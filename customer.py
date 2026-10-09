import pandas as pd

# 1. Load your comprehensive dataset
print("Loading 'EV_vs_Fuel_Engines_and_Customer_Insights.csv'...")
df = pd.read_csv('EV_vs_Fuel_Engines_and_Customer_Insights.csv')

# 2. Analyze Customer Primary Preferences by Powertrain Type
preference_summary = df.groupby(['Powertrain_Type', 'Customer_Primary_Preference'])['Sales_Volume'].sum().reset_index()
preference_summary.rename(columns={'Sales_Volume': 'Total_Sales_Volume'}, inplace=True)

# 3. Analyze Average Customer Satisfaction Ratings by Powertrain Type
satisfaction_summary = df.groupby('Powertrain_Type')['Customer_Satisfaction_Rating'].mean().reset_index()

print("\n" + "="*50)
print("--- CUSTOMER PRIMARY PREFERENCE SUMMARY ---")
print("="*50)
print(preference_summary.head(10))

# 4. Save these insights into separate CSV files for Power BI
preference_summary.to_csv('customer_preferences_analysis.csv', index=False)
satisfaction_summary.to_csv('customer_satisfaction_analysis.csv', index=False)

print("\n" + "="*50)
print("Success! Customer insights saved to 'customer_preferences_analysis.csv' & 'customer_satisfaction_analysis.csv'.")
print("="*50)