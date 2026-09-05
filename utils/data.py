"""
Static content for A-Day: Crack the Code.
Edit this file to change event copy, schedule times, or the event date —
nothing else in the app needs to change.
"""

EVENT_NAME = "A-Day: Crack the Code"
EVENT_TAGLINE = "One day. Six cases. A campus full of clues waiting to be decoded."
EVENT_DATE = "2026-10-24 10:00:00"  # edit to your actual date — used for the home page countdown

CASES = [
    {
        "code": "solo_01",
        "name": "60-Second Verdict",
        "kind": "Solo Case · 01",
        "subtitle": "Buzzer in hand. Clock running. No time to overthink.",
        "what": "A high-speed buzzer quiz of logic traps and data trivia — speed matters as much as knowledge.",
        "steps": [
            "Small buzzer pods; a question appears on screen.",
            "Fastest correct buzz scores; wrong buzz locks you out.",
            "Pod winners advance to a knockout final.",
        ],
        "facts": {"Format": "Individual, knockout", "Duration": "40 minutes",
                   "Tests": "Speed, analytical recall", "Scoring": "Buzzer accuracy under time"},
        "quote": "Fast thinking beats big knowledge.",
    },
    {
        "code": "group_01",
        "name": "The Campus Cipher",
        "kind": "Group Case · 01",
        "subtitle": "A jigsaw of the campus — solved from memory, finished on foot.",
        "what": "A campus jigsaw that unlocks inside-out — teams reason out the picture before they can even see it.",
        "steps": [
            "Solve inner pieces first; outer pieces unlock in sequence.",
            "Identify the campus spot the finished image shows.",
            "Reach the spot, click a team photo, upload to close the case.",
        ],
        "facts": {"Team Size": "4–6 members", "Duration": "35–40 minutes",
                   "Tests": "Visual reasoning, memory, teamwork", "Scoring": "Speed + correct location"},
        "quote": "See the pattern before you see the picture.",
    },
    {
        "code": "group_02",
        "name": "Bull Street",
        "kind": "Group Case · 02",
        "subtitle": "A stock market built from real history — your calls, your profit.",
        "what": "Teams trade a mini portfolio using real historical stock data, company profiles, and period news.",
        "steps": [
            "Get virtual capital and a dossier on 4–5 companies.",
            "Market moves in rounds; news cards drop between them.",
            "Buy, hold or sell — highest portfolio value wins.",
        ],
        "facts": {"Team Size": "4–6 members", "Duration": "45 minutes",
                   "Tests": "Risk judgment, pattern reading", "Scoring": "Final portfolio value"},
        "quote": "Every trade is a bet on a pattern.",
    },
    {
        "code": "group_03",
        "name": "Real or Rigged",
        "kind": "Group Case · 03",
        "subtitle": "Two charts. One is telling the truth.",
        "what": "Teams see real vs. manipulated chart pairs and must spot the fake — and explain the trick.",
        "steps": [
            "Each round: one real, one rigged chart or stat.",
            "Team marks the manipulated one against the clock.",
            "Name the trick used for bonus points.",
        ],
        "facts": {"Team Size": "3–4 members", "Duration": "30 minutes",
                   "Tests": "Data literacy, skepticism", "Scoring": "Accuracy + reasoning"},
        "quote": "Numbers don't lie. Presentations do.",
    },
    {
        "code": "solo_02",
        "name": "Checkmate in Two",
        "kind": "Solo Case · 02",
        "subtitle": "One board. A forced win hiding in plain sight.",
        "what": "A timed chess-puzzle bracket — find the forced mate-in-1 or mate-in-2, not just a good move.",
        "steps": [
            "Board position shown with a forced mate hidden in it.",
            "Call the winning move sequence before time runs out.",
            "Faster, correct solves score higher each round.",
        ],
        "facts": {"Format": "Individual, timed rounds", "Duration": "40 minutes",
                   "Tests": "Forward planning, precision", "Scoring": "Correctness + speed"},
        "quote": "One right move beats ten good ones.",
    },
    {
        "code": "finale",
        "name": "The Last Case",
        "kind": "Grand Finale",
        "subtitle": "A campus-wide treasure hunt for the day's top analysts.",
        "what": "Winners and runners-up from every case qualify and are re-grouped for one final hunt across campus.",
        "steps": [
            "Qualifying teams get the first riddle — a campus-based clue.",
            "Solving it reveals a spot; reaching it hands over a task and the next clue.",
            "Each leg reveals a piece of the final code — first to crack it wins A-Day.",
        ],
        "facts": {"Format": "Re-grouped qualifiers", "Duration": "~90 minutes",
                   "Tests": "Everything, at once", "Scoring": "First team to solve"},
        "quote": "The last clue is always the hardest to see.",
    },
]

CASE_NAMES = [c["name"] for c in CASES]

SCHEDULE = [
    ("10:00", "Registration & Check-in", "Kits and buzzer codes handed out, WiFi shared."),
    ("10:45", "Opening & 60-Second Verdict", "Quick briefing, then the solo buzzer quiz opens the day."),
    ("12:00", "Group Cases Run Parallel", "Campus Cipher, Bull Street and Real or Rigged, three zones."),
    ("2:00", "Lunch & Leaderboard Reveal", "Live scoreboard update at the food zone."),
    ("3:15", "Checkmate in Two", "Afternoon solo chess-puzzle knockout."),
    ("4:45", "Qualifier Announcement", "Top scorers re-grouped for the finale."),
    ("5:15", "The Last Case", "Campus-wide finale hunt, tracked live at base camp."),
    ("7:00", "Prize Distribution & Close", "Winners announced, closing group photo."),
]

BUDGET = [
    ("Venue & basic infra", "Seating, sound, signage", 15000),
    ("Event materials", "Buzzers, print sets, stationery", 10000),
    ("Prizes & certificates", "Winners, runner-ups, finalists", 20000),
    ("Marketing", "Posters, IDs, social boosts", 5000),
    ("Refreshments", "Snacks & lunch, all day", 15000),
    ("Technology", "Forms, backup internet, printing", 3000),
    ("Contingency (10%)", "Buffer for last-minute needs", 6800),
]

# Brand colours — keep these in sync with .streamlit/config.toml
PRIMARY = "#0B4F6C"
PRIMARY_DARK = "#073547"
ACCENT = "#F2A541"
ICE = "#EAF6F8"
