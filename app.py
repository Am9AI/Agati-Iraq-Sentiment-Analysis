import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# ── Load Data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("reviews.csv")
df["at"] = pd.to_datetime(df["at"], errors="coerce")
df["month"] = df["at"].dt.to_period("M").astype(str)

# ── Stats ──────────────────────────────────────────────────────────────────────
total    = len(df)
positive = len(df[df["sentiment"] == "Positive"])
negative = len(df[df["sentiment"] == "Negative"])
neutral  = len(df[df["sentiment"] == "Neutral"])
pos_pct  = round((positive / total) * 100) if total else 0
neg_pct  = round((negative / total) * 100) if total else 0
avg_score = round(df["score"].mean(), 1)

# ── Top Keywords ───────────────────────────────────────────────────────────────
all_text = " ".join(df["content"].astype(str).tolist()).lower()
words = re.findall(r'\b\w{3,}\b', all_text)
stopwords = {"من","في","على","إلى","عن","مع","هذا","هذه","التي","الذي","وهو","كان","قال","لكن","أيضا","حتى","بعد","قبل","كل","يمكن","لان","لأن","انا","ماكو","اكو","بس","هو","هي","الي","مال","ولا","ما","مو","وين","شو","ليش"}
word_freq = Counter(w for w in words if w not in stopwords)
top_words = word_freq.most_common(8)
wlabels, wvalues = zip(*top_words) if top_words else ([], [])

# ── Monthly ────────────────────────────────────────────────────────────────────
monthly = df.groupby("month").size().reset_index(name="count")

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Agati Iraq Dashboard", page_icon="🚖", layout="wide")

st.markdown("""
<style>
body, .stApp { background:#0f1117 !important; color:#e8eaf0; font-family: Segoe UI, Tahoma, Arial; }
[data-testid="stMetricValue"] { font-size:2.2rem !important; font-weight:900 !important; }
[data-testid="stMetricLabel"] { font-size:0.75rem !important; color:#8b8fa8 !important; text-transform:uppercase; letter-spacing:0.08em; }
div[data-testid="metric-container"] {
    background:#1a1d27; border:1px solid #2a2d3a;
    border-radius:14px; padding:18px 20px;
}
.section-title {
    display:flex; align-items:center; gap:10px;
    font-size:11px; font-weight:700; color:#8b8fa8;
    text-transform:uppercase; letter-spacing:0.1em;
    margin-bottom:12px; margin-top:4px;
}
.section-title::before {
    content:''; display:inline-block;
    width:3px; height:16px; background:#f7a600; border-radius:2px;
}
.rec-card {
    background:#1a1d27; border:1px solid #2a2d3a;
    border-radius:12px; padding:16px 18px;
    margin-bottom:10px;
}
.stDataFrame { background:#1a1d27 !important; }
hr { border-color:#2a2d3a !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;background:#1a1d27;
            border:1px solid #2a2d3a;border-radius:14px;padding:18px 22px;margin-bottom:24px">
  <div style="background:#f7a600;border-radius:10px;width:46px;height:46px;
              display:flex;align-items:center;justify-content:center;font-size:22px">🚖</div>
  <div>
    <div style="font-size:20px;font-weight:800;color:#e8eaf0">Agati Iraq</div>
    <div style="font-size:12px;color:#8b8fa8">Customer Reviews Dashboard</div>
  </div>
  <div style="margin-left:auto;background:#22c55e22;border:1px solid #22c55e55;
              border-radius:20px;padding:4px 14px;font-size:12px;color:#22c55e;font-weight:600">
    ● Live
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📋 Total Reviews", total)
c2.metric("😊 Positive",      positive)
c3.metric("😐 Neutral",       neutral)
c4.metric("😞 Negative",      negative)
c5.metric("⭐ Avg Score",     avg_score)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

CHART = dict(paper_bgcolor="#1a1d27", plot_bgcolor="#1a1d27",
             font=dict(color="#e8eaf0", family="Segoe UI"),
             margin=dict(t=10, b=10, l=10, r=10))

with col1:
    st.markdown('<div class="section-title">Sentiment Distribution</div>', unsafe_allow_html=True)
    fig_pie = go.Figure(go.Pie(
        values=[positive, neutral, negative],
        labels=["Positive", "Neutral", "Negative"],
        hole=0.55,
        marker=dict(colors=["#22c55e","#f59e0b","#ef4444"], line=dict(color="#0f1117", width=2)),
    ))
    fig_pie.update_layout(**CHART, legend=dict(font=dict(color="#e8eaf0")))
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown('<div class="section-title">Top Keywords</div>', unsafe_allow_html=True)
    fig_words = go.Figure(go.Bar(
        x=list(wvalues), y=list(wlabels), orientation="h",
        marker=dict(color="#f7a600", line=dict(width=0)),
    ))
    fig_words.update_layout(**CHART,
        xaxis=dict(showgrid=True, gridcolor="#2a2d3a", color="#8b8fa8"),
        yaxis=dict(showgrid=False, color="#e8eaf0"))
    st.plotly_chart(fig_words, use_container_width=True, config={"displayModeBar": False})

# ── Monthly Trend ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Monthly Review Trend</div>', unsafe_allow_html=True)
fig_monthly = go.Figure(go.Bar(
    x=monthly["month"], y=monthly["count"],
    marker=dict(color="#f7a600", opacity=0.85, line=dict(width=0)),
))
fig_monthly.update_layout(**CHART,
    xaxis=dict(showgrid=False, color="#8b8fa8"),
    yaxis=dict(showgrid=True, gridcolor="#2a2d3a", color="#8b8fa8"))
st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})

# ── Score Distribution ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Score Distribution (1-5 ⭐)</div>', unsafe_allow_html=True)
score_counts = df["score"].value_counts().sort_index()
fig_score = go.Figure(go.Bar(
    x=[f"{'⭐'*i}" for i in score_counts.index],
    y=score_counts.values,
    marker=dict(color=["#ef4444","#f59e0b","#f59e0b","#22c55e","#22c55e"], line=dict(width=0)),
))
fig_score.update_layout(**CHART,
    xaxis=dict(showgrid=False, color="#e8eaf0"),
    yaxis=dict(showgrid=True, gridcolor="#2a2d3a", color="#8b8fa8"))
st.plotly_chart(fig_score, use_container_width=True, config={"displayModeBar": False})

# ── Recommendations ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Smart Recommendations</div>', unsafe_allow_html=True)
r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown(f"""<div class="rec-card" style="border-right:3px solid #ef4444">
        <div style="font-size:20px;margin-bottom:8px">🚨</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:4px">Reduce Negatives</div>
        <div style="font-size:12px;color:#8b8fa8;line-height:1.6">{neg_pct}% negative reviews — focus on response time and driver tracking.</div>
    </div>""", unsafe_allow_html=True)

with r2:
    st.markdown(f"""<div class="rec-card" style="border-right:3px solid #22c55e">
        <div style="font-size:20px;margin-bottom:8px">✅</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:4px">Keep Strengths</div>
        <div style="font-size:12px;color:#8b8fa8;line-height:1.6">{pos_pct}% positive — customers love the service. Maintain driver quality.</div>
    </div>""", unsafe_allow_html=True)

with r3:
    st.markdown(f"""<div class="rec-card" style="border-right:3px solid #f59e0b">
        <div style="font-size:20px;margin-bottom:8px">📊</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:4px">Convert Neutrals</div>
        <div style="font-size:12px;color:#8b8fa8;line-height:1.6">{neutral} neutral reviews — offer discounts or loyalty points to convert them.</div>
    </div>""", unsafe_allow_html=True)

with r4:
    st.markdown(f"""<div class="rec-card" style="border-right:3px solid #a855f7">
        <div style="font-size:20px;margin-bottom:8px">📱</div>
        <div style="font-size:13px;font-weight:700;color:#e8eaf0;margin-bottom:4px">App Experience</div>
        <div style="font-size:12px;color:#8b8fa8;line-height:1.6">Avg score {avg_score}/5 — review payment and navigation issues in the app.</div>
    </div>""", unsafe_allow_html=True)

# ── Reviews Table ──────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">All Reviews</div>', unsafe_allow_html=True)

filter_col, search_col = st.columns([1, 3])
with filter_col:
    sentiment_filter = st.selectbox("Filter by Sentiment", ["All", "Positive", "Neutral", "Negative"], label_visibility="collapsed")
with search_col:
    search_text = st.text_input("Search", placeholder="🔍 Search reviews...", label_visibility="collapsed")

filtered = df.copy()
if sentiment_filter != "All":
    filtered = filtered[filtered["sentiment"] == sentiment_filter]
if search_text:
    filtered = filtered[filtered["content"].str.contains(search_text, na=False)]

st.dataframe(
    filtered[["content", "score", "at", "sentiment"]].rename(columns={
        "content": "Review", "score": "Score", "at": "Date", "sentiment": "Sentiment"
    }),
    use_container_width=True,
    hide_index=True,
)
st.caption(f"Showing {len(filtered)} of {total} reviews")
