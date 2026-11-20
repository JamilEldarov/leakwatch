"""Run with: streamlit run dashboard.py"""
import pandas as pd
import streamlit as st
from sqlalchemy import select

from app.collectors.demo import seed_demo
from app.collectors.pastes import scan_configured_pastes
from app.config import get_settings
from app.db import get_session, init_db
from app.models import Finding

st.set_page_config(page_title="LeakWatch", page_icon="🛡️", layout="wide")
st.title("🛡️ LeakWatch")
st.caption("Organizational Data Leak Monitoring & Early Warning — hackathon MVP")
settings = get_settings()
st.info(f"Monitored domain: **{settings.target_domain}** · Indicator match ≠ confirmed breach")

try:
    init_db()
except Exception as exc:
    st.error(f"Database unavailable. Start PostgreSQL (`docker compose up -d db`). Detail: {exc}")
    st.stop()

with st.sidebar:
    st.header("Collectors")
    if st.button("Load synthetic demo", use_container_width=True):
        st.success(f"Created {seed_demo()} new synthetic findings (duplicates skipped)")
    if st.button("Scan configured paste URLs", use_container_width=True):
        new_count, errors = scan_configured_pastes()
        st.success(f"Created {new_count} new findings")
        for error in errors:
            st.warning(error)
    st.caption("Telegram: run `python run_scan.py --telegram` in a terminal after login.")
    st.divider()
    level_filter = st.multiselect("Risk", ["HIGH", "MEDIUM", "LOW"], default=["HIGH", "MEDIUM", "LOW"])
    source_filter = st.multiselect("Sources", ["telegram", "pastebin", "rentry", "paste"], default=["telegram", "pastebin", "rentry", "paste"])

with get_session() as session:
    findings = session.scalars(select(Finding).order_by(Finding.created_at.desc(), Finding.id.desc())).all()
rows = [
    {
        "Detected UTC": f.created_at.isoformat(timespec="seconds"),
        "Source": f.source_type,
        "Source name": f.source_name,
        "Type": f.entity_type,
        "Indicator (masked)": f.entity_masked,
        "Risk": f.risk_level,
        "Score": f.risk_score,
        "Reason": f.reason,
        "URL": f.source_url,
    }
    for f in findings if f.risk_level in level_filter and f.source_type in source_filter
]
df = pd.DataFrame(rows)
a, b, c, d = st.columns(4)
a.metric("Matching indicators", len(rows))
b.metric("High risk", sum(row["Risk"] == "HIGH" for row in rows))
c.metric("Medium risk", sum(row["Risk"] == "MEDIUM" for row in rows))
d.metric("Data sources", len({row["Source"] for row in rows}))

if not df.empty:
    left, right = st.columns(2)
    with left:
        st.subheader("Risk distribution")
        st.bar_chart(df["Risk"].value_counts())
    with right:
        st.subheader("Findings by source")
        st.bar_chart(df["Source"].value_counts())
    st.subheader("Findings")
    st.dataframe(df, use_container_width=True, hide_index=True, column_config={"URL": st.column_config.LinkColumn("Source URL")})
    st.download_button(
        "Export redacted CSV", df.to_csv(index=False).encode("utf-8"),
        file_name="leakwatch-findings-redacted.csv", mime="text/csv"
    )
else:
    st.warning("No findings yet. Click **Load synthetic demo** in the sidebar.")

st.caption("All demo evidence is fictional; no exposed passwords or raw leaked content are stored.")
