# A-Day: Crack the Code — Event Tracker

A Streamlit site for running A-Day end-to-end: team registration, a live
leaderboard, event/schedule info pages, and an admin panel to record scores.

```
aday_site/
├── app.py                      # Home page
├── pages/
│   ├── 1_📝_Register.py        # Team registration form
│   ├── 2_🏆_Leaderboard.py     # Live standings + per-case breakdown
│   ├── 3_🎯_Events.py          # The 6 cases, from the deck
│   ├── 4_🗓️_Schedule.py        # Day timeline + budget snapshot
│   └── 5_🔐_Admin.py           # Password-gated: add teams, record scores, export CSV
├── utils/
│   ├── data.py                  # All event copy, schedule, budget — edit this, not the pages
│   ├── db.py                    # SQLite read/write helpers
│   └── ui.py                    # Shared styling + logo rendering
├── assets/                      # Put your logo here (see guide below)
├── .streamlit/
│   ├── config.toml              # Theme colors (teal/amber, matches the deck)
│   └── secrets.toml.example     # Copy to secrets.toml, don't commit the real one
├── requirements.txt
└── .gitignore
```

## 1. Run it locally

```bash
cd aday_site
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and set a real admin_password
streamlit run app.py
```

It opens at `http://localhost:8501`. A SQLite file `aday.db` is created next
to `app.py` the first time it runs — that's your database, nothing else to
set up.

## 2. Push it to GitHub

Streamlit Community Cloud deploys straight from a GitHub repo.

1. Create a new repo (e.g. `aday-tracker`) on GitHub.
2. From inside the `aday_site` folder:
   ```bash
   git init
   git add .
   git commit -m "A-Day event tracker"
   git branch -M main
   git remote add origin https://github.com/<your-username>/aday-tracker.git
   git push -u origin main
   ```
3. Double-check `.streamlit/secrets.toml` was **not** pushed (it's in
   `.gitignore`) — only `secrets.toml.example` should be in the repo.

## 3. Deploy on Streamlit Community Cloud

1. Go to **share.streamlit.io** and sign in with GitHub.
2. Click **"New app"** → pick your `aday-tracker` repo → branch `main` →
   main file path `app.py`.
3. Before clicking Deploy, open **"Advanced settings" → Secrets** and paste:
   ```toml
   admin_password = "put-a-real-password-here"
   ```
4. Click **Deploy**. In a minute or two you'll get a URL like
   `https://aday-tracker.streamlit.app` — that's the live site.

**A note on data persistence:** Streamlit Cloud's disk is ephemeral — the
`aday.db` SQLite file survives while your app stays awake, but a redeploy or
a long sleep can reset it. For a single event day this is completely fine
(the app wakes up once, runs all day, you export the CSVs from Admin at the
end). If you want scores to survive redeploys too, see the optional upgrade
at the bottom of this file.

## 4. Integrating the IIM Amritsar logo

The app doesn't ship with the actual logo file — you'll need to add your
institute's official logo yourself (so you're using the correct, current,
and authorized version rather than one pulled off the web).

**Step 1 — Get the official file.** Ask your institute's communications
or admin office for the official logo, or download it from IIM Amritsar's
own website/brand-guidelines page. Prefer a PNG with a transparent
background if one is available.

**Step 2 — Name and place the file.** Put it in the `assets/` folder and
name it exactly:
```
assets/iim_amritsar_logo.png
```
(A `.jpg` named `iim_amritsar_logo.jpg` also works — the app checks for
both.) Once it's there, delete `assets/PUT_LOGO_HERE.txt`.

**Step 3 — That's it, actually.** Every page already calls
`render_sidebar_logo()`, which auto-detects the file and:
- Shows it at the top of the sidebar on every page.
- Falls back to a "logo missing" placeholder box if the file isn't there yet
  (so the app never crashes for lack of a logo).

It also becomes the browser tab icon (favicon) and the small top-left
`st.logo` badge, via `apply_page_config()` in `utils/ui.py` — no extra code
needed.

**Step 4 — Redeploy.** Commit and push the new file:
```bash
git add assets/iim_amritsar_logo.png
git commit -m "Add IIM Amritsar logo"
git push
```
Streamlit Cloud auto-redeploys on every push to `main`.

**Optional — logo on printed certificates or exports.** If you later add a
certificate-generation feature (e.g. with `reportlab` or `fpdf2`), point it
at the same `assets/iim_amritsar_logo.png` path so every artifact uses one
source file — change the logo once, it updates everywhere.

## 5. Using it on the day

- Share the site link for **Register** ahead of time.
- Organizers log into **Admin** (sidebar → Admin, then the password from
  Secrets) to enter scores as each case wraps up.
- Project the **Leaderboard** page on a screen at base camp — toggle
  "Auto-refresh every 15s" so it updates itself.
- At the end of the day, go to Admin → Export and download the CSVs for
  your records.

## Editing event content

Everything text-based — event descriptions, the schedule, the budget table —
lives in `utils/data.py`. Change it there and every page picks it up
automatically; you never need to touch the page files for a content update.

## Optional: persistent storage with Google Sheets

If you're running this across multiple days/redeploys and want the
database to never reset, swap SQLite for a Google Sheet:

1. Create a Google Cloud service account, enable the Sheets API, and share
   your sheet with the service account's email.
2. `pip install gspread google-auth`
3. Replace the functions in `utils/db.py` with equivalents that read/write
   rows via `gspread` instead of `sqlite3`. The function signatures
   (`add_team`, `get_teams`, `upsert_score`, `get_leaderboard`, ...) can stay
   the same, so no page file needs to change.
4. Store the service account JSON in Streamlit Secrets, not in the repo.

This is a bigger lift than the SQLite version, so it's left as an upgrade
path rather than the default — most one-day fests won't need it.
