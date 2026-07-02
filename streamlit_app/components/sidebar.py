import streamlit as st


def render_sidebar():
    st.sidebar.title("Shopper Spectrum")
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Customer intelligence, segmentation, and product recommendations for retail decision makers."
    )
    st.sidebar.markdown("---")
    st.sidebar.success("Built with Python, Streamlit, Plotly, and machine learning.")
    st.sidebar.markdown("---")
    st.sidebar.caption("Portfolio-ready retail analytics project")
