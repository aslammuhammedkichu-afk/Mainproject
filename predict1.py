import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Load your exact CSV file from the workspace
print("Loading 'Global_EV_Market_Dataset_2020_2026.csv'...")
df = pd.read_csv('Global_EV_Market_Dataset_2020_2026.csv')

# 2. Group historical sales by Year
yearly_sales = df.groupby('Year')['Sales_Volume'].sum().reset_index()

# 3. Set up machine learning variables
X = yearly_sales[['Year']]
y = yearly_sales['Sales_Volume']

# 4. Train the Linear Regression model
model = LinearRegression()
model.fit(X, y)

# 5. Predict future sales for years 2027 to 2030
future_years = np.array([[2027], [2028], [2029], [2030]])
predicted_sales = model.predict(future_years)

print("\n" + "="*50)
print("--- GLOBAL MARKET SALES FORECAST (2027 - 2030) ---")
print("="*50)

forecast_data = []
for yr, sales in zip(future_years.flatten(), predicted_sales):
    val = int(sales)
    print(f"Year {yr}: Predicted Sales Volume = {val:,}")
    forecast_data.append({'Year': yr, 'Predicted_Sales_Volume': val})

# 6. Save the forecast results to a CSV file for Power BI
df_forecast = pd.DataFrame(forecast_data)
df_forecast.to_csv('ev_sales_forecast_2030.csv', index=False)

print("\n" + "="*50)
print("Success! Forecast saved to 'ev_sales_forecast_2030.csv'.")
print("="*50)