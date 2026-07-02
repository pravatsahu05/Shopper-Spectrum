import plotly.express as px
import streamlit as st

from components.sidebar import render_sidebar
from components.ui import CHART_TEMPLATE, insight, load_css, page_header, section_card, style_chart
from utils import load_clean_data, load_customer_segments


st.set_page_config(page_title="Business Insights", page_icon="Insights", layout="wide")

load_css()
render_sidebar()

clean_df = load_clean_data()
rfm = load_customer_segments()

total_revenue = clean_df["Revenue"].sum()
customers = clean_df["CustomerID"].nunique()
products = clean_df["Description"].nunique()
countries = clean_df["Country"].nunique()

page_header(
    "Executive Business Insights",
    "A recruiter-friendly summary of the commercial story: where revenue is concentrated, which customers matter most, and what actions should come next.",
    pills=["Boardroom Summary", "Risks", "Growth Levers", "Recommendations"],
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"INR {total_revenue:,.0f}")
c2.metric("Customers", f"{customers:,}")
c3.metric("Products", f"{products:,}")
c4.metric("Countries", f"{countries:,}")

st.subheader("Top Business Findings")
findings = [
    ("Revenue concentration", "Sales are led by a small number of countries, creating both focus and expansion opportunities."),
    ("Segment opportunity", "Regular Customers form a large base that can be moved upward through loyalty and personalization."),
    ("High-value retention", "Premium and High-Value customers deserve dedicated retention because their spend per customer is materially higher."),
    ("Product strategy", "Popular home and gift products can anchor bundles and cross-sell campaigns."),
    ("Recommendation value", "Item similarity reveals natural add-on products that can raise average order value."),
    ("Churn prevention", "At-Risk customers should receive timely win-back campaigns before they become inactive."),
]

cols = st.columns(2)
for index, (title, body) in enumerate(findings):
    with cols[index % 2]:
        section_card(title, body)

segment_revenue = rfm.groupby("Segment", as_index=False)["Monetary"].sum()
fig = px.bar(
    segment_revenue,
    x="Segment",
    y="Monetary",
    color="Monetary",
    color_continuous_scale="Greens",
    title="Revenue Contribution by Customer Segment",
    template=CHART_TEMPLATE,
)
style_chart(fig)
st.plotly_chart(fig, use_container_width=True)
insight(
    "Customer Value Concentration",
    "Premium and High-Value customers may be smaller groups, but they carry a large revenue role. Losing them would hurt more than losing an average customer.",
)

country = (
    clean_df.groupby("Country", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
    .head(10)
)
fig = px.bar(
    country,
    x="Country",
    y="Revenue",
    color="Revenue",
    color_continuous_scale="Teal",
    title="Top Revenue Generating Countries",
    template=CHART_TEMPLATE,
)
style_chart(fig)
st.plotly_chart(fig, use_container_width=True)
insight(
    "Market Expansion Signal",
    "The strongest market should remain protected, while underperforming countries can be tested with localized campaigns and curated product ranges.",
)

st.subheader("Business Risks")
risk_cols = st.columns(2)
risks = [
    "Heavy revenue dependence on a small set of markets.",
    "A small VIP base means premium retention must be intentional.",
    "At-Risk customers can quietly reduce lifetime value if not contacted.",
    "Seasonal demand may create stockouts or underused inventory.",
]
for index, risk in enumerate(risks):
    with risk_cols[index % 2]:
        insight("Risk", risk, tone="risk")

st.subheader("Strategic Recommendations")
recommendations = [
    "Launch tiered loyalty programs for Regular and Loyal customers.",
    "Create VIP retention journeys for Premium and High-Value customers.",
    "Use recommendation outputs for bundles, checkout add-ons, and email campaigns.",
    "Build win-back campaigns for At-Risk customers with time-sensitive offers.",
    "Monitor seasonal sales patterns before procurement and staffing decisions.",
    "Retrain models as new transaction data arrives so segments stay current.",
]
for number, recommendation in enumerate(recommendations, start=1):
    insight(f"Recommendation {number}", recommendation, tone="recommendation")

insight(
    "Executive Conclusion",
    "The project demonstrates a practical machine learning workflow that does more than predict. It explains customer behavior and converts model outputs into decisions a business team can act on.",
    tone="action",
)
