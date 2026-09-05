import streamlit as st
from utils.db import init_db
from utils.ui import apply_page_config, inject_css, render_sidebar_logo, page_header
from utils.data import EVENT_NAME, SCHEDULE

apply_page_config(f"Schedule · {EVENT_NAME}")
inject_css()
init_db()
render_sidebar_logo()

page_header("Logistics", "How the day flows", "10 AM to 7 PM — group cases run in parallel, solo cases follow, the finale closes it out.")

for time_, title, desc in SCHEDULE:
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown(f"### {time_}")
    with c2:
        st.markdown(f"**{title}**")
        st.caption(desc)
    st.divider()
