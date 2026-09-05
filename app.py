import streamlit as st
from datetime import datetime
from utils.db import init_db, team_count
from utils.ui import apply_page_config, inject_css, render_sidebar_logo, page_header
from utils.data import EVENT_NAME, EVENT_TAGLINE, EVENT_DATE, CASES, PRIMARY, ACCENT

apply_page_config(EVENT_NAME)
inject_css()
init_db()
render_sidebar_logo()

# ---------------------------------------------------------------- hero ----
st.markdown(
    f"""
    <div style="background-color:{PRIMARY}; border-radius:14px; padding:2.5rem 2rem; text-align:center;">
        <div style="color:{ACCENT}; letter-spacing:3px; font-size:0.85rem; font-weight:700;">
            ANALYTICS CLUB PRESENTS
        </div>
        <div style="color:white; font-size:3rem; font-weight:800; font-family:Georgia, serif; margin:0.3rem 0;">
            A-DAY
        </div>
        <div style="color:{ACCENT}; font-style:italic; font-size:1.3rem;">CRACK THE CODE</div>
        <div style="color:#EAF6F8; margin-top:0.6rem;">{EVENT_TAGLINE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ------------------------------------------------------------ countdown ----
try:
    event_dt = datetime.fromisoformat(EVENT_DATE)
    delta = event_dt - datetime.now()
    days, hours = delta.days, delta.seconds // 3600
    countdown_text = f"{days} days, {hours} hours to go" if delta.total_seconds() > 0 else "Today's the day! 🎉"
except Exception:
    countdown_text = None

c1, c2, c3, c4 = st.columns(4)
c1.metric("Teams registered", team_count())
c2.metric("Cases", len(CASES))
c3.metric("Format", "3 group · 2 solo")
c4.metric("Countdown", countdown_text or "—")

st.write("")
page_header("Get Started", "Where do you want to go?")

n1, n2, n3, n4 = st.columns(4)
with n1:
    st.markdown('<div class="aday-card">📝 <b>Register</b><br><span style="font-size:0.85rem;">Sign your team up for A-Day.</span></div>', unsafe_allow_html=True)
    st.page_link("pages/1_📝_Register.py", label="Register a team", icon="📝")
with n2:
    st.markdown('<div class="aday-card">🏆 <b>Leaderboard</b><br><span style="font-size:0.85rem;">See live standings across all cases.</span></div>', unsafe_allow_html=True)
    st.page_link("pages/2_🏆_Leaderboard.py", label="View leaderboard", icon="🏆")
with n3:
    st.markdown('<div class="aday-card">🎯 <b>Events</b><br><span style="font-size:0.85rem;">What each case is and how it works.</span></div>', unsafe_allow_html=True)
    st.page_link("pages/3_🎯_Events.py", label="Browse events", icon="🎯")
with n4:
    st.markdown('<div class="aday-card">🗓️ <b>Schedule</b><br><span style="font-size:0.85rem;">How the day flows, start to finish.</span></div>', unsafe_allow_html=True)
    st.page_link("pages/4_🗓️_Schedule.py", label="See schedule", icon="🗓️")

st.write("")
st.info("Organizing the event? Head to **Admin** in the sidebar to record scores and manage teams.")
