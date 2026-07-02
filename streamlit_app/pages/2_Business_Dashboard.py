import pandas as pd
import plotly.express as px
import streamlit as st

from components.sidebar import render_sidebar
from components.ui import CHART_COLORS, CHART_TEMPLATE, insight, load_css, page_header, style_chart
from utils import load_clean_data, load_customer_segments


st.set_page_config(page_title="Business Dashboard", page_icon="Dashboard", layout="wide")

load_css()
render_sidebar()

clean_df = load_clean_data()
rfm = load_customer_segments()

clean_df["Year"] = clean_df["InvoiceDate"].dt.year
clean_df["Month"] = clean_df["InvoiceDate"].dt.strftime("%B")

st.sidebar.header("Dashboard Filters")
selected_country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(clean_df["Country"].dropna().unique().tolist()),
)
selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(clean_df["Year"].dropna().unique().tolist()),
)

filtered_df = clean_df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

revenue = filtered_df["Revenue"].sum()
customers = filtered_df["CustomerID"].nunique()
orders = filtered_df["InvoiceNo"].nunique()
average_order = revenue / orders if orders else 0

page_header(
    "Business Dashboard",
    "Explore where revenue comes from, which products create demand, and how customer segments influence commercial strategy.",
    pills=[f"Country: {selected_country}", f"Year: {selected_year}", "Interactive Filters"],
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Revenue", f"INR {revenue:,.0f}")
col2.metric("Customers", f"{customers:,}")
col3.metric("Orders", f"{orders:,}")
col4.metric("Average Order Value", f"INR {average_order:,.2f}")

if filtered_df.empty:
    st.warning("No transactions match the selected filters. Choose a wider country or year filter.")
    st.stop()

chart_template = CHART_TEMPLATE

country_sales = (
    filtered_df.groupby("Country", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
    .head(10)
)
fig = px.bar(
    country_sales,
    x="Country",
    y="Revenue",
    color="Revenue",
    color_continuous_scale="Teal",
    title="Top 10 Countries by Revenue",
    template=chart_template,
)
style_chart(fig)
st.plotly_chart(fig, use_container_width=True)
insight(
    "Market Concentration",
    "Revenue is concentrated in a small set of countries. This is useful for prioritizing core markets, but it also signals a growth opportunity in underpenetrated regions.",
)

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
monthly = filtered_df.groupby("Month", as_index=False)["Revenue"].sum()
monthly["Month"] = pd.Categorical(monthly["Month"], categories=month_order, ordered=True)
monthly = monthly.sort_values("Month")
fig = px.line(
    monthly,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend",
    template=chart_template,
)
fig.update_traces(line_color=CHART_COLORS["blue"], marker_size=8)
style_chart(fig)
st.plotly_chart(fig, use_container_width=True)
insight(
    "Seasonality",
    "Revenue peaks show when promotions, inventory planning, and staffing should be strongest. These periods are ideal for campaign testing and product bundling.",
)

left, right = st.columns(2)
with left:
    top_products = (
        filtered_df.groupby("Description", as_index=False)["Quantity"]
        .sum()
        .sort_values("Quantity", ascending=False)
        .head(10)
    )
    fig = px.bar(
        top_products,
        x="Quantity",
        y="Description",
        orientation="h",
        title="Top 10 Selling Products",
        template=chart_template,
        color="Quantity",
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

with right:
    segment_counts = rfm["Segment"].value_counts().reset_index()
    segment_counts.columns = ["Segment", "Customers"]
    fig = px.pie(
        segment_counts,
        names="Segment",
        values="Customers",
        hole=0.55,
        title="Customer Segment Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2,
        template=chart_template,
    )
    style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

insight(
    "Merchandising Signal",
    "Best-selling products should remain consistently stocked and can anchor bundles with recommendation-engine products to raise average order value.",
    tone="action",
)

segment_monetary = rfm.groupby("Segment", as_index=False)["Monetary"].mean()
fig = px.bar(
    segment_monetary,
    x="Segment",
    y="Monetary",
    color="Monetary",
    color_continuous_scale="Greens",
    title="Average Spending by Customer Segment",
    template=chart_template,
)
style_chart(fig)
st.plotly_chart(fig, use_container_width=True)
insight(
    "Retention Priority",
    "Premium and High-Value customers contribute far more per customer. They should receive the strongest retention offers, early access, and personalized recommendations.",
)
