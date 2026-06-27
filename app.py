import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
import re

# ── Config ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Agati Iraq Dashboard", page_icon="🚖", layout="wide")

# ── Load Data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("reviews.csv")
df["at"] = pd.to_datetime(df["at"], errors="coerce")
df["month"] = df["at"].dt.to_period("M").astype(str)

# ── Stats ──────────────────────────────────────────────────────────────────────
total     = len(df)
positive  = len(df[df["sentiment"] == "Positive"])
negative  = len(df[df["sentiment"] == "Negative"])
neutral   = len(df[df["sentiment"] == "Neutral"])
pos_pct   = round((positive / total) * 100) if total else 0
neg_pct   = round((negative / total) * 100) if total else 0
neu_pct   = round((neutral  / total) * 100) if total else 0
avg_score = round(df["score"].mean(), 2)

# ── Palette & Chart Defaults ───────────────────────────────────────────────────
BG      = "#0f1117"
SURFACE = "#1a1d27"
BORDER  = "#2a2d3a"
ACCENT  = "#f7a600"
TEXT    = "#e8eaf0"
MUTED   = "#8b8fa8"
GREEN   = "#22c55e"
AMBER   = "#f59e0b"
RED     = "#ef4444"
PURPLE  = "#a855f7"

CHART = dict(
    paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
    font=dict(color=TEXT, family="Segoe UI"),
    margin=dict(t=10, b=10, l=10, r=10)
)

# ── Helpers ────────────────────────────────────────────────────────────────────
def section(label):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:20px 0 12px">
        <div style="width:3px;height:18px;background:{ACCENT};border-radius:2px"></div>
        <span style="font-size:11px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em">{label}</span>
    </div>""", unsafe_allow_html=True)

def insight_card(icon, value, label, color=TEXT):
    st.markdown(f"""
    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:14px;padding:22px 20px">
        <div style="font-size:22px;margin-bottom:8px">{icon}</div>
        <div style="font-size:32px;font-weight:900;color:{color};letter-spacing:-1px">{value}</div>
        <div style="font-size:11px;color:{MUTED};font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-top:4px">{label}</div>
    </div>""", unsafe_allow_html=True)

def rec_card(icon, title, body, color):
    st.markdown(f"""
    <div style="background:{BG};border:1px solid {BORDER};border-right:3px solid {color};
                border-radius:12px;padding:16px 18px;height:100%">
        <div style="font-size:18px;margin-bottom:6px">{icon}</div>
        <div style="font-size:13px;font-weight:700;color:{TEXT};margin-bottom:4px">{title}</div>
        <div style="font-size:12px;color:{MUTED};line-height:1.7">{body}</div>
    </div>""", unsafe_allow_html=True)

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
body, .stApp {{ background:{BG} !important; color:{TEXT}; font-family:Segoe UI,Tahoma,Arial; }}
[data-testid="stMetricValue"] {{ font-size:2rem !important; font-weight:900 !important; }}
[data-testid="stMetricLabel"] {{ font-size:0.72rem !important; color:{MUTED} !important; text-transform:uppercase; letter-spacing:0.08em; }}
div[data-testid="metric-container"] {{ background:{SURFACE}; border:1px solid {BORDER}; border-radius:14px; padding:18px 20px; }}
hr {{ border-color:{BORDER} !important; }}
.stDataFrame {{ background:{SURFACE} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;background:{SURFACE};
            border:1px solid {BORDER};border-radius:14px;padding:18px 22px;margin-bottom:24px">
  <div style="background:{ACCENT};border-radius:10px;width:46px;height:46px;
              display:flex;align-items:center;justify-content:center;font-size:22px">🚖</div>
  <div>
    <div style="font-size:20px;font-weight:800;color:{TEXT}">Agati Iraq</div>
    <div style="font-size:12px;color:{MUTED}">Customer Reviews — Business Intelligence Dashboard</div>
  </div>
  <div style="margin-left:auto;background:#22c55e22;border:1px solid #22c55e55;
              border-radius:20px;padding:4px 14px;font-size:12px;color:{GREEN};font-weight:600">● Live</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📋 Total Reviews", total)
k2.metric("😊 Positive",      positive)
k3.metric("😐 Neutral",       neutral)
k4.metric("😞 Negative",      negative)
k5.metric("⭐ Avg Score",     avg_score)

# ── Key Insights ───────────────────────────────────────────────────────────────
section("Key Insights")

i1, i2, i3, i4 = st.columns(4)
with i1: insight_card("😊", f"{pos_pct}%", "Positive Rate", GREEN)
with i2: insight_card("😞", f"{neg_pct}%", "Negative Rate", RED)
with i3: insight_card("⭐", f"{avg_score}/5", "Avg Rating", ACCENT)
with i4: insight_card("📋", total, "Total Reviews", TEXT)

# Auto-generated summary
if avg_score >= 4.5 and pos_pct >= 70:
    health = "🟢 **Strong**"
    summary = f"Customer sentiment is strong. With {pos_pct}% positive reviews and an average rating of {avg_score}/5, Agati Iraq is delivering a consistently good experience. Focus on maintaining service quality and scaling growth."
elif avg_score >= 3.5 or pos_pct >= 50:
    health = "🟡 **Moderate**"
    summary = f"Sentiment is moderate. {pos_pct}% of customers are satisfied, but {neg_pct}% express dissatisfaction. Investigate recurring complaints and address them before they impact retention."
else:
    health = "🔴 **At Risk**"
    summary = f"Customer sentiment is concerning. Only {pos_pct}% positive reviews with an average of {avg_score}/5 signals urgent need for service improvement. Prioritize resolving the most common negative feedback themes."

st.markdown(f"""
<div style="background:{SURFACE};border:1px solid {BORDER};border-radius:14px;padding:20px 24px;margin-top:12px">
    <div style="font-size:13px;color:{MUTED};margin-bottom:6px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em">Business Health</div>
    <div style="font-size:15px;color:{TEXT};line-height:1.8">{health} — {summary}</div>
</div>
""", unsafe_allow_html=True)

# ── Charts ─────────────────────────────────────────────────────────────────────
section("Analytics")
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"<div style='font-size:12px;color:{MUTED};margin-bottom:8px'>Sentiment Distribution</div>", unsafe_allow_html=True)
    fig_pie = go.Figure(go.Pie(
        values=[positive, neutral, negative],
        labels=["Positive", "Neutral", "Negative"],
        hole=0.62,
        marker=dict(colors=[GREEN, AMBER, RED], line=dict(color=BG, width=2)),
        textfont=dict(color=TEXT),
    ))
    fig_pie.update_layout(**CHART, legend=dict(font=dict(color=TEXT)))
    fig_pie.add_annotation(text=f"<b>{total}</b><br><span style='font-size:11px'>reviews</span>",
                           x=0.5, y=0.5, font=dict(size=18, color=TEXT), showarrow=False)
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

with c2:
    st.markdown(f"<div style='font-size:12px;color:{MUTED};margin-bottom:8px'>Rating Distribution (1–5 ⭐)</div>", unsafe_allow_html=True)
    score_counts = df["score"].value_counts().sort_index()
    score_colors = {1: RED, 2: RED, 3: AMBER, 4: GREEN, 5: GREEN}
    fig_score = go.Figure(go.Bar(
        x=[f"{'⭐'*i}" for i in score_counts.index],
        y=score_counts.values,
        marker=dict(color=[score_colors.get(i, ACCENT) for i in score_counts.index], line=dict(width=0)),
        text=score_counts.values, textposition="outside", textfont=dict(color=TEXT),
    ))
    fig_score.update_layout(**CHART,
        xaxis=dict(showgrid=False, color=TEXT),
        yaxis=dict(showgrid=True, gridcolor=BORDER, color=MUTED))
    st.plotly_chart(fig_score, use_container_width=True, config={"displayModeBar": False})

section("Monthly Review Trend")
monthly = df.groupby("month").size().reset_index(name="count")
fig_monthly = go.Figure(go.Bar(
    x=monthly["month"], y=monthly["count"],
    marker=dict(color=ACCENT, opacity=0.85, line=dict(width=0)),
    text=monthly["count"], textposition="outside", textfont=dict(color=TEXT),
))
fig_monthly.update_layout(**CHART,
    xaxis=dict(showgrid=False, color=MUTED),
    yaxis=dict(showgrid=True, gridcolor=BORDER, color=MUTED))
st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})

# ── Dynamic Recommendations ────────────────────────────────────────────────────
section("Smart Recommendations")

recs = []

if neg_pct >= 20:
    recs.append((RED, "🚨", "Address Negative Feedback Urgently",
                 f"{neg_pct}% of reviews are negative. Identify the most common complaints and create a dedicated task force to resolve them within 30 days."))
elif neg_pct >= 10:
    recs.append((AMBER, "⚠️", "Monitor Negative Trends",
                 f"{neg_pct}% negative reviews is manageable but needs attention. Set up weekly review analysis to catch issues early."))

if pos_pct >= 75:
    recs.append((GREEN, "✅", "Leverage Positive Sentiment",
                 f"{pos_pct}% satisfaction rate is excellent. Use positive reviews in marketing campaigns and app store highlights to attract new users."))
else:
    recs.append((GREEN, "📈", "Build on Positives",
                 f"With {pos_pct}% positive reviews, identify what customers love most and double down on those service aspects."))

if neu_pct >= 15:
    recs.append((AMBER, "🎯", "Convert Neutral Users",
                 f"{neutral} neutral reviews ({neu_pct}%) represent untapped loyalty. Launch targeted offers or loyalty rewards to convert them into brand advocates."))

if avg_score < 4.0:
    recs.append((PURPLE, "⭐", "Improve Overall Rating",
                 f"Average score of {avg_score}/5 is below the 4.0 threshold most users use to judge app quality. Focus on resolving the lowest-rated experiences first."))
elif avg_score >= 4.5:
    recs.append((PURPLE, "🏆", "Maintain High Rating",
                 f"Outstanding average of {avg_score}/5. Protect this score by responding to all negative reviews publicly and showing customers you listen."))

cols = st.columns(len(recs))
for col, (color, icon, title, body) in zip(cols, recs):
    with col:
        rec_card(icon, title, body, color)

# ── Review Explorer ────────────────────────────────────────────────────────────
section("Review Explorer")
st.markdown(f"<div style='font-size:12px;color:{MUTED};margin-bottom:14px'>Browse, filter, and search individual customer reviews. Use this to identify recurring themes, spot specific complaints, or validate recommendations above.</div>", unsafe_allow_html=True)

f1, f2 = st.columns([1, 3])
with f1:
    sentiment_filter = st.selectbox("Sentiment", ["All", "Positive", "Neutral", "Negative"], label_visibility="collapsed")
with f2:
    search_text = st.text_input("Search", placeholder="🔍 Search reviews...", label_visibility="collapsed")

filtered = df.copy()
if sentiment_filter != "All":
    filtered = filtered[filtered["sentiment"] == sentiment_filter]
if search_text:
    filtered = filtered[filtered["content"].str.contains(search_text, na=False, case=False)]

display = filtered[["content", "score", "at", "sentiment"]].rename(columns={
    "content": "Review", "score": "Score", "at": "Date", "sentiment": "Sentiment"
})

st.dataframe(display, use_container_width=True, hide_index=True)

dl1, dl2 = st.columns([1, 5])
with dl1:
    st.download_button(
        label="⬇️ Download CSV",
        data=display.to_csv(index=False).encode("utf-8-sig"),
        file_name="filtered_reviews.csv",
        mime="text/csv",
    )
with dl2:
    st.caption(f"Showing {len(filtered)} of {total} reviews")
