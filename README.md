# Sales Trend Visualization — Data Analytics Project

A beginner-friendly sales analytics dashboard built with Python, Pandas, Matplotlib, and Streamlit.

## Features
- Total sales, order count, average order value, and units sold KPIs
- Monthly sales trend line chart
- Sales by category and region
- Date, category, and region filters
- Recent transaction table
- Download filtered data as CSV
- Synthetic sample dataset included

## Project structure
```text
sales-trend-visualization/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sales_data.csv
├── src/
│   ├── __init__.py
│   └── analysis.py
└── outputs/
```

## Run on Windows (VS Code)
1. Extract the ZIP file.
2. Open the extracted `sales-trend-visualization` folder in VS Code.
3. Open Terminal → New Terminal.
4. (Recommended) Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt:
   ```bat
   .venv\Scripts\activate.bat
   ```
5. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Launch the dashboard:
   ```powershell
   python -m streamlit run app.py
   ```
7. Open the local URL Streamlit prints, usually `http://localhost:8501`.

**Important:** Do not run this app using `python app.py`; launch it with `streamlit run app.py`.

## Dataset columns
- `Order ID`: unique transaction/order identifier
- `Order Date`: order date
- `Category`: product category
- `Region`: sales region
- `Sales`: revenue amount
- `Quantity`: units sold

The included dataset is generated synthetic data for practice, not real company data. Replace `data/sales_data.csv` with your own data while preserving the required column names.
