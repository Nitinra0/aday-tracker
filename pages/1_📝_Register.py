import streamlit as st
from utils.db import init_db, add_team, team_count
from utils.ui import apply_page_config, inject_css, render_sidebar_logo, page_header
from utils.data import EVENT_NAME

apply_page_config(f"Register · {EVENT_NAME}")
inject_css()
init_db()
render_sidebar_logo()

page_header("Sign Up", "Register your team", "One form, one team. Every member should be listed below.")

st.metric("Teams registered so far", team_count())
st.write("")

with st.form("register_form", clear_on_submit=True):
    team_name = st.text_input("Team name *", placeholder="e.g. The Outliers")
    members = st.text_area(
        "Team members *",
        placeholder="One name per line (or comma-separated) — include roll numbers/section if your college needs it.",
        height=100,
    )
    col1, col2 = st.columns(2)
    with col1:
        contact = st.text_input("Contact number / email *", placeholder="For last-minute updates")
    with col2:
        department = st.text_input("Department / batch", placeholder="e.g. MBA 2026–28")

    agree = st.checkbox("We've read the case format and agree to the event rules.")
    submitted = st.form_submit_button("Register team", width='stretch')

    if submitted:
        if not agree:
            st.error("Please confirm you've read the rules before registering.")
        else:
            ok, msg = add_team(team_name, members, contact, department)
            if ok:
                st.success(msg)
                st.balloons()
            else:
                st.error(msg)

st.write("")
st.caption("Trouble registering? Reach out on the event WhatsApp group.")
