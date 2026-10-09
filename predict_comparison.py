import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Load the comprehensive dataset containing both EV and ICE
print("Loading 'EV_vs_Fuel_Engines_and_Customer_Insights.csv'...")
df = pd.read_csv('EV_vs_Fuel_Engines_and_Customer_Insights.csv')

# 2. Group EV sales by Year
ev_data = df[df['Powertrain_Type'] == 'EV']
yearly_ev = ev_data.groupby('Year')['Sales_Volume'].sum().reset_index()

# 3. Group ICE (Petrol + Diesel combined) sales by Year
ice_data = df[df['Powertrain_Type'].isin(['Petrol_ICE', 'Diesel_ICE'])]
yearly_ice = ice_data.groupby('Year')['Sales_Volume'].sum().reset_index()

# 4. Train Linear Regression Models for both categories
model_ev = LinearRegression()
model_ev.fit(yearly_ev[['Year']], yearly_ev['Sales_Volume'])

model_ice = LinearRegression()
model_ice.fit(yearly_ice[['Year']], yearly_ice['Sales_Volume'])

# 5. Predict future sales from 2027 to 2030
future_years = np.array([[2027], [2028], [2029], [2030]])
pred_ev = model_ev.predict(future_years)
pred_ice = model_ice.predict(future_years)

print("\n" + "="*65)
print("--- SIDE-BY-SIDE EV vs ICE SALES FORECAST (2027 - 2030) ---")
print("="*65)

comparison_data = []
for yr, ev_val, ice_val in zip(future_years.flatten(), pred_ev, pred_ice):
    ev_sales = int(ev_val)
    ice_sales = int(ice_val)
    print(f"Year {yr} -> EV Sales: {ev_sales:,}  |  ICE (Fuel) Sales: {ice_sales:,}")
    
    comparison_data.append({
        'Year': yr,
        'Predicted_EV_Sales': ev_sales,
        'Predicted_ICE_Sales': ice_sales
    })

# 6. Save into a separate new file for Power BI
df_comparison = pd.DataFrame(comparison_data)
df_comparison.to_csv('ev_vs_ice_comparison_2030.csv', index=False)

print("\n" + "="*65)
print("Success! Saved comparison to 'ev_vs_ice_comparison_2030.csv'.")
print("="*65)