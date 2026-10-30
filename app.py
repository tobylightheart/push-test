import streamlit as st
import plotly.express as px
from load import load
from gemma import ask

st.set_page_config(page_title="Reservoir Watch", layout="wide")
st.title("Reservoir Watch")
st.caption("How full are Adelaide's reservoirs, and what does that mean? Ask in plain English.")

df = st.cache_data(load)()
latest = df[df.date == df.date.max()]
res = st.selectbox("Reservoir", sorted(df.reservoir.unique()))
one = df[df.reservoir == res]

c1, c2 = st.columns([2, 1])
with c1:
    st.plotly_chart(px.line(one, x="date", y="pct_full", title=f"{res}: % full",
                            labels={"pct_full": "% full", "date": ""}), width="stretch")
with c2:
    now = one.iloc[-1]
    yr = one[one.date <= now.date - __import__("pandas").Timedelta(days=330)].tail(1)
    st.metric("Now", f"{now.pct_full:.0f}% full", None if yr.empty else f"{now.pct_full - yr.pct_full.iloc[0]:+.0f} pts vs a year ago")
    st.metric("Network total", f"{100 * latest.volume_ml.sum() / latest.capacity_ml.sum():.0f}% full")

def facts():
    s = one.set_index("date").pct_full.resample("QE").last().dropna().round(0)
    return (f"Reservoir: {res}. Capacity {now.capacity_ml:,.0f} ML. Latest reading {now.date:%d %b %Y}: "
            f"{now.volume_ml:,.0f} ML ({now.pct_full:.0f}% full). Quarterly % full history: "
            + ", ".join(f"{d:%b %Y} {v:.0f}%" for d, v in s.items())
            + ". Same month in earlier years: "
            + ", ".join(f"{r.date:%b %Y} {r.pct_full:.0f}%" for r in one[one.date.dt.month == now.date.month].itertuples())
            + f". Whole network at {latest.date.max():%d %b %Y}: {100 * latest.volume_ml.sum() / latest.capacity_ml.sum():.0f}% full.")

q = st.text_input("Ask about this reservoir", "Is this level unusual for this time of year?")
if st.button("Ask Gemma", type="primary"):
    prompt = ("You explain South Australian reservoir data to residents. Use ONLY the facts below. "
              "Answer in 2-3 plain sentences. If the facts can't answer it, say so. No advice about water use.\n\n"
              f"FACTS: {facts()}\n\nQUESTION: {q}")
    with st.spinner("Gemma is reading the numbers…"):
        try:
            text, backend, secs = ask(prompt)
            st.success(text)
            st.caption(f"{backend} · {secs:.1f}s")
        except RuntimeError as e:
            st.error("Gemma is unavailable right now. Try again in a moment.")
            st.caption(str(e)[:200])

st.caption("Source: SA Water, Government of South Australia, licensed under CC BY 4.0 (data.sa.gov.au).")
