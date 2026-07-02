import streamlit as st

from components.sidebar import render_sidebar
from components.ui import load_css, page_header, section_card, timeline
from utils import load_clean_data


st.set_page_config(page_title="About Project", page_icon="About", layout="wide")

load_css()
render_sidebar()

clean_df = load_clean_data()

page_header(
    "About Shopper Spectrum",
    "An end-to-end data science project for e-commerce customer intelligence, built to be readable by both technical reviewers and business stakeholders.",
    pills=["Python", "Pandas", "Scikit-Learn", "Plotly", "Streamlit"],
)

st.subheader("Project Overview")
section_card(
    "Business Problem",
    "Retail transaction data is valuable, but it is difficult to act on without segmentation and recommendation systems. Shopper Spectrum turns transaction history into customer groups, product relationships, and clear business actions.",
)

st.subheader("Machine Learning Pipeline")
timeline(
    [
        "Raw transactions",
        "Cleaning and validation",
        "Exploratory analysis",
        "RFM feature engineering",
        "Standard scaling",
        "K-Means clustering",
        "Item-based filtering",
        "Streamlit deployment",
    ]
)

st.subheader("Dataset Snapshot")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Transactions", f"{len(clean_df):,}")
col2.metric("Customers", f"{clean_df['CustomerID'].nunique():,}")
col3.metric("Products", f"{clean_df['Description'].nunique():,}")
col4.metric("Countries", f"{clean_df['Country'].nunique():,}")

st.subheader("Key Features")
feature_cols = st.columns(3)
with feature_cols[0]:
    section_card("Interactive Dashboard", "Revenue, country, product, seasonal, and segment views with filters for exploration.")
with feature_cols[1]:
    section_card("Customer Segmentation", "RFM inputs are transformed and classified with the saved K-Means model.")
with feature_cols[2]:
    section_card("Recommendation Engine", "Collaborative filtering suggests related products for cross-sell and bundle campaigns.")

st.subheader("Portfolio Value")
left, right = st.columns(2)
with left:
    section_card(
        "Technical Skills Demonstrated",
        "Data cleaning, feature engineering, clustering, similarity modeling, model serialization, visualization, and Streamlit application design.",
    )
with right:
    section_card(
        "Business Skills Demonstrated",
        "Insight writing, prioritization, executive storytelling, campaign recommendations, and translating ML output into decisions.",
    )

st.subheader("Future Enhancements")
future_cols = st.columns(2)
with future_cols[0]:
    section_card(
        "Model Improvements",
        "Add churn prediction, customer lifetime value estimation, sales forecasting, and automated model retraining.",
    )
with future_cols[1]:
    section_card(
        "Deployment Improvements",
        "Connect a cloud database, add user authentication, expose recommendations through an API, and schedule data refreshes.",
    )

st.subheader("Developer")
st.markdown(
    """
    **Project:** Shopper Spectrum  
    **Domain:** Data Science and Machine Learning  
    **Author:** Pravat Sahu  
    **Purpose:** Academic and portfolio project
    """
)

st.caption("Copyright 2026 Shopper Spectrum. End-to-end data science portfolio project.")
