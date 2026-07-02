import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.sidebar import render_sidebar
from components.ui import insight, load_css, page_header, section_card, style_chart
from utils import load_customer_segments, load_kmeans, load_scaler


st.set_page_config(page_title="Customer Segmentation", page_icon="Segments", layout="wide")

load_css()
render_sidebar()

rfm = load_customer_segments()
scaler = load_scaler()
kmeans = load_kmeans()

segment_labels = {
    0: "Regular Customers",
    1: "At-Risk Customers",
    2: "Loyal Customers",
    3: "High-Value Customers",
    4: "Premium Customers",
}

if "Segment" not in rfm.columns:
    rfm["Segment"] = rfm["Cluster"].map(segment_labels)
elif pd.api.types.is_numeric_dtype(rfm["Segment"]):
    rfm["Segment"] = rfm["Segment"].map(segment_labels)

segment_details = {
    "Regular Customers": {
        "status": "Active",
        "priority": "Medium",
        "value": "Medium",
        "action": "Encourage repeat purchases with loyalty rewards, cross-selling, and personalized offers.",
        "insight": "Regular customers create a stable revenue base and are the easiest group to move into higher-value behavior.",
    },
    "At-Risk Customers": {
        "status": "Inactive",
        "priority": "High",
        "value": "Recoverable",
        "action": "Run win-back campaigns with limited-time discounts, reminders, and product recommendations based on past baskets.",
        "insight": "These customers have not purchased recently. A targeted recovery workflow can protect revenue that would otherwise be lost.",
    },
    "Loyal Customers": {
        "status": "Highly Active",
        "priority": "High",
        "value": "High",
        "action": "Reward loyalty with referral benefits, tiered points, and early access to new products.",
        "insight": "Loyal customers buy repeatedly and can become advocates if the brand gives them a reason to share.",
    },
    "High-Value Customers": {
        "status": "Highly Active",
        "priority": "Critical",
        "value": "Very High",
        "action": "Offer premium service, exclusive discounts, and curated recommendations.",
        "insight": "High-value customers produce a significant share of sales, so retention has direct revenue impact.",
    },
    "Premium Customers": {
        "status": "VIP",
        "priority": "Critical",
        "value": "Exceptional",
        "action": "Create VIP membership benefits, exclusive experiences, and dedicated support.",
        "insight": "Premium customers are rare but commercially powerful. They should be treated as a strategic account segment.",
    },
}

page_header(
    "Customer Segmentation",
    "Predict a customer's business segment using recency, frequency, and monetary value, then convert that prediction into a marketing action.",
    pills=["RFM Input", "K-Means Model", "Retention Strategy"],
)

with st.container():
    st.subheader("Enter Customer Profile")
    col1, col2, col3 = st.columns(3)
    with col1:
        recency = st.number_input("Recency in days", min_value=1, value=30)
    with col2:
        frequency = st.number_input("Purchase frequency", min_value=1, value=5)
    with col3:
        monetary = st.number_input("Monetary value (INR)", min_value=1.0, value=1000.0)

predict = st.button("Predict Customer Segment", use_container_width=True)

segment_avg = rfm.groupby("Segment")[["Recency", "Frequency", "Monetary"]].mean()

if predict:
    customer = pd.DataFrame(
        {"Recency": [recency], "Frequency": [frequency], "Monetary": [monetary]}
    )
    scaled_customer = scaler.transform(customer)
    cluster = int(kmeans.predict(scaled_customer)[0])
    segment = segment_labels.get(cluster, "Unknown")
    details = segment_details.get(segment)

    if details is None:
        st.error("The model returned a cluster that is not mapped to a business segment.")
        st.stop()

    st.subheader("Prediction Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Segment", segment)
    col2.metric("Status", details["status"])
    col3.metric("Priority", details["priority"])
    col4.metric("Customer Value", details["value"])

    insight("Recommended Business Action", details["action"], tone="action")
    insight("Why This Matters", details["insight"])

    if segment in segment_avg.index:
        categories = ["Recency", "Frequency", "Monetary"]
        fig = go.Figure()
        fig.add_trace(
            go.Scatterpolar(
                r=[recency, frequency, monetary],
                theta=categories,
                fill="toself",
                name="Current Customer",
            )
        )
        fig.add_trace(
            go.Scatterpolar(
                r=segment_avg.loc[segment].tolist(),
                theta=categories,
                fill="toself",
                name="Segment Average",
            )
        )
        fig.update_layout(
            title="Customer Profile vs Segment Average",
            template="plotly_dark",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
            polar=dict(radialaxis=dict(visible=True)),
        )
        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Model Details"):
        st.write(f"Predicted cluster ID: {cluster}")
        st.write("Algorithm: K-Means Clustering")
        st.dataframe(customer, use_container_width=True, hide_index=True)
        scaled_df = pd.DataFrame(scaled_customer, columns=["Recency", "Frequency", "Monetary"])
        st.dataframe(scaled_df.round(3), use_container_width=True, hide_index=True)
else:
    st.subheader("Segment Playbook")
    cols = st.columns(2)
    for index, (segment_name, details) in enumerate(segment_details.items()):
        with cols[index % 2]:
            section_card(segment_name, f"{details['insight']} Recommended action: {details['action']}")

st.subheader("Average Segment Characteristics")
display_table = segment_avg.rename(
    columns={
        "Recency": "Average Days Since Last Purchase",
        "Frequency": "Average Purchases",
        "Monetary": "Average Customer Spend (INR)",
    }
)
st.dataframe(display_table.round(2), use_container_width=True)
