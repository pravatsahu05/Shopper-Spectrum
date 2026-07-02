import streamlit as st

from components.sidebar import render_sidebar
from components.ui import load_css, page_header, section_card, timeline
from utils import load_clean_data, load_customer_segments


st.set_page_config(page_title="Home", page_icon="Home", layout="wide")

load_css()
render_sidebar()

clean_df = load_clean_data()
rfm = load_customer_segments()

total_customers = clean_df["CustomerID"].nunique()
total_products = clean_df["Description"].nunique()
total_countries = clean_df["Country"].nunique()
total_revenue = clean_df["Revenue"].sum()
largest_segment = rfm["Segment"].value_counts().idxmax()

page_header(
    "Retail Intelligence That Reads Like a Business Case",
    "Shopper Spectrum combines RFM segmentation, K-Means clustering, and item-based recommendations so a retail team can identify valuable customers, recover churn risk, and grow basket value.",
    pills=["Customer 360", "Revenue Analytics", "Cross-Sell Strategy", "Portfolio Project"],
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", f"{total_customers:,}")
col2.metric("Products", f"{total_products:,}")
col3.metric("Countries", f"{total_countries:,}")
col4.metric("Revenue", f"INR {total_revenue:,.0f}")

st.subheader("What This Application Solves")
overview_cols = st.columns(3)
with overview_cols[0]:
    section_card(
        "Segment Customers",
        f"Customers are grouped by recency, frequency, and monetary value. The largest current group is {largest_segment}, making retention and repeat purchase programs especially important.",
    )
with overview_cols[1]:
    section_card(
        "Recommend Products",
        "The recommendation engine finds products that are frequently purchased in similar baskets, supporting bundles, cross-sell offers, and merchandising decisions.",
    )
with overview_cols[2]:
    section_card(
        "Explain Business Actions",
        "Each page translates model outputs into plain-language insights, risks, and recommended actions for marketing and operations teams.",
    )

st.subheader("Project Workflow")
timeline(
    [
        "Raw retail transactions",
        "Data cleaning",
        "Exploratory analysis",
        "RFM feature engineering",
        "Feature scaling",
        "K-Means segmentation",
        "Collaborative filtering",
        "Executive dashboard",
    ]
)

st.subheader("Why Recruiters Should Notice")
left, right = st.columns(2)
with left:
    section_card(
        "End-to-End Ownership",
        "The project covers data preparation, machine learning, model persistence, visual analytics, business interpretation, and deployment-ready Streamlit packaging.",
    )
with right:
    section_card(
        "Business Communication",
        "The interface avoids raw technical output as the final answer. It presents insights, recommendations, and decisions in the language of retail growth.",
    )

st.caption("Developed by Pravat Sahu as an end-to-end data science and machine learning portfolio project.")
