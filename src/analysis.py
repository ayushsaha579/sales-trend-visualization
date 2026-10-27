from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"Order ID", "Order Date", "Category", "Region", "Sales", "Quantity"}

def load_sales_data(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Sales dataset not found: {path}")
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "Dataset is missing required columns: " + ", ".join(sorted(missing))
        )
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df = df.dropna(subset=["Order ID", "Order Date", "Category", "Region", "Sales", "Quantity"])
    return df

def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    result = (df.assign(Month=df["Order Date"].dt.to_period("M").dt.to_timestamp())
              .groupby("Month", as_index=False)["Sales"].sum()
              .sort_values("Month"))
    return result

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("Category", as_index=False)["Sales"].sum()
            .sort_values("Sales", ascending=False))

def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("Region", as_index=False)["Sales"].sum()
            .sort_values("Sales", ascending=False))

def kpi_summary(df: pd.DataFrame) -> dict:
    total_sales = float(df["Sales"].sum())
    total_orders = int(df["Order ID"].nunique())
    units_sold = int(df["Quantity"].sum())
    average_order_value = total_sales / total_orders if total_orders else 0.0
    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "average_order_value": average_order_value,
        "units_sold": units_sold,
    }
