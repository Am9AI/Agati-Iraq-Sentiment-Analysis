# 🚖 Agati Iraq — Sentiment Analysis Dashboard

A Business Intelligence dashboard built to analyze customer reviews for Agati Iraq, one of Iraq's leading ride-hailing apps.

## Features
- KPI cards: total reviews, positive, neutral, negative, avg score
- Sentiment distribution donut chart
- Monthly review trend
- Rating distribution (1–5)
- Auto-generated business insights
- Dynamic smart recommendations based on real metrics
- Review explorer with search, filter, and CSV export

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly

## Run Locally
pip install -r requirements.txt
streamlit run app.py

## Dataset
143 real customer reviews with columns: content, score, at, sentiment
