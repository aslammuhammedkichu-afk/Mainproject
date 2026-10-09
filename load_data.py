import pandas as pd
from sqlalchemy import create_engine

# 1. Load your datasets into Pandas dataframes
print("Loading datasets...")
df_market = pd.read_csv('Global_EV_Market_Dataset_2020_2026.csv')
df_insights = pd.read_csv('EV_vs_Fuel_Engines_and_Customer_Insights.csv')

# 2. Connect to your MySQL database password
print("Connecting to MySQL database 'ev_project'...")
engine = create_engine('mysql+pymysql://root:223344@localhost:3306/ev_project')

# 3. Automatically create tables and insert all rows
print("Uploading market dataset to MySQL...")
df_market.to_sql('market', con=engine, if_exists='replace', index=False)

print("Uploading insights dataset to MySQL...")
df_insights.to_sql('insights', con=engine, if_exists='replace', index=False)

print("SUCCESS: All data successfully loaded into MySQL!")