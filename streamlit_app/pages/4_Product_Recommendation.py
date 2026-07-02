import streamlit as st

from components.sidebar import render_sidebar
from components.ui import insight, load_css, page_header, section_card
from utils import load_product_names, load_similarity, recommend_products


st.set_page_config(page_title="Product Recommendation", page_icon="Recommend", layout="wide")

load_css()
render_sidebar()

similarity_df = load_similarity()
product_names = load_product_names()

page_header(
    "Product Recommendation Engine",
    "Find products that behave similarly in customer baskets and turn those relationships into cross-sell, bundle, and merchandising ideas.",
    pills=["Item-Based Filtering", "Cosine Similarity", "Downloadable Output"],
)

selected_product = st.selectbox("Search or select a product", sorted(product_names))
top_n = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)

try:
    recommendations = recommend_products(selected_product, similarity_df, top_n=top_n)
except Exception as exc:
    st.error(f"Unable to generate recommendations: {exc}")
    st.stop()

if recommendations.empty:
    st.warning("No recommendations were found for this product. Try another product from the list.")
    st.stop()

top_product = recommendations.iloc[0]
st.subheader("Best Next Product to Promote")
col1, col2, col3 = st.columns([2, 1, 1])
col1.metric("Recommended Product", top_product["Recommended Product"])
col2.metric("Similarity", f"{top_product['Similarity Score']:.3f}")
col3.metric("Strength", top_product["Recommendation Strength"])

insight(
    "Cross-Sell Opportunity",
    "Customers who buy the selected product show similar purchase behavior with the recommended products. These items are strong candidates for bundles, cart add-ons, and email recommendations.",
    tone="action",
)

st.subheader("Recommendation Cards")
for rank, row in enumerate(recommendations.itertuples(index=False), start=1):
    section_card(
        f"{rank}. {row[0]}",
        f"Similarity score: {row[1]:.3f}. Recommendation strength: {row[2]}. Use this item in cross-sell placements near the selected product.",
    )

st.subheader("Recommendation Table")
st.dataframe(recommendations, use_container_width=True, hide_index=True)

summary_cols = st.columns(3)
summary_cols[0].metric("Highest Similarity", f"{recommendations['Similarity Score'].max():.3f}")
summary_cols[1].metric("Average Similarity", f"{recommendations['Similarity Score'].mean():.3f}")
summary_cols[2].metric("Products Recommended", f"{len(recommendations):,}")

insight(
    "How to Use This",
    "Higher scores indicate stronger product relationships. A business team can use these outputs to design bundles, improve product detail pages, and personalize post-purchase campaigns.",
)

st.download_button(
    label="Download Recommendations CSV",
    data=recommendations.to_csv(index=False),
    file_name="recommended_products.csv",
    mime="text/csv",
    use_container_width=True,
)

st.caption("Recommendation engine powered by item-based collaborative filtering and cosine similarity.")
