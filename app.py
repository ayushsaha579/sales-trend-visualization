from pathlib import Path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.analysis import load_sales_data, monthly_sales, sales_by_category, sales_by_region, kpi_summary

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

st.set_page_config(page_title="Sales Trend Analysis", page_icon="📈", layout="wide")
st.title("📈 Sales Trend Visualization Dashboard")
st.caption("Explore revenue trends, product categories, and regional performance.")

@st.cache_data
def get_data(path: str) -> pd.DataFrame:
    return load_sales_data(path)

try:
    df = get_data(str(DATA_PATH))
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.info("Place sales_data.csv inside the project's data folder.")
    st.stop()

if df.empty:
    st.warning("The dataset is empty.")
    st.stop()

# Filters
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df = df.dropna(subset=["Order Date"])
min_date, max_date = df["Order Date"].min().date(), df["Order Date"].max().date()

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input("Order date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    categories = ["All"] + sorted(df["Category"].dropna().astype(str).unique().tolist())
    selected_category = st.selectbox("Category", categories)
    regions = ["All"] + sorted(df["Region"].dropna().astype(str).unique().tolist())
    selected_region = st.selectbox("Region", regions)

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["Order Date"].dt.date >= start_date) &
        (filtered["Order Date"].dt.date <= end_date)
    ]
if selected_category != "All":
    filtered = filtered[filtered["Category"].astype(str) == selected_category]
if selected_region != "All":
    filtered = filtered[filtered["Region"].astype(str) == selected_region]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

kpis = kpi_summary(filtered)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"₹{kpis['total_sales']:,.0f}")
c2.metric("Total Orders", f"{kpis['total_orders']:,}")
c3.metric("Average Order Value", f"₹{kpis['average_order_value']:,.2f}")
c4.metric("Units Sold", f"{kpis['units_sold']:,}")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Monthly Sales Trend")
    trend = monthly_sales(filtered)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(trend["Month"], trend["Sales"], marker="o")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales (₹)")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right:
    st.subheader("Sales by Category")
    category_data = sales_by_category(filtered)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(category_data["Category"], category_data["Sales"])
    ax.set_ylabel("Sales (₹)")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

left, right = st.columns(2)
with left:
    st.subheader("Sales by Region")
    region_data = sales_by_region(filtered)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(region_data["Region"], region_data["Sales"])
    ax.set_ylabel("Sales (₹)")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right:
    st.subheader("Recent Transactions")
    st.dataframe(filtered.sort_values("Order Date", ascending=False).head(15), use_container_width=True)

st.subheader("Download filtered data")
csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", data=csv_bytes, file_name="filtered_sales_data.csv", mime="text/csv")

st.caption("Demo dataset is synthetic and intended for learning; replace it with your own sales records.")
