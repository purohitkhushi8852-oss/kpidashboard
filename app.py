"""
Business KPI Dashboard
-----------------------
A single-file Streamlit app tracking Revenue, Profit, and Customer Growth
across regions and segments, with monthly trend charts and interactive
filters. Built with Plotly for visuals.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# PAGE CONFIG & STYLE
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Business KPI Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .block-container {padding-top: 1.6rem; padding-bottom: 2rem;}
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #eaeaea;
        border-radius: 12px;
        padding: 14px 18px 10px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetricLabel"] {font-size: 0.85rem; color: #6b7280;}
    section[data-testid="stSidebar"] {background-color: #f6f7fb;}
    h1, h2, h3 {font-family: 'Segoe UI', sans-serif; color: #1f2a44;}
    .footer-note {color: #9ca3af; font-size: 0.8rem; margin-top: 2rem;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

TEMPLATE = "plotly_white"
COLOR_SEQ = px.colors.qualitative.Set2


# ----------------------------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------------------------
@st.cache_data
def load_data(path: str = "data.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Date"])
    df["Month_Label"] = df["Date"].dt.strftime("%b %Y")
    return df


try:
    raw_df = load_data()
except FileNotFoundError:
    st.error("`data.csv` not found. Make sure it sits next to app.py in the project folder.")
    st.stop()

if raw_df.empty:
    st.warning("The dataset is empty — nothing to show yet.")
    st.stop()

# ----------------------------------------------------------------------------
# SIDEBAR — FILTERS
# ----------------------------------------------------------------------------
st.sidebar.title("🔎 Filters")

min_date, max_date = raw_df["Date"].min(), raw_df["Date"].max()
date_range = st.sidebar.date_input(
    "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date,
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

region_options = sorted(raw_df["Region"].unique())
selected_regions = st.sidebar.multiselect("Region", region_options, default=region_options)

segment_options = sorted(raw_df["Segment"].unique())
selected_segments = st.sidebar.multiselect("Segment", segment_options, default=segment_options)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit + Plotly · Demo business dataset (2024–2025)")

# ----------------------------------------------------------------------------
# APPLY FILTERS
# ----------------------------------------------------------------------------
mask = (
    (raw_df["Date"] >= pd.to_datetime(start_date))
    & (raw_df["Date"] <= pd.to_datetime(end_date))
    & (raw_df["Region"].isin(selected_regions))
    & (raw_df["Segment"].isin(selected_segments))
)
df = raw_df.loc[mask].copy()

st.title("📈 Business KPI Dashboard")
st.caption("Track revenue, profitability, and customer growth across regions and segments.")

if df.empty:
    st.info("No records match the current filters. Try widening the date range or selections.")
    st.stop()

# ----------------------------------------------------------------------------
# KPI ROW
# ----------------------------------------------------------------------------
total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0
new_customers = df["New_Customers"].sum()

# Customer growth rate: compare total customers at end vs start of filtered period
month_end_totals = df.groupby("Date")["Total_Customers"].sum().sort_index()
if len(month_end_totals) >= 2:
    start_customers = month_end_totals.iloc[0]
    end_customers = month_end_totals.iloc[-1]
    customer_growth_rate = ((end_customers - start_customers) / start_customers * 100) if start_customers else 0
else:
    customer_growth_rate = 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
k2.metric("📈 Total Profit", f"${total_profit:,.0f}")
k3.metric("🧮 Profit Margin", f"{profit_margin:.1f}%")
k4.metric("🧑‍🤝‍🧑 New Customers", f"{new_customers:,}")
k5.metric("🚀 Customer Growth", f"{customer_growth_rate:.1f}%")

st.markdown("---")

# ----------------------------------------------------------------------------
# ROW 1 — Monthly Revenue & Profit Trend
# ----------------------------------------------------------------------------
st.subheader("Monthly Revenue & Profit Trend")
trend_df = df.groupby("Date", as_index=False).agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
trend_df = trend_df.sort_values("Date")
fig_trend = px.line(
    trend_df, x="Date", y=["Revenue", "Profit"], markers=True,
    template=TEMPLATE, color_discrete_sequence=["#2563eb", "#16a34a"],
)
fig_trend.update_layout(yaxis_title="Amount ($)", xaxis_title="Month", legend_title="")
st.plotly_chart(fig_trend, use_container_width=True)

# ----------------------------------------------------------------------------
# ROW 2 — Customer Growth (cumulative + new customers)
# ----------------------------------------------------------------------------
st.subheader("Customer Growth")
cust_df = df.groupby("Date", as_index=False).agg(
    Total_Customers=("Total_Customers", "sum"), New_Customers=("New_Customers", "sum")
).sort_values("Date")

fig_cust = go.Figure()
fig_cust.add_trace(go.Bar(
    x=cust_df["Date"], y=cust_df["New_Customers"], name="New Customers",
    marker_color="#93c5fd", yaxis="y1",
))
fig_cust.add_trace(go.Scatter(
    x=cust_df["Date"], y=cust_df["Total_Customers"], name="Total Customers",
    mode="lines+markers", line=dict(color="#1d4ed8", width=3), yaxis="y2",
))
fig_cust.update_layout(
    template=TEMPLATE,
    yaxis=dict(title="New Customers"),
    yaxis2=dict(title="Total Customers", overlaying="y", side="right"),
    xaxis_title="Month",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_cust, use_container_width=True)

# ----------------------------------------------------------------------------
# ROW 3 — Revenue by Region | Revenue by Segment
# ----------------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Revenue by Region")
    region_df = df.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    fig_region = px.bar(
        region_df, x="Region", y="Revenue", text_auto=".2s",
        color="Region", color_discrete_sequence=COLOR_SEQ, template=TEMPLATE,
    )
    fig_region.update_layout(showlegend=False, yaxis_title="Revenue ($)", xaxis_title="")
    st.plotly_chart(fig_region, use_container_width=True)

with c2:
    st.subheader("Revenue by Segment")
    segment_df = df.groupby("Segment", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    fig_segment = px.pie(
        segment_df, names="Segment", values="Revenue", hole=0.45,
        color_discrete_sequence=COLOR_SEQ, template=TEMPLATE,
    )
    fig_segment.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_segment, use_container_width=True)

# ----------------------------------------------------------------------------
# DETAIL TABLE
# ----------------------------------------------------------------------------
with st.expander("🔍 View filtered raw data"):
    st.dataframe(
        df.sort_values("Date", ascending=False).drop(columns=["Month_Label"]).reset_index(drop=True),
        use_container_width=True,
    )
    st.download_button(
        "Download filtered data as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_kpi_data.csv",
        mime="text/csv",
    )

st.markdown(
    '<p class="footer-note">Business KPI Dashboard · Demo project · Data is synthetic, '
    'generated for educational / prototyping purposes.</p>',
    unsafe_allow_html=True,
)
