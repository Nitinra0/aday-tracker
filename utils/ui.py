"""
Shared look-and-feel helpers so every page renders consistently.
"""

import streamlit as st
from pathlib import Path
from utils.data import PRIMARY, PRIMARY_DARK, ACCENT, ICE

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO_CANDIDATES = ["iim_amritsar_logo.png", "iim_amritsar_logo.jpg", "logo.png"]


def find_logo() -> Path | None:
    for name in LOGO_CANDIDATES:
        p = ASSETS / name
        if p.exists():
            return p
    return None


def inject_css():
    st.markdown(f"""
        <style>
        .stApp {{ background-color: #FFFFFF; }}
        h1, h2, h3 {{ color: {PRIMARY}; font-family: 'Georgia', serif; }}
        .aday-kicker {{
            color: {ACCENT}; font-weight: 700; letter-spacing: 2px;
            font-size: 0.8rem; text-transform: uppercase; margin-bottom: -0.5rem;
        }}
        .aday-card {{
            background-color: {ICE}; border-radius: 10px; padding: 1.1rem 1.3rem;
            margin-bottom: 0.8rem;
        }}
        .aday-dark-card {{
            background-color: {PRIMARY}; color: white; border-radius: 10px;
            padding: 1.1rem 1.3rem; margin-bottom: 0.8rem;
        }}
        .aday-quote {{
            border-left: 4px solid {ACCENT}; padding-left: 0.8rem; font-style: italic;
            color: {PRIMARY}; margin-top: 0.6rem;
        }}
        div.stButton > button {{
            background-color: {PRIMARY}; color: white; border-radius: 6px; border: none;
        }}
        div.stButton > button:hover {{ background-color: {PRIMARY_DARK}; color: white; }}
        section[data-testid="stSidebar"] {{ background-color: {ICE}; }}
        </style>
    """, unsafe_allow_html=True)


def render_sidebar_logo(caption: str = "A-Day · Crack the Code"):
    logo = find_logo()
    with st.sidebar:
        if logo:
            st.image(str(logo), width='stretch')
        else:
            st.markdown(
                f"""<div style="border:1px dashed {PRIMARY}; border-radius:8px; padding:0.8rem;
                text-align:center; color:{PRIMARY}; font-size:0.8rem;">
                Add your college logo at<br><code>assets/iim_amritsar_logo.png</code>
                </div>""",
                unsafe_allow_html=True,
            )
        st.caption(caption)
        st.divider()


def page_header(kicker: str, title: str, subtitle: str = ""):
    st.markdown(f'<div class="aday-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.write("")


def apply_page_config(page_title: str, page_icon_emoji: str = "🕵️"):
    logo = find_logo()
    st.set_page_config(
        page_title=page_title,
        page_icon=str(logo) if logo else page_icon_emoji,
        layout="wide",
    )
    # st.logo puts a small logo in the very top-left corner (Streamlit 1.32+)
    logo = find_logo()
    if logo and hasattr(st, "logo"):
        st.logo(str(logo))
