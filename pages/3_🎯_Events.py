import streamlit as st
from utils.db import init_db
from utils.ui import apply_page_config, inject_css, render_sidebar_logo, page_header
from utils.data import EVENT_NAME, CASES

apply_page_config(f"Events · {EVENT_NAME}")
inject_css()
init_db()
render_sidebar_logo()

page_header("The Cases", "Events", "Three group cases, two solo cases, and one grand finale.")

for case in CASES:
    with st.container(border=True):
        left, right = st.columns([2.2, 1])
        with left:
            st.markdown(f'<div class="aday-kicker">{case["kind"]}</div>', unsafe_allow_html=True)
            st.subheader(case["name"])
            st.caption(case["subtitle"])
            st.write(f"**What it is:** {case['what']}")
            st.write("**How it works:**")
            for i, step in enumerate(case["steps"], 1):
                st.write(f"{i}. {step}")
            st.markdown(f'<div class="aday-quote">{case["quote"]}</div>', unsafe_allow_html=True)
        with right:
            st.markdown('<div class="aday-dark-card">', unsafe_allow_html=True)
            st.markdown("**Quick facts**")
            for k, v in case["facts"].items():
                st.write(f"*{k}:* {v}")
            st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
