import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── Setup ──────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Agati Iraq Dashboard", page_icon="🚖", layout="wide")

df = pd.read_csv("reviews.csv")
df["at"] = pd.to_datetime(df["at"], errors="coerce")
df["month"] = df["at"].dt.to_period("M").astype(str)

total     = len(df)
positive  = len(df[df["sentiment"] == "Positive"])
negative  = len(df[df["sentiment"] == "Negative"])
neutral   = len(df[df["sentiment"] == "Neutral"])
pos_pct   = round(positive / total * 100)
neg_pct   = round(negative / total * 100)
neu_pct   = round(neutral  / total * 100)
avg_score = round(df["score"].mean(), 2)
monthly   = df.groupby("month").size().reset_index(name="count")
recent_growth = monthly["count"].iloc[-1] > monthly["count"].mean() if len(monthly) > 1 else False

# ── Constants ──────────────────────────────────────────────────────────────────
BG, SURFACE, BORDER = "#0f1117", "#1a1d27", "#2a2d3a"
ACCENT, TEXT, MUTED  = "#f7a600", "#e8eaf0", "#8b8fa8"
GREEN, AMBER, RED, PURPLE = "#22c55e", "#f59e0b", "#ef4444", "#a855f7"
CHART = dict(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
             font=dict(color=TEXT, family="Segoe UI"), margin=dict(t=10,b=10,l=10,r=10))

# ── Helpers ────────────────────────────────────────────────────────────────────
def section(label):
    st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin:22px 0 14px">
        <div style="width:3px;height:18px;background:{ACCENT};border-radius:2px"></div>
        <span style="font-size:11px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em">{label}</span>
    </div>""", unsafe_allow_html=True)

def card(icon, title, body, border_color, bg=None):
    st.markdown(f"""<div style="background:{bg or BG};border:1px solid {BORDER};
        border-right:3px solid {border_color};border-radius:12px;padding:18px;height:100%">
        <div style="font-size:20px;margin-bottom:8px">{icon}</div>
        <div style="font-size:13px;font-weight:700;color:{TEXT};margin-bottom:6px">{title}</div>
        <div style="font-size:12px;color:{MUTED};line-height:1.75">{body}</div>
    </div>""", unsafe_allow_html=True)

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown(f"""<style>
body,.stApp{{background:{BG}!important;color:{TEXT};font-family:Segoe UI,Tahoma,Arial}}
[data-testid="stMetricValue"]{{font-size:2rem!important;font-weight:900!important}}
[data-testid="stMetricLabel"]{{font-size:.72rem!important;color:{MUTED}!important;text-transform:uppercase;letter-spacing:.08em}}
div[data-testid="metric-container"]{{background:{SURFACE};border:1px solid {BORDER};border-radius:14px;padding:18px 20px}}
hr{{border-color:{BORDER}!important}}
</style>""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""<div style="display:flex;align-items:center;gap:14px;background:{SURFACE};
    border:1px solid {BORDER};border-radius:14px;padding:18px 22px;margin-bottom:24px">
  <div style="background:{ACCENT};border-radius:10px;width:46px;height:46px;
      display:flex;align-items:center;justify-content:center;font-size:22px">🚖</div>
  <div>
    <div style="font-size:20px;font-weight:800">Agati Iraq</div>
    <div style="font-size:12px;color:{MUTED}">Customer Reviews — Business Intelligence Dashboard</div>
  </div>
  <div style="margin-left:auto;background:#22c55e22;border:1px solid #22c55e55;
      border-radius:20px;padding:4px 14px;font-size:12px;color:{GREEN};font-weight:600">● Live</div>
</div>""", unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
for col, (label, val) in zip(st.columns(5), [
    ("📋 Total Reviews", total), ("😊 Positive", positive),
    ("😐 Neutral", neutral),     ("😞 Negative", negative),
    ("⭐ Avg Score", avg_score)
]):
    col.metric(label, val)

# ── Business Insights ──────────────────────────────────────────────────────────
section("Business Insights")

if avg_score >= 4.5 and pos_pct >= 75:
    health, hcolor = "🟢 Strong Performance", GREEN
    summary = f"Customer sentiment is strong. {pos_pct}% positive reviews and an average rating of {avg_score}/5 indicate a consistently good service experience."
elif avg_score >= 3.8 or pos_pct >= 55:
    health, hcolor = "🟡 Moderate Performance", AMBER
    summary = f"Sentiment is acceptable but improvable. {pos_pct}% of customers are satisfied, while {neg_pct}% express dissatisfaction — indicating room for targeted improvement."
else:
    health, hcolor = "🔴 Performance at Risk", RED
    summary = f"Customer sentiment is below acceptable levels. Only {pos_pct}% positive with an average of {avg_score}/5 signals operational issues that require immediate attention."

st.markdown(f"""<div style="background:{SURFACE};border:1px solid {BORDER};border-radius:14px;padding:20px 24px">
    <div style="font-size:13px;font-weight:700;color:{hcolor};margin-bottom:8px">{health}</div>
    <div style="font-size:13px;color:{TEXT};line-height:1.8;margin-bottom:12px">{summary}</div>
    <div style="display:flex;gap:24px;flex-wrap:wrap">
        {"".join(f'<span style="font-size:12px;color:{MUTED}">{"•"} {t}</span>' for t in [
            f"Satisfaction rate: <b style='color:{TEXT}'>{pos_pct}%</b>",
            f"Negative rate: <b style='color:{RED}'>{neg_pct}%</b>",
            f"Neutral rate: <b style='color:{AMBER}'>{neu_pct}%</b>",
            f"Avg rating: <b style='color:{ACCENT}'>{avg_score}/5</b>",
            f"Total reviews: <b style='color:{TEXT}'>{total}</b>",
        ])}
    </div>
</div>""", unsafe_allow_html=True)

# ── Charts ─────────────────────────────────────────────────────────────────────
section("Analytics")
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"<div style='font-size:12px;color:{MUTED};margin-bottom:8px'>Sentiment Distribution</div>", unsafe_allow_html=True)
    fig = go.Figure(go.Pie(
        values=[positive, neutral, negative], labels=["Positive","Neutral","Negative"],
        hole=0.62, marker=dict(colors=[GREEN,AMBER,RED], line=dict(color=BG,width=2))
    ))
    fig.update_layout(**CHART, legend=dict(font=dict(color=TEXT)))
    fig.add_annotation(text=f"<b>{total}</b><br>reviews", x=0.5, y=0.5,
                       font=dict(size=16, color=TEXT), showarrow=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

with c2:
    st.markdown(f"<div style='font-size:12px;color:{MUTED};margin-bottom:8px'>Rating Distribution (1–5 ⭐)</div>", unsafe_allow_html=True)
    sc = df["score"].value_counts().sort_index()
    fig2 = go.Figure(go.Bar(
        x=[f"{'⭐'*i}" for i in sc.index], y=sc.values,
        marker=dict(color=[RED,RED,AMBER,GREEN,GREEN][:len(sc)], line=dict(width=0)),
        text=sc.values, textposition="outside", textfont=dict(color=TEXT)
    ))
    fig2.update_layout(**CHART, xaxis=dict(showgrid=False,color=TEXT),
                       yaxis=dict(showgrid=True,gridcolor=BORDER,color=MUTED))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

section("Monthly Review Trend")
fig3 = go.Figure(go.Bar(
    x=monthly["month"], y=monthly["count"],
    marker=dict(color=ACCENT, opacity=0.85, line=dict(width=0)),
    text=monthly["count"], textposition="outside", textfont=dict(color=TEXT)
))
fig3.update_layout(**CHART, xaxis=dict(showgrid=False,color=MUTED),
                   yaxis=dict(showgrid=True,gridcolor=BORDER,color=MUTED))
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

# ── Smart Recommendations ──────────────────────────────────────────────────────
section("Smart Recommendations")

def build_recs():
    recs = []

    if neg_pct >= 20:
        recs.append((RED, "🚨", "High Negative Sentiment Detected",
            f"Negative reviews have reached {neg_pct}% of total feedback. "
            f"<b>Action:</b> Analyze the most recent negative reviews to identify recurring operational issues — such as driver behavior, wait times, or payment errors — and escalate to the operations team."))
    elif neg_pct >= 10:
        recs.append((AMBER, "⚠️", "Negative Trend Requires Monitoring",
            f"Negative sentiment stands at {neg_pct}%. While not critical, this metric should be tracked weekly. "
            f"<b>Action:</b> Set up a monthly review audit to catch issues before they escalate."))
    else:
        recs.append((GREEN, "✅", "Negative Sentiment Under Control",
            f"Only {neg_pct}% negative reviews — below the 10% warning threshold. "
            f"<b>Action:</b> Maintain current service standards and continue monitoring."))

    if avg_score < 4.0:
        recs.append((RED, "⭐", "Average Rating Below Target",
            f"The average rating is {avg_score}/5, below the 4.0 benchmark expected by app store algorithms. "
            f"<b>Action:</b> Prioritize resolving the lowest-rated experiences and encourage satisfied customers to update their reviews."))
    elif avg_score < 4.5:
        recs.append((AMBER, "⭐", "Rating Close to Target — Push Higher",
            f"Average rating is {avg_score}/5. A score above 4.5 would significantly improve app store visibility. "
            f"<b>Action:</b> Identify the gap between 4-star and 5-star experiences and close it through service improvements."))
    else:
        recs.append((GREEN, "🏆", "Excellent Rating — Protect It",
            f"Average rating of {avg_score}/5 is outstanding. "
            f"<b>Action:</b> Respond publicly to all negative reviews to show management responsiveness and protect the rating."))

    if pos_pct >= 75:
        recs.append((GREEN, "📣", "Leverage Positive Reviews in Marketing",
            f"{pos_pct}% satisfaction rate is a strong asset. "
            f"<b>Action:</b> Use top positive reviews in social media campaigns, app store listings, and pitch decks to attract new users and investors."))
    else:
        recs.append((AMBER, "📈", "Grow the Positive Base",
            f"Positive reviews stand at {pos_pct}%. Industry leaders typically exceed 75%. "
            f"<b>Action:</b> Introduce post-ride prompts encouraging happy customers to leave reviews, which will shift the sentiment balance."))

    if neu_pct >= 15:
        recs.append((PURPLE, "🎯", "Convert Neutral Customers",
            f"{neutral} reviews ({neu_pct}%) are neutral — customers who are not dissatisfied but not loyal either. "
            f"<b>Action:</b> Launch targeted loyalty rewards or in-app surveys to understand what would turn these users into repeat customers."))
    elif recent_growth:
        recs.append((PURPLE, "📊", "Review Volume Is Growing",
            f"Recent review activity is above the monthly average. "
            f"<b>Action:</b> Monitor operational capacity closely. Increased demand without matched capacity often leads to a drop in service quality."))
    else:
        recs.append((PURPLE, "🔍", "Collect More Feedback",
            f"Review volume could be higher for more reliable insights. "
            f"<b>Action:</b> Add in-app prompts after ride completion to increase review submission rates and improve data quality."))

    return recs[:4]

cols = st.columns(4)
for col, (color, icon, title, body) in zip(cols, build_recs()):
    with col:
        card(icon, title, body, color)

# ── Review Explorer ────────────────────────────────────────────────────────────
section("Review Explorer")
st.markdown(f"<div style='font-size:12px;color:{MUTED};margin-bottom:14px'>Use this section to investigate individual customer reviews, validate the insights above, and identify specific complaints or praise patterns.</div>", unsafe_allow_html=True)

f1, f2 = st.columns([1, 3])
with f1:
    sent_filter = st.selectbox("Sentiment", ["All","Positive","Neutral","Negative"], label_visibility="collapsed")
with f2:
    search = st.text_input("Search", placeholder="🔍 Search reviews...", label_visibility="collapsed")

filtered = df.copy()
if sent_filter != "All":
    filtered = filtered[filtered["sentiment"] == sent_filter]
if search:
    filtered = filtered[filtered["content"].str.contains(search, na=False, case=False)]

display = filtered[["content","score","at","sentiment"]].rename(
    columns={"content":"Review","score":"Score","at":"Date","sentiment":"Sentiment"})

st.dataframe(display, use_container_width=True, hide_index=True)

d1, d2 = st.columns([1, 5])
with d1:
    st.download_button("⬇️ Download CSV", display.to_csv(index=False).encode("utf-8-sig"),
                       "filtered_reviews.csv", "text/csv")
with d2:
    st.caption(f"Showing {len(filtered)} of {total} reviews")
