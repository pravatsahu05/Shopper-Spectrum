# Shopper Spectrum

Shopper Spectrum is an end-to-end retail analytics and machine learning application built with Streamlit. It analyzes e-commerce transaction data, segments customers with RFM and K-Means clustering, and recommends related products using item-based collaborative filtering.

## Highlights

- Interactive business dashboard for revenue, products, countries, seasonality, and customer segments.
- Customer segmentation tool that converts RFM values into business-friendly customer labels.
- Product recommendation engine for cross-sell, bundles, and merchandising decisions.
- Executive insights page with risks, opportunities, and strategic recommendations.
- Deployment-focused project structure with cleaned dependencies and Streamlit theme config.

## Project Structure

```text
Shopper_Spectrum/
  data/
    cleaned/
    processed/
    raw/
  models/
  notebooks/
  reports/
  streamlit_app/
    app.py
    assets/
    components/
    pages/
  requirements.txt
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

## Business Use Cases

- Identify premium, loyal, regular, and at-risk customers.
- Plan customer retention and win-back campaigns.
- Improve product bundling and cross-selling.
- Track market concentration and seasonal revenue patterns.
- Present machine learning results in a business-readable dashboard.

## Author

Pravat Sahu
