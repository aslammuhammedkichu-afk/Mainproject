# EV Market Analysis and Forecasting

A Python-based project for exploring electric vehicle (EV) market trends, comparing EVs with internal-combustion-engine (ICE) vehicles, and analyzing sales and customer insights.

**GitHub repository:** https://github.com/aslammuhammedkichu-afk/Mainproject

## Project Overview

This project brings together datasets and Python scripts for market analysis, visualization, and forecasting. The workspace includes files related to:

- EV market data covering 2020–2026
- EV sales forecasting through 2030
- EV versus ICE comparisons and timelines
- Customer preferences and customer satisfaction analysis
- Dashboard development and exploratory analysis

## Features

- **Market analysis:** Explore EV market data and trends.
- **Sales forecasting:** Use a Linear Regression model to estimate future sales from yearly historical sales totals.
- **EV vs. ICE comparison:** Review comparison datasets and timeline information.
- **Customer insights:** Analyze customer preferences and satisfaction datasets.
- **Visualization/dashboard:** Build a dashboard to present findings.

> Forecasts are estimates based on the data and model used; they should not be treated as guaranteed future outcomes.

## Project Files

The repository currently includes files such as:

| File | Purpose |
|---|---|
| `Global_EV_Market_Dataset_2020_2026.csv` | Main EV market dataset |
| `ev_sales_forecast_2030.csv` | EV sales forecast output/data |
| `ev_vs_ice_comparison_2030.csv` | EV and ICE comparison data |
| `master_ev_vs_ice_timeline_2030.csv` | EV vs. ICE timeline data |
| `customer_preferences_analysis.csv` | Customer preferences analysis data |
| `customer_satisfaction_analysis.csv` | Customer satisfaction analysis data |
| `ev_dashboard.py` | Dashboard application/script |
| `predict1.py` | Sales forecasting with Linear Regression |
| `predict_comparison.py` | EV/ICE prediction or comparison script |
| `customer.py` | Customer analysis script |
| `master_sale.py` | Sales analysis script |
| `load_data.py` | Data-loading utilities |
| `check.py` | Checks or testing script |

File purposes are inferred from their names and may need updating to match the final implementation.

## Tech Stack

- Python
- pandas
- NumPy
- scikit-learn
- CSV datasets
- Visual Studio Code

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/aslammuhammedkichu-afk/Mainproject.git
cd Mainproject
```

### 2. Create and activate a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the packages used by the scripts:

```bash
pip install pandas numpy scikit-learn
```

If the dashboard uses a framework such as Streamlit or another visualization library, install it as well. A `requirements.txt` file can be added to make setup reproducible.

### 4. Run a script

For example, to run the forecasting script:

```bash
python predict1.py
```

Run other scripts by replacing `predict1.py` with the relevant filename. Check each script's code for its expected input files and run instructions before execution.

## Forecasting Approach

The forecasting script shown in the project groups historical records by `Year`, sums `Sales_Volume` for each year, and fits a scikit-learn `LinearRegression` model using year as the input feature. Predictions depend on the dataset, model assumptions, and forecast horizon.

## Data and Privacy

- Confirm that datasets are permitted to be shared before committing them.
- Remove personal, confidential, or sensitive customer information before publishing the repository.
- Do not commit passwords, API keys, `.env` files, or private credentials.
- Document each dataset's source, license, date range, and column definitions where available.

## Future Improvements

- Add a `requirements.txt` file.
- Add data-source and dataset documentation.
- Evaluate forecast accuracy using a held-out test set and appropriate metrics.
- Add charts, screenshots, and dashboard usage instructions.
- Add automated tests and clearer run instructions for each script.

## Author

**Aslam Muhammed Kichu**

## License

No license is specified yet. Add a license file if you want to define how others may use, modify, and distribute this project.
