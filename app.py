import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

df = pd.read_csv("reviews.csv")

total = len(df)
positive = len(df[df["sentiment"] == "Positive"])
negative = len(df[df["sentiment"] == "Negative"])
neutral = len(df[df["sentiment"] == "Neutral"])
pos_pct = round((positive / total) * 100) if total else 0
neg_pct = round((negative / total) * 100) if total else 0

all_text = " ".join(df["review"].astype(str).tolist()).lower()
words = re.findall(r'\b\w{3,}\b', all_text)
stopwords = {"the","and","for","with","this","that","was","are","have","from","they","been","its","also","but","not","can","our","more","very","will","had"}
word_freq = Counter(w for w in words if w not in stopwords)
top_words = word_freq.most_common(8)
wlabels, wvalues = zip(*top_words) if top_words else ([], [])

if "date" in df.columns:
    df["month"] = pd.to_datetime(df["date"], errors="coerce").dt.to_period("M").astype(str)
    monthly = df.groupby("month").size().reset_index(name="count")
else:
    monthly = pd.DataFrame({"month": [], "count": []})

BG = "#0f1117"
SURFACE = "#1a1d27"
BORDER = "#2a2d3a"
ACCENT = "#f7a600"
TEXT = "#e8eaf0"
MUTED = "#8b8fa8"
GREEN = "#22c55e"
AMBER = "#f59e0b"
RED = "#ef4444"
PURPLE = "#a855f7"

CHART = dict(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
             font=dict(color=TEXT, family="Segoe UI"), margin=dict(t=10,b=10,l=10,r=10))

fig_pie = px.pie(values=[positive,neutral,negative],
                 names=["Positive","Neutral","Negative"],
                 color_discrete_sequence=[GREEN,AMBER,RED], hole=0.55)
fig_pie.update_traces(marker=dict(line=dict(color=BG, width=2)))
fig_pie.update_layout(**CHART, legend=dict(font=dict(color=TEXT)))

fig_words = go.Figure(go.Bar(x=list(wvalues), y=list(wlabels), orientation="h",
                              marker=dict(color=ACCENT, line=dict(width=0))))
fig_words.update_layout(**CHART,
    xaxis=dict(showgrid=True, gridcolor=BORDER, color=MUTED),
    yaxis=dict(showgrid=False, color=TEXT))

fig_monthly = go.Figure(go.Bar(x=monthly["month"], y=monthly["count"],
                                marker=dict(color=ACCENT, opacity=0.85, line=dict(width=0))))
fig_monthly.update_layout(**CHART,
    xaxis=dict(showgrid=False, color=MUTED),
    yaxis=dict(showgrid=True, gridcolor=BORDER, color=MUTED))

def kpi(icon, value, label, color=TEXT):
    return html.Div([
        html.Div(icon, style={"fontSize":"24px","marginBottom":"8px"}),
        html.Div(str(value), style={"fontSize":"34px","fontWeight":"900","color":color,"letterSpacing":"-1px"}),
        html.Div(label, style={"fontSize":"11px","color":MUTED,"fontWeight":"600","textTransform":"uppercase","letterSpacing":"0.08em","marginTop":"4px"}),
    ], style={"background":SURFACE,"border":f"1px solid {BORDER}","borderRadius":"14px","padding":"22px 20px","flex":"1","minWidth":"150px"})

def rec(icon, title, text, color):
    return html.Div([
        html.Div(icon, style={"fontSize":"20px","marginBottom":"8px"}),
        html.Div(title, style={"fontSize":"13px","fontWeight":"700","color":TEXT,"marginBottom":"4px"}),
        html.Div(text, style={"fontSize":"12px","color":MUTED,"lineHeight":"1.6"}),
    ], style={"background":BG,"border":f"1px solid {BORDER}","borderRight":f"3px solid {color}",
              "borderRadius":"12px","padding":"16px 18px","flex":"1","minWidth":"200px"})

def title(text):
    return html.Div([
        html.Div(style={"width":"3px","height":"18px","background":ACCENT,"borderRadius":"2px"}),
        html.Span(text, style={"fontSize":"12px","fontWeight":"700","color":MUTED,"textTransform":"uppercase","letterSpacing":"0.1em"}),
    ], style={"display":"flex","alignItems":"center","gap":"10px","marginBottom":"16px"})

app = dash.Dash(__name__, title="Agati Iraq Dashboard")

app.layout = html.Div(style={"background":BG,"minHeight":"100vh","fontFamily":"Segoe UI, Tahoma, Arial"}, children=[

    html.Div([
        html.Div("🚖", style={"fontSize":"22px","background":ACCENT,"borderRadius":"10px",
                               "width":"44px","height":"44px","display":"flex","alignItems":"center","justifyContent":"center"}),
        html.Div([
            html.Div("Agati Iraq", style={"fontSize":"20px","fontWeight":"800","color":TEXT}),
            html.Div("Customer Reviews Dashboard", style={"fontSize":"12px","color":MUTED}),
        ]),
        html.Div("● Live", style={"marginLeft":"auto","background":"#22c55e22","border":"1px solid #22c55e55",
                                   "borderRadius":"20px","padding":"4px 14px","fontSize":"12px","color":GREEN,"fontWeight":"600"}),
    ], style={"background":SURFACE,"borderBottom":f"1px solid {BORDER}","padding":"18px 32px",
              "display":"flex","alignItems":"center","gap":"14px"}),

    html.Div(style={"maxWidth":"1200px","margin":"0 auto","padding":"28px 24px"}, children=[

        html.Div([
            kpi("📋", total,        "Total Reviews"),
            kpi("😊", positive,     "Positive",    GREEN),
            kpi("😐", neutral,      "Neutral",     AMBER),
            kpi("😞", negative,     "Negative",    RED),
            kpi("📈", f"{pos_pct}%","Satisfaction",ACCENT),
        ], style={"display":"flex","gap":"16px","flexWrap":"wrap","marginBottom":"24px"}),

        html.Div([
            html.Div([title("Sentiment Distribution"),
                      dcc.Graph(figure=fig_pie, config={"displayModeBar":False}, style={"height":"260px"})],
                     style={"background":SURFACE,"border":f"1px solid {BORDER}","borderRadius":"14px","padding":"24px","flex":"1"}),
            html.Div([title("Top Keywords"),
                      dcc.Graph(figure=fig_words, config={"displayModeBar":False}, style={"height":"260px"})],
                     style={"background":SURFACE,"border":f"1px solid {BORDER}","borderRadius":"14px","padding":"24px","flex":"1"}),
        ], style={"display":"flex","gap":"20px","marginBottom":"20px","flexWrap":"wrap"}),

        html.Div([title("Monthly Trend"),
                  dcc.Graph(figure=fig_monthly, config={"displayModeBar":False}, style={"height":"180px"})],
                 style={"background":SURFACE,"border":f"1px solid {BORDER}","borderRadius":"14px","padding":"24px","marginBottom":"20px"}),

        html.Div([title("Smart Recommendations"),
            html.Div([
                rec("🚨","Reduce Wait Time",      f"{neg_pct}% negative reviews — improve driver response and live tracking.", RED),
                rec("✅","Driver Quality",         "Positive reviews highlight polite drivers and clean cars. Keep it up.",     GREEN),
                rec("📊","Convert Neutral Users", f"{neutral} neutral reviews — offer discounts to build loyalty.",            AMBER),
                rec("📱","App Experience",         "Check payment and navigation issues — tech bugs hurt satisfaction.",        PURPLE),
            ], style={"display":"flex","gap":"14px","flexWrap":"wrap"}),
        ], style={"background":SURFACE,"border":f"1px solid {BORDER}","borderRadius":"14px","padding":"24px","marginBottom":"20px"}),

        html.Div([title("All Reviews"),
            html.Div(df[["review","sentiment"]].to_html(index=False, classes="tbl", border=0), dangerously_allow_html=True),
        ], style={"background":SURFACE,"border":f"1px solid {BORDER}","borderRadius":"14px","padding":"24px"}),
    ]),

    html.Style(f"""
        .tbl{{width:100%;border-collapse:collapse;font-size:13px;color:{TEXT};font-family:Segoe UI}}
        .tbl th{{padding:10px 12px;color:{MUTED};font-weight:600;border-bottom:1px solid {BORDER};text-align:left}}
        .tbl td{{padding:10px 12px;border-bottom:1px solid #2a2d3a33}}
        .tbl tr:hover td{{background:#ffffff06}}
    """),
])

if __name__ == "__main__":
    app.run(debug=True)
