import streamlit as st
import pandas as pd
from utils.db import init_db, get_leaderboard, get_breakdown
from utils.ui import apply_page_config, inject_css, render_sidebar_logo, page_header
from utils.data import EVENT_NAME

apply_page_config(f"Leaderboard · {EVENT_NAME}")
inject_css()
init_db()
render_sidebar_logo()

page_header("Live Standings", "Leaderboard", "Updates the moment a score is entered in Admin.")

auto = st.toggle("Auto-refresh every 15s", value=False)

board = get_leaderboard()

if board.empty:
    st.info("No teams registered yet — check back once registrations open.")
else:
    top3 = board.head(3)
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    for i, (_, row) in enumerate(top3.iterrows()):
        with cols[i]:
            st.markdown(
                f"""<div class="aday-dark-card" style="text-align:center;">
                <div style="font-size:2rem;">{medals[i]}</div>
                <div style="font-size:1.1rem; font-weight:700;">{row['Team']}</div>
                <div style="opacity:0.85;">{row['Total Points']:.1f} pts</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.write("")
    st.subheader("Full rankings")
    st.dataframe(board, width='stretch', hide_index=True)

    st.write("")
    st.subheader("Top teams by total points")
    chart_df = board.head(10).set_index("Team")[["Total Points"]]
    st.bar_chart(chart_df)

    with st.expander("Per-case breakdown"):
        breakdown = get_breakdown()
        if breakdown.empty:
            st.caption("No scores recorded yet.")
        else:
            st.dataframe(breakdown, width='stretch')

if auto:
    import time
    time.sleep(15)
    st.rerun()
