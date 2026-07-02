import joblib
import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

from config import (
    CLEAN_DATA,
    CUSTOMER_SEGMENTS,
    KMEANS_MODEL_PATH,
    PRODUCT_NAMES_PATH,
    SCALER_PATH,
    SIMILARITY_MATRIX_PATH,
)


@st.cache_data
def load_clean_data():
    return pd.read_csv(CLEAN_DATA, parse_dates=["InvoiceDate"])


@st.cache_data
def load_customer_segments():
    return pd.read_csv(CUSTOMER_SEGMENTS)


@st.cache_resource
def load_scaler():
    return joblib.load(SCALER_PATH)


@st.cache_resource
def load_kmeans():
    return joblib.load(KMEANS_MODEL_PATH)


@st.cache_resource
def load_similarity():
    if SIMILARITY_MATRIX_PATH.exists():
        return joblib.load(SIMILARITY_MATRIX_PATH)

    clean_df = pd.read_csv(
        CLEAN_DATA,
        usecols=["CustomerID", "Description", "Quantity"],
    )

    customer_product_matrix = pd.pivot_table(
        clean_df,
        index="CustomerID",
        columns="Description",
        values="Quantity",
        aggfunc="sum",
        fill_value=0,
    )

    customer_product_matrix = (customer_product_matrix > 0).astype(int)
    product_customer_matrix = customer_product_matrix.T
    similarity_matrix = cosine_similarity(product_customer_matrix)

    return pd.DataFrame(
        similarity_matrix,
        index=product_customer_matrix.index,
        columns=product_customer_matrix.index,
    )


@st.cache_resource
def load_product_names():
    return joblib.load(PRODUCT_NAMES_PATH)


def recommend_products(product_name, similarity_df, top_n=5):
    if product_name not in similarity_df.index:
        return pd.DataFrame(
            columns=[
                "Recommended Product",
                "Similarity Score",
                "Recommendation Strength",
            ]
        )

    recommendations = (
        similarity_df[product_name]
        .sort_values(ascending=False)
        .iloc[1 : top_n + 1]
    )

    recommendation_df = pd.DataFrame(
        {
            "Recommended Product": recommendations.index,
            "Similarity Score": recommendations.values.round(3),
        }
    )
    recommendation_df["Recommendation Strength"] = recommendation_df[
        "Similarity Score"
    ].apply(recommendation_strength)
    return recommendation_df


def recommendation_strength(score):
    if score >= 0.90:
        return "Excellent match"
    if score >= 0.80:
        return "Very strong match"
    if score >= 0.70:
        return "Strong match"
    if score >= 0.60:
        return "Moderate match"
    return "Weak match"
