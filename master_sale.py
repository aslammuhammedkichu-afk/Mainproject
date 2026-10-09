import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Load dataset
print("Loading 'EV_vs_Fuel_Engines_and_Customer_Insights.csv'...")
df = pd.read_csv('EV_vs_Fuel_Engines_and_Customer_Insights.csv')

# 2. Aggregate historical sales by Year and Powertrain Type
ev_hist = df[df['Powertrain_Type'] == 'EV'].groupby('Year')['Sales_Volume'].sum().reset_index()
ev_hist['Vehicle_Type'] = 'EV'

ice_hist = df[df['Powertrain_Type'].isin(['Petrol_ICE', 'Diesel_ICE'])].groupby('Year')['Sales_Volume'].sum().reset_index()
ice_hist['Vehicle_Type'] = 'ICE_Fuel'

# Combine historical data
history_combined = pd.concat([ev_hist, ice_hist])

# 3. Train models to forecast 2027 - 2030
model_ev = LinearRegression().fit(ev_hist[['Year']], ev_hist['Sales_Volume'])
model_ice = LinearRegression().fit(ice_hist[['Year']], ice_hist['Sales_Volume'])

future_years = np.array([[2027], [2028], [2029], [2030]])
pred_ev = model_ev.predict(future_years)
pred_ice = model_ice.predict(future_years)

# Create forecast dataframe
forecast_data = []
for yr, ev_val, ice_val in zip(future_years.flatten(), pred_ev, pred_ice):
    forecast_data.append({'Year': yr, 'Sales_Volume': int(ev_val), 'Vehicle_Type': 'EV', 'Data_Type': 'Forecast'})
    forecast_data.append({'Year': yr, 'Sales_Volume': int(ice_val), 'Vehicle_Type': 'ICE_Fuel', 'Data_Type': 'Forecast'})

history_combined['Data_Type'] = 'Historical'
forecast_df = pd.DataFrame(forecast_data)

# 4. Merge everything into one master file for Power BI
master_df = pd.concat([history_combined, forecast_df], ignore_index=True)
master_df.to_csv('master_ev_vs_ice_timeline_2030.csv', index=False)

print("\n" + "="*65)
print("Success! Combined historical & forecast data saved to 'master_ev_vs_ice_timeline_2030.csv'.")
print("="*65)