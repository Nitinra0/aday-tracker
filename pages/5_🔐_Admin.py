import streamlit as st
import pandas as pd
from utils.db import init_db, get_teams, add_team, delete_team, upsert_score, get_scores_raw, get_leaderboard
from utils.ui import apply_page_config, inject_css, render_sidebar_logo, page_header
from utils.data import EVENT_NAME, CASE_NAMES

apply_page_config(f"Admin · {EVENT_NAME}")
inject_css()
init_db()
render_sidebar_logo()

page_header("Organizers Only", "Admin panel", "Record scores, manage teams, export data.")


def get_admin_password() -> str:
    # Set this in .streamlit/secrets.toml (locally) or the Streamlit Cloud
    # "Secrets" settings (in production) as:
    #   admin_password = "your-real-password"
    # Falls back to a default so the app still runs before you configure it —
    # change this before your event goes live.
    try:
        return st.secrets["admin_password"]
    except Exception:
        return "aday2026"


if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

if not st.session_state.admin_ok:
    pwd = st.text_input("Admin password", type="password")
    if st.button("Log in"):
        if pwd == get_admin_password():
            st.session_state.admin_ok = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

st.success("Logged in as organizer.")
if st.button("Log out"):
    st.session_state.admin_ok = False
    st.rerun()

st.write("")
tab_scores, tab_teams, tab_export = st.tabs(["📊 Record scores", "👥 Manage teams", "⬇️ Export"])

# ------------------------------------------------------------ scores ----
with tab_scores:
    teams_df = get_teams()
    if teams_df.empty:
        st.info("No teams registered yet.")
    else:
        with st.form("score_form"):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                team_choice = st.selectbox("Team", teams_df["team_name"].tolist())
            with col2:
                case_choice = st.selectbox("Case", CASE_NAMES)
            with col3:
                points = st.number_input("Points", min_value=0.0, step=1.0)
            save = st.form_submit_button("Save score", width='stretch')
            if save:
                team_id = int(teams_df.loc[teams_df["team_name"] == team_choice, "id"].iloc[0])
                upsert_score(team_id, case_choice, points)
                st.success(f"Saved: {team_choice} — {case_choice} — {points} pts")
                st.rerun()

        st.write("")
        st.subheader("All recorded scores")
        st.dataframe(get_scores_raw(), width='stretch', hide_index=True)

# ------------------------------------------------------------- teams ----
with tab_teams:
    st.subheader("Add a walk-in team")
    with st.form("admin_add_team", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            tname = st.text_input("Team name")
            contact = st.text_input("Contact")
        with c2:
            members = st.text_area("Members", height=80)
            dept = st.text_input("Department / batch")
        add = st.form_submit_button("Add team")
        if add:
            ok, msg = add_team(tname, members, contact, dept)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()

    st.write("")
    st.subheader("Registered teams")
    teams_df = get_teams()
    st.dataframe(teams_df, width='stretch', hide_index=True)

    if not teams_df.empty:
        remove_choice = st.selectbox("Remove a team", ["—"] + teams_df["team_name"].tolist())
        if remove_choice != "—" and st.button(f"Delete '{remove_choice}'", type="secondary"):
            tid = int(teams_df.loc[teams_df["team_name"] == remove_choice, "id"].iloc[0])
            delete_team(tid)
            st.success(f"Removed '{remove_choice}'.")
            st.rerun()

# ------------------------------------------------------------ export ----
with tab_export:
    st.subheader("Download data")
    teams_csv = get_teams().to_csv(index=False).encode("utf-8")
    scores_csv = get_scores_raw().to_csv(index=False).encode("utf-8")
    board_csv = get_leaderboard().to_csv(index=False).encode("utf-8")

    c1, c2, c3 = st.columns(3)
    c1.download_button("Teams (CSV)", teams_csv, "aday_teams.csv", "text/csv", width='stretch')
    c2.download_button("Scores (CSV)", scores_csv, "aday_scores.csv", "text/csv", width='stretch')
    c3.download_button("Leaderboard (CSV)", board_csv, "aday_leaderboard.csv", "text/csv", width='stretch')
