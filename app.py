import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Agati Iraq Dashboard",
    page_icon="🚖",
    layout="wide"
)

# Load Data
df = pd.read_csv("reviews.csv")

# Title
st.title("🚖 Agati Iraq Analytics Dashboard")
st.markdown("### Customer Reviews & Business Insights")

# KPIs
total_reviews = len(df)
positive = len(df[df["sentiment"] == "Positive"])
negative = len(df[df["sentiment"] == "Negative"])
neutral = len(df[df["sentiment"] == "Neutral"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("📄 Total Reviews", total_reviews)
col2.metric("😊 Positive", positive)
col3.metric("😐 Neutral", neutral)
col4.metric("😞 Negative", negative)

st.divider()

# Sentiment Chart
sentiment_counts = df["sentiment"].value_counts()

fig = px.pie(
    values=sentiment_counts.values,
    names=sentiment_counts.index,
    title="Sentiment Distribution"
)

st.plotly_chart(fig, use_container_width=True)
