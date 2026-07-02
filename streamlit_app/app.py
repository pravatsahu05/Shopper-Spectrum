import streamlit as st

from components.sidebar import render_sidebar
from components.ui import load_css, page_header, section_card


st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="SS",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
render_sidebar()

page_header(
    "Shopper Spectrum",
    "A polished retail intelligence application that turns transaction data into customer segments, product recommendations, and executive business actions.",
    pills=["RFM Segmentation", "Recommendation Engine", "Executive Insights", "Deployment Ready"],
)

col1, col2, col3 = st.columns(3)

with col1:
    section_card(
        "Business Dashboard",
        "Explore revenue, countries, top products, seasonality, and segment performance with interactive filters.",
    )

with col2:
    section_card(
        "Customer Segmentation",
        "Enter RFM values and classify a customer into a business-friendly segment with recommended next actions.",
    )

with col3:
    section_card(
        "Product Recommendations",
        "Search a product and discover likely complementary items for cross-sell and bundle campaigns.",
    )

st.info(
    "Use the sidebar to open each page. Every page is written for recruiters and business readers, with clear insights and practical recommendations."
)
