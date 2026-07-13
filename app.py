
import random
import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="PlanForge",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
HERO_IMAGE = BASE_DIR / "assets" / "hero.png"
DB_PATH = BASE_DIR / "planforge.db"

EXERCISES = [
    {
        "name": "Bench press",
        "muscle": "Prsia",
        "secondary": "Triceps, predné ramená",
        "equipment": ["Veľká činka", "Lavička"],
        "level": ["Mierne pokročilý", "Pokročilý"],
        "pattern": "horizontal_push",
        "tips": "Lopatky stiahni dozadu, chodidlá pevne na zemi a činku spúšťaj kontrolovane na spodnú časť hrudníka.",
        "setup": "Rovná lavička. Oči približne pod osou činky. Úchop mierne širší ako ramená.",
    },
    {
        "name": "Tlaky s jednoručkami na šikmej lavičke",
        "muscle": "Horné prsia",
        "secondary": "Predné ramená, triceps",
        "equipment": ["Jednoručky", "Lavička"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "incline_push",
        "tips": "Lakte drž mierne pod úrovňou ramien a činky spúšťaj kontrolovane.",
        "setup": "Lavičku nastav približne na 25–35 stupňov.",
    },
    {
        "name": "Chest press na stroji",
        "muscle": "Prsia",
        "secondary": "Triceps, predné ramená",
        "equipment": ["Stroje"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "horizontal_push",
        "tips": "Nedvíhaj ramená k ušiam a neodrážaj záťaž.",
        "setup": "Sedadlo nastav tak, aby rukoväte boli približne v strede hrudníka.",
    },
    {
        "name": "Kliky",
        "muscle": "Prsia",
        "secondary": "Triceps, ramená, core",
        "equipment": ["Vlastná váha"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "horizontal_push",
        "tips": "Telo drž v jednej línii a hrudník spúšťaj medzi dlane.",
        "setup": "Dlane mierne širšie ako ramená.",
    },
    {
        "name": "Rozpažovanie na kladkách",
        "muscle": "Prsia",
        "secondary": "Predné ramená",
        "equipment": ["Kladka"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "chest_isolation",
        "tips": "Lakte nechaj mierne pokrčené a pohyb veď oblúkom.",
        "setup": "Kladky nastav približne na úroveň ramien.",
    },
    {
        "name": "Tlaky nad hlavu s jednoručkami",
        "muscle": "Ramená",
        "secondary": "Triceps",
        "equipment": ["Jednoručky", "Lavička"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "vertical_push",
        "tips": "Nezakláňaj sa a nevytláčaj činky príliš ďaleko pred telo.",
        "setup": "Operadlo nastav približne na 75–85 stupňov.",
    },
    {
        "name": "Shoulder press na stroji",
        "muscle": "Ramená",
        "secondary": "Triceps",
        "equipment": ["Stroje"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "vertical_push",
        "tips": "Ramená drž dole a lakte neprepínaj.",
        "setup": "Sedadlo nastav tak, aby rukoväte začínali približne pri úrovni brady.",
    },
    {
        "name": "Upažovanie s jednoručkami",
        "muscle": "Bočné ramená",
        "secondary": "Trapézy",
        "equipment": ["Jednoručky"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "shoulder_isolation",
        "tips": "Dvíhaj lakte, nie zápästia. Nepoužívaj švih.",
        "setup": "Mierny predklon, lakte jemne pokrčené.",
    },
    {
        "name": "Upažovanie na kladke",
        "muscle": "Bočné ramená",
        "secondary": "Trapézy",
        "equipment": ["Kladka"],
        "level": ["Mierne pokročilý", "Pokročilý"],
        "pattern": "shoulder_isolation",
        "tips": "Pohyb veď plynulo a zastav približne v úrovni ramien.",
        "setup": "Spodná kladka, stoj bokom k stroju.",
    },
    {
        "name": "Sťahovanie hornej kladky",
        "muscle": "Chrbát",
        "secondary": "Biceps",
        "equipment": ["Kladka"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "vertical_pull",
        "tips": "Ťahaj lakte smerom dole a hrudník drž mierne hore.",
        "setup": "Stehná zaisti pod valce, úchop mierne širší ako ramená.",
    },
    {
        "name": "Zhyby",
        "muscle": "Chrbát",
        "secondary": "Biceps, predlaktia",
        "equipment": ["Hrazda", "Vlastná váha"],
        "level": ["Mierne pokročilý", "Pokročilý"],
        "pattern": "vertical_pull",
        "tips": "Začni stiahnutím lopatiek a nehojdaj sa.",
        "setup": "Nadhmat približne na šírku ramien alebo mierne širšie.",
    },
    {
        "name": "Príťahy jednoručky v predklone",
        "muscle": "Chrbát",
        "secondary": "Biceps, zadné ramená",
        "equipment": ["Jednoručky", "Lavička"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "horizontal_pull",
        "tips": "Ťahaj lakeť k boku a neotáčaj trup.",
        "setup": "Jedno koleno a dlaň opri o lavičku.",
    },
    {
        "name": "Veslovanie na kladke",
        "muscle": "Chrbát",
        "secondary": "Biceps, zadné ramená",
        "equipment": ["Kladka"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "horizontal_pull",
        "tips": "Nevytláčaj hlavu dopredu a neprehýbaj kríže.",
        "setup": "Chodidlá opri, kolená mierne pokrč a trup drž stabilne.",
    },
    {
        "name": "Face pull",
        "muscle": "Zadné ramená",
        "secondary": "Horný chrbát",
        "equipment": ["Kladka"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "rear_delt",
        "tips": "Ťahaj lano k tvári a lakte drž vysoko.",
        "setup": "Kladku nastav približne do výšky očí.",
    },
    {
        "name": "Bicepsový zdvih s jednoručkami",
        "muscle": "Biceps",
        "secondary": "Predlaktia",
        "equipment": ["Jednoručky"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "biceps",
        "tips": "Lakte drž pri tele a nehojdaj trupom.",
        "setup": "Stoj vzpriamene, dlane smerujú dopredu.",
    },
    {
        "name": "Bicepsový zdvih na kladke",
        "muscle": "Biceps",
        "secondary": "Predlaktia",
        "equipment": ["Kladka"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "biceps",
        "tips": "Napätie drž počas celého pohybu.",
        "setup": "Spodná kladka, lakte pri tele.",
    },
    {
        "name": "Tricepsové stláčanie lana",
        "muscle": "Triceps",
        "secondary": "Predlaktia",
        "equipment": ["Kladka"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "triceps",
        "tips": "Lakte nepúšťaj dopredu a dole lano mierne roztiahni.",
        "setup": "Horná kladka s lanom.",
    },
    {
        "name": "Francúzsky tlak s jednoručkou",
        "muscle": "Triceps",
        "secondary": "Ramená",
        "equipment": ["Jednoručky", "Lavička"],
        "level": ["Mierne pokročilý", "Pokročilý"],
        "pattern": "triceps",
        "tips": "Lakte drž čo najstabilnejšie a pohyb rob kontrolovane.",
        "setup": "Sediaca alebo ležiaca verzia.",
    },
    {
        "name": "Leg press",
        "muscle": "Kvadricepsy",
        "secondary": "Zadok, hamstringy",
        "equipment": ["Stroje"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "squat",
        "tips": "Kolená smerujú v línii so špičkami. Neodlepuj panvu.",
        "setup": "Chodidlá približne na šírku ramien v strede platformy.",
    },
    {
        "name": "Goblet drep",
        "muscle": "Kvadricepsy",
        "secondary": "Zadok, core",
        "equipment": ["Jednoručky"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "squat",
        "tips": "Koleno drž v smere špičky a trup čo najvzpriamenejší.",
        "setup": "Jednoručku drž pred hrudníkom.",
    },
    {
        "name": "Drep s veľkou činkou",
        "muscle": "Kvadricepsy",
        "secondary": "Zadok, hamstringy, core",
        "equipment": ["Veľká činka", "Stojan"],
        "level": ["Mierne pokročilý", "Pokročilý"],
        "pattern": "squat",
        "tips": "Spevni brucho, kolená drž v línii so špičkami a nepadni dopredu.",
        "setup": "Činku polož stabilne na hornú časť chrbta.",
    },
    {
        "name": "Bulharský drep",
        "muscle": "Kvadricepsy",
        "secondary": "Zadok, hamstringy",
        "equipment": ["Jednoručky", "Lavička"],
        "level": ["Mierne pokročilý", "Pokročilý"],
        "pattern": "single_leg",
        "tips": "Predné chodidlo polož dosť ďaleko, aby sa päta neodlepovala.",
        "setup": "Zadnú nohu polož na lavičku.",
    },
    {
        "name": "Výpady s jednoručkami",
        "muscle": "Kvadricepsy",
        "secondary": "Zadok, hamstringy",
        "equipment": ["Jednoručky"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "single_leg",
        "tips": "Krok urob dostatočne dlhý a drž stabilný trup.",
        "setup": "Jednoručky drž vedľa tela.",
    },
    {
        "name": "Rumunský mŕtvy ťah s jednoručkami",
        "muscle": "Hamstringy",
        "secondary": "Zadok, spodný chrbát",
        "equipment": ["Jednoručky"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "hinge",
        "tips": "Boky tlač dozadu a chrbát drž neutrálny.",
        "setup": "Činky drž pred stehnami, kolená jemne pokrčené.",
    },
    {
        "name": "Rumunský mŕtvy ťah s veľkou činkou",
        "muscle": "Hamstringy",
        "secondary": "Zadok, spodný chrbát",
        "equipment": ["Veľká činka"],
        "level": ["Mierne pokročilý", "Pokročilý"],
        "pattern": "hinge",
        "tips": "Činku drž blízko nôh a pohyb začni bokmi.",
        "setup": "Úchop približne na šírku ramien.",
    },
    {
        "name": "Zakopávanie",
        "muscle": "Hamstringy",
        "secondary": "Lýtka",
        "equipment": ["Stroje"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "hamstring_curl",
        "tips": "Panvu drž pritlačenú a neodrážaj záťaž.",
        "setup": "Valec nastav tesne nad pätami.",
    },
    {
        "name": "Predkopávanie",
        "muscle": "Kvadricepsy",
        "secondary": "—",
        "equipment": ["Stroje"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "quad_isolation",
        "tips": "Hore krátko zatni stehno a dole nepúšťaj závažie voľným pádom.",
        "setup": "Os otáčania stroja zarovnaj s kolenom.",
    },
    {
        "name": "Hip thrust",
        "muscle": "Zadok",
        "secondary": "Hamstringy",
        "equipment": ["Veľká činka", "Lavička"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "glute",
        "tips": "Hore podsad panvu a neprehýbaj kríže.",
        "setup": "Lopatky opri o lavičku, činku polož cez panvu.",
    },
    {
        "name": "Výpony v stoji",
        "muscle": "Lýtka",
        "secondary": "—",
        "equipment": ["Jednoručky"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "calves",
        "tips": "Choď cez plný rozsah a hore na chvíľu zastav.",
        "setup": "Môžeš stáť na vyvýšenej podložke.",
    },
    {
        "name": "Plank",
        "muscle": "Core",
        "secondary": "Ramená, zadok",
        "equipment": ["Vlastná váha"],
        "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
        "pattern": "core",
        "tips": "Zadok nedvíhaj ani neprepadaj. Brucho drž pevné.",
        "setup": "Lakte pod ramenami.",
    },
]

SPLITS = {
    2: [
        ("Deň 1 · Full Body A", ["horizontal_push", "vertical_pull", "squat", "hinge", "shoulder_isolation", "biceps"]),
        ("Deň 2 · Full Body B", ["incline_push", "horizontal_pull", "single_leg", "hamstring_curl", "vertical_push", "triceps"]),
    ],
    3: [
        ("Deň 1 · Vrch tela", ["horizontal_push", "vertical_pull", "vertical_push", "horizontal_pull", "biceps", "triceps"]),
        ("Deň 2 · Spodok tela", ["squat", "hinge", "single_leg", "hamstring_curl", "calves", "core"]),
        ("Deň 3 · Full Body", ["incline_push", "horizontal_pull", "squat", "rear_delt", "biceps", "triceps"]),
    ],
    4: [
        ("Deň 1 · Upper A", ["horizontal_push", "vertical_pull", "vertical_push", "horizontal_pull", "biceps", "triceps"]),
        ("Deň 2 · Lower A", ["squat", "hinge", "quad_isolation", "hamstring_curl", "calves", "core"]),
        ("Deň 3 · Upper B", ["incline_push", "horizontal_pull", "chest_isolation", "rear_delt", "shoulder_isolation", "triceps"]),
        ("Deň 4 · Lower B", ["single_leg", "glute", "hamstring_curl", "quad_isolation", "calves", "core"]),
    ],
    5: [
        ("Deň 1 · Push", ["horizontal_push", "incline_push", "vertical_push", "shoulder_isolation", "triceps", "triceps"]),
        ("Deň 2 · Pull", ["vertical_pull", "horizontal_pull", "horizontal_pull", "rear_delt", "biceps", "biceps"]),
        ("Deň 3 · Legs", ["squat", "hinge", "single_leg", "hamstring_curl", "quad_isolation", "calves"]),
        ("Deň 4 · Upper", ["incline_push", "vertical_pull", "horizontal_push", "horizontal_pull", "shoulder_isolation", "biceps"]),
        ("Deň 5 · Lower", ["squat", "glute", "hamstring_curl", "quad_isolation", "calves", "core"]),
    ],
    6: [
        ("Deň 1 · Push A", ["horizontal_push", "incline_push", "vertical_push", "shoulder_isolation", "triceps"]),
        ("Deň 2 · Pull A", ["vertical_pull", "horizontal_pull", "rear_delt", "biceps", "biceps"]),
        ("Deň 3 · Legs A", ["squat", "hinge", "hamstring_curl", "calves", "core"]),
        ("Deň 4 · Push B", ["incline_push", "chest_isolation", "vertical_push", "shoulder_isolation", "triceps"]),
        ("Deň 5 · Pull B", ["horizontal_pull", "vertical_pull", "rear_delt", "biceps", "biceps"]),
        ("Deň 6 · Legs B", ["single_leg", "glute", "quad_isolation", "hamstring_curl", "calves"]),
    ],
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Oswald:wght@600;700&display=swap');

:root {
  --bg: #080a0f;
  --panel: #10131a;
  --panel-2: #161a22;
  --text: #f5f7fb;
  --muted: #9aa3b2;
  --accent: #ff5e1f;
  --accent-2: #ff8533;
  --line: rgba(255,255,255,.08);
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
}

.stApp {
  background:
    radial-gradient(circle at 85% 10%, rgba(255,94,31,.12), transparent 22%),
    radial-gradient(circle at 10% 40%, rgba(111,66,193,.08), transparent 25%),
    var(--bg);
  color: var(--text);
}

.block-container {
  max-width: 1280px;
  padding-top: 1.5rem;
  padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0e1117 0%, #0a0c11 100%);
  border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
  color: #f5f7fb;
}

h1, h2, h3 {
  letter-spacing: -.02em;
}

.hero {
  position: relative;
  overflow: hidden;
  min-height: 530px;
  border: 1px solid var(--line);
  border-radius: 28px;
  background-size: cover;
  background-position: center;
  box-shadow: 0 30px 80px rgba(0,0,0,.35);
  margin-bottom: 1.4rem;
}

.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(7,9,13,.97) 0%, rgba(7,9,13,.88) 42%, rgba(7,9,13,.18) 76%);
}

.hero-content {
  position: relative;
  z-index: 2;
  width: min(650px, 92%);
  padding: 72px 64px;
}

.eyebrow {
  color: var(--accent);
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .18em;
  text-transform: uppercase;
  margin-bottom: 14px;
}

.hero-title {
  font-family: 'Oswald', sans-serif;
  font-size: clamp(48px, 7vw, 90px);
  line-height: .95;
  text-transform: uppercase;
  margin: 0 0 20px 0;
}

.hero-copy {
  color: #c7ced9;
  font-size: 18px;
  line-height: 1.7;
  max-width: 570px;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 24px;
}

.badge {
  border: 1px solid var(--line);
  background: rgba(16,19,26,.72);
  backdrop-filter: blur(10px);
  padding: 10px 14px;
  border-radius: 999px;
  color: #e8ebf0;
  font-size: 13px;
  font-weight: 700;
}

.card {
  background: linear-gradient(180deg, rgba(22,26,34,.96), rgba(13,16,22,.96));
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 22px;
  box-shadow: 0 14px 40px rgba(0,0,0,.22);
  height: 100%;
}

.card h3 {
  margin-top: 0;
}

.metric {
  background: linear-gradient(180deg, rgba(22,26,34,.96), rgba(13,16,22,.96));
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 18px;
}

.metric-label {
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: .12em;
  font-weight: 700;
}

.metric-value {
  font-size: 26px;
  font-weight: 800;
  margin-top: 7px;
}

.workout-card {
  background: linear-gradient(160deg, rgba(20,23,31,.98), rgba(10,12,17,.98));
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 22px;
  margin-bottom: 18px;
}

.exercise-card {
  background: rgba(255,255,255,.028);
  border: 1px solid rgba(255,255,255,.07);
  border-radius: 16px;
  padding: 18px;
  margin: 10px 0;
}

.exercise-name {
  font-size: 18px;
  font-weight: 800;
  margin-bottom: 7px;
}

.exercise-meta {
  color: #aeb6c2;
  font-size: 13px;
}

.accent {
  color: var(--accent);
}

.small-muted {
  color: var(--muted);
  font-size: 13px;
}

div.stButton > button {
  width: 100%;
  border-radius: 12px;
  border: 1px solid rgba(255,94,31,.5);
  background: linear-gradient(90deg, #ff5e1f, #ff7a2f);
  color: white;
  font-weight: 800;
  min-height: 48px;
  box-shadow: 0 10px 24px rgba(255,94,31,.18);
}

div.stButton > button:hover {
  border-color: #ff8b52;
  color: white;
  transform: translateY(-1px);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-testid="stNumberInput"] input {
  background: #12161e !important;
  border-color: rgba(255,255,255,.08) !important;
  color: white !important;
  border-radius: 12px !important;
}

.stMultiSelect [data-baseweb="tag"] {
  background: rgba(255,94,31,.18);
}

[data-testid="stTabs"] button {
  color: #c4cad4;
  font-weight: 700;
}

[data-testid="stTabs"] button[aria-selected="true"] {
  color: white;
}

hr {
  border-color: var(--line);
}

.footer {
  text-align: center;
  color: #7f8794;
  padding-top: 38px;
  font-size: 12px;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

for key, default in {
    "screen": "Domov",
    "plan": [],
    "profile": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def normalize_muscle_group(muscle):
    muscle = muscle.lower()
    if "prsia" in muscle:
        return "Prsia"
    if "ramen" in muscle:
        return "Ramená"
    if "chrb" in muscle:
        return "Chrbát"
    if "biceps" in muscle:
        return "Biceps"
    if "triceps" in muscle:
        return "Triceps"
    if "kvadriceps" in muscle or "hamstring" in muscle:
        return "Nohy"
    if "zadok" in muscle:
        return "Zadok"
    if "lýtka" in muscle:
        return "Lýtka"
    if "core" in muscle:
        return "Core"
    return muscle.title()

def detailed_muscle_group(muscle):
    muscle = muscle.lower()
    if "horné prsia" in muscle or "prsia" in muscle:
        return "Prsia"
    if "zadné ramená" in muscle or "bočné ramená" in muscle or "ramená" in muscle:
        return "Ramená"
    if "chrbát" in muscle:
        return "Chrbát"
    if "biceps" in muscle:
        return "Biceps"
    if "triceps" in muscle:
        return "Triceps"
    if "kvadriceps" in muscle:
        return "Kvadricepsy"
    if "hamstring" in muscle:
        return "Hamstringy"
    if "zadok" in muscle:
        return "Zadok"
    if "lýtka" in muscle:
        return "Lýtka"
    if "core" in muscle:
        return "Core"
    return muscle.title()


def group_exercises_by_muscle(exercises):
    """
    Zachová poradie, v ktorom sa partie v tréningu prvýkrát objavia,
    ale všetky cviky rovnakej partie presunie k sebe.
    Príklad: chrbát, ramená, chrbát, triceps ->
    chrbát, chrbát, ramená, triceps.
    """
    group_order = []
    grouped = {}

    for exercise in exercises:
        group = detailed_muscle_group(exercise["muscle"])
        if group not in grouped:
            grouped[group] = []
            group_order.append(group)
        grouped[group].append(exercise)

    ordered = []
    for group in group_order:
        ordered.extend(grouped[group])
    return ordered


def available_exercises(profile):
    equipment = set(profile["equipment"])
    excluded = set(profile["excluded"])
    excluded_muscles = set(profile.get("excluded_muscles", []))
    level = profile["level"]

    result = []
    for ex in EXERCISES:
        if ex["name"] in excluded:
            continue
        if normalize_muscle_group(ex["muscle"]) in excluded_muscles:
            continue
        if level not in ex["level"]:
            continue
        if not set(ex["equipment"]).intersection(equipment):
            continue
        result.append(ex)
    return result

def exercise_for_pattern(pattern, pool, used, profile):
    choices = [ex for ex in pool if ex["pattern"] == pattern and ex["name"] not in used]
    if not choices:
        choices = [ex for ex in pool if ex["pattern"] == pattern]
    if not choices:
        return None

    # Pohlavie nič nezakazuje. Používa sa iba na jemné predvolené poradie.
    # Ženám pri tlakoch častejšie ponúkne jednoručky alebo stroj, no bench zostáva dostupný.
    if profile.get("sex") == "Žena" and pattern in {"horizontal_push", "incline_push"}:
        preferred = [
            "Tlaky s jednoručkami na šikmej lavičke",
            "Chest press na stroji",
            "Kliky",
            "Bench press",
        ]
        ranked = sorted(choices, key=lambda ex: preferred.index(ex["name"]) if ex["name"] in preferred else 99)
        top_rank = preferred.index(ranked[0]["name"]) if ranked[0]["name"] in preferred else 99
        best = [ex for ex in ranked if (preferred.index(ex["name"]) if ex["name"] in preferred else 99) == top_rank]
        return random.choice(best)

    # Pri vyššom veku dá pri hlavných cvikoch miernu prednosť stabilnejším variantom.
    if profile.get("age", 0) >= 50 and pattern in {"horizontal_push", "vertical_push", "squat"}:
        machine_choices = [ex for ex in choices if "Stroje" in ex["equipment"]]
        if machine_choices:
            return random.choice(machine_choices)

    return random.choice(choices)

def order_patterns(patterns, profile):
    """
    Zoradí cviky tak, aby plán nepôsobil náhodne:
    1. hlavné viackĺbové cviky
    2. ďalšie veľké pohyby
    3. doplnkové cviky
    4. izolácie a core
    Prioritná partia sa môže posunúť dopredu.
    """
    base_order = {
        # hlavné cviky na vrch
        "horizontal_push": 10,
        "horizontal_pull": 20,
        "vertical_pull": 30,
        "vertical_push": 40,
        "incline_push": 45,

        # hlavné cviky na spodok
        "squat": 10,
        "hinge": 20,
        "single_leg": 30,
        "glute": 35,

        # doplnkové a izolované cviky
        "chest_isolation": 60,
        "rear_delt": 65,
        "shoulder_isolation": 70,
        "quad_isolation": 75,
        "hamstring_curl": 80,
        "calves": 85,
        "biceps": 90,
        "triceps": 92,
        "core": 95,
    }

    priority_patterns = {
        "Prsia": {"horizontal_push", "incline_push", "chest_isolation"},
        "Ramená": {"vertical_push", "shoulder_isolation", "rear_delt"},
        "Chrbát": {"horizontal_pull", "vertical_pull", "rear_delt"},
        "Ruky": {"biceps", "triceps"},
        "Nohy": {"squat", "hinge", "single_leg", "quad_isolation", "hamstring_curl"},
        "Zadok": {"glute", "single_leg", "hinge"},
    }

    priority = priority_patterns.get(profile.get("priority"), set())

    indexed = list(enumerate(patterns))
    indexed.sort(
        key=lambda item: (
            -1 if item[1] in priority else 0,
            base_order.get(item[1], 50),
            item[0],
        )
    )
    return [pattern for _, pattern in indexed]


def generate_plan(profile):
    pool = available_exercises(profile)
    split = SPLITS[profile["days"]]
    plan = []
    global_used = set()

    for day_name, patterns in split:
        day_exercises = []
        local_used = set()

        # Add one extra exercise for the chosen priority when possible.
        priority_map = {
            "Prsia": "chest_isolation",
            "Ramená": "shoulder_isolation",
            "Chrbát": "horizontal_pull",
            "Ruky": "biceps",
            "Zadok": "glute",
            "Nohy": "quad_isolation",
            "Bez priority": None,
        }
        final_patterns = list(patterns)
        priority_pattern = priority_map.get(profile["priority"])

        # Jemná automatická personalizácia bez tvrdých stereotypov.
        if profile.get("priority") == "Bez priority" and profile.get("sex") == "Žena":
            priority_pattern = "glute"
        if priority_pattern and profile["goal"] == "Naberanie svalov":
            final_patterns.append(priority_pattern)

        final_patterns = order_patterns(final_patterns, profile)

        for pattern in final_patterns:
            ex = exercise_for_pattern(pattern, pool, local_used, profile)
            if ex:
                local_used.add(ex["name"])
                global_used.add(ex["name"])
                if profile["goal"] == "Sila" and pattern in {"horizontal_push", "squat", "hinge", "vertical_pull"}:
                    sets, reps = 4, "4–6"
                elif pattern in {"shoulder_isolation", "biceps", "triceps", "calves", "rear_delt", "quad_isolation", "hamstring_curl", "chest_isolation", "glute"}:
                    sets, reps = 3, "10–15"
                else:
                    sets, reps = 3, "6–10"

                # Začiatočník alebo starší cvičenec začne miernejším objemom.
                if profile.get("level") == "Začiatočník":
                    sets = min(sets, 3)
                if profile.get("age", 0) >= 55:
                    sets = min(sets, 3)
                    if reps == "4–6":
                        reps = "6–8"

                day_exercises.append({
                    **ex,
                    "sets": sets,
                    "reps": reps,
                    "rest": "90–120 s" if reps in {"4–6", "6–8"} else "60–90 s",
                })

        day_exercises = group_exercises_by_muscle(day_exercises)
        plan.append({"day": day_name, "exercises": day_exercises})
    return plan

def swap_exercise(day_idx, ex_idx):
    profile = st.session_state.profile
    pool = available_exercises(profile)
    current = st.session_state.plan[day_idx]["exercises"][ex_idx]
    candidates = [
        ex for ex in pool
        if ex["pattern"] == current["pattern"] and ex["name"] != current["name"]
    ]
    if not candidates:
        st.warning("Pre tento cvik momentálne nemáme ďalšiu vhodnú alternatívu pri zvolenom vybavení.")
        return
    replacement = random.choice(candidates)
    st.session_state.plan[day_idx]["exercises"][ex_idx] = {
        **replacement,
        "sets": current["sets"],
        "reps": current["reps"],
        "rest": current["rest"],
    }
    st.rerun()


def init_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS weekly_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_no INTEGER NOT NULL UNIQUE,
                logged_on TEXT NOT NULL,
                avg_weight REAL NOT NULL,
                waist REAL,
                completed_sessions INTEGER NOT NULL,
                strength_status TEXT NOT NULL,
                recovery INTEGER NOT NULL,
                notes TEXT
            )
            """
        )
        conn.commit()


def load_progress():
    init_database()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT week_no, logged_on, avg_weight, waist,
                   completed_sessions, strength_status, recovery, notes
            FROM weekly_progress
            ORDER BY week_no ASC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def save_progress_record(
    week_no,
    logged_on,
    avg_weight,
    waist,
    completed_sessions,
    strength_status,
    recovery,
    notes,
):
    init_database()
    waist_value = None if waist <= 0 else float(waist)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO weekly_progress (
                week_no, logged_on, avg_weight, waist,
                completed_sessions, strength_status, recovery, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(week_no) DO UPDATE SET
                logged_on = excluded.logged_on,
                avg_weight = excluded.avg_weight,
                waist = excluded.waist,
                completed_sessions = excluded.completed_sessions,
                strength_status = excluded.strength_status,
                recovery = excluded.recovery,
                notes = excluded.notes
            """,
            (
                int(week_no),
                logged_on.isoformat(),
                float(avg_weight),
                waist_value,
                int(completed_sessions),
                strength_status,
                int(recovery),
                notes.strip(),
            ),
        )
        conn.commit()


def clear_progress():
    init_database()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM weekly_progress")
        conn.commit()


def analyze_progress(records, profile):
    if len(records) < 2:
        return {
            "status": "Potrebujeme ešte jeden týždeň",
            "tone": "info",
            "message": "Po prvom zápise ešte nevieme rozlíšiť trend od bežného kolísania váhy.",
            "recommendation": "Pokračuj podľa plánu a o týždeň zapíš ďalší týždenný priemer.",
            "adjustment": "none",
        }

    previous = records[-2]
    current = records[-1]
    previous_weight = float(previous["avg_weight"])
    current_weight = float(current["avg_weight"])
    change_kg = current_weight - previous_weight
    change_pct = (change_kg / previous_weight) * 100 if previous_weight else 0
    planned_sessions = max(1, int(profile.get("days", 3)))
    adherence = int(current["completed_sessions"]) / planned_sessions
    strength = current["strength_status"]
    recovery = int(current["recovery"])
    goal = profile.get("goal", "Naberanie svalov")

    direction = f"{change_kg:+.2f} kg ({change_pct:+.2f} %)"
    base = f"Od minulého týždňa: **{direction}**. Odcvičené: **{current['completed_sessions']}/{planned_sessions}** tréningov."

    if adherence < 0.75:
        return {
            "status": "Najprv zlepši pravidelnosť",
            "tone": "warning",
            "message": base,
            "recommendation": "Tréning zatiaľ nemeníme. Pri nízkej dochádzke by appka nevedela, či stagnuje plán alebo iba chýbajú tréningy.",
            "adjustment": "none",
        }

    if goal == "Chudnutie":
        if -0.75 <= change_pct <= -0.25:
            return {
                "status": "Tempo chudnutia je v poriadku",
                "tone": "success",
                "message": base,
                "recommendation": "Nechaj tréning bez zmeny. Snaž sa udržať silu a rovnakú pravidelnosť.",
                "adjustment": "none",
            }
        if change_pct > -0.25:
            if strength == "Slabší" or recovery <= 2:
                return {
                    "status": "Váha stagnuje, ale regenerácia je slabá",
                    "tone": "warning",
                    "message": base,
                    "recommendation": "Nepridávaj ďalší tréning. Najprv zlepši spánok a regeneráciu; kalorický príjem skontroluj samostatne.",
                    "adjustment": "none",
                }
            return {
                "status": "Chudnutie stagnuje",
                "tone": "warning",
                "message": base,
                "recommendation": "Silový plán necháme a pridáme krátke kardio po dvoch tréningoch. Zároveň skontroluj priemerný kalorický príjem.",
                "adjustment": "add_cardio",
            }
        return {
            "status": "Chudneš príliš rýchlo",
            "tone": "warning",
            "message": base,
            "recommendation": "Ak klesá sila alebo regenerácia, znížime doplnkový objem. Hlavné silové cviky zostanú.",
            "adjustment": "reduce_volume" if strength == "Slabší" or recovery <= 2 else "none",
        }

    if goal == "Naberanie svalov":
        if 0.10 <= change_pct <= 0.35:
            return {
                "status": "Tempo naberania je v poriadku",
                "tone": "success",
                "message": base,
                "recommendation": "Tréning nemeníme. Pokračuj v progresívnom pridávaní opakovaní alebo váhy.",
                "adjustment": "none",
            }
        if change_pct < 0.10:
            if strength == "Silnejší":
                return {
                    "status": "Váha stojí, ale výkon rastie",
                    "tone": "success",
                    "message": base,
                    "recommendation": "Zatiaľ nič nemeň. Výkon je lepší signál než jeden týždeň váhy.",
                    "adjustment": "none",
                }
            if recovery >= 3:
                return {
                    "status": "Naberanie stagnuje",
                    "tone": "warning",
                    "message": base,
                    "recommendation": "Pridáme malý objem prioritnej partii. Súčasne skontroluj, či je príjem energie dostatočný.",
                    "adjustment": "add_priority_volume",
                }
            return {
                "status": "Stagnácia s horšou regeneráciou",
                "tone": "warning",
                "message": base,
                "recommendation": "Objem nepridávame. Najprv zlepši regeneráciu a až potom tréning navyšuj.",
                "adjustment": "none",
            }
        return {
            "status": "Váha rastie rýchlo",
            "tone": "warning",
            "message": base,
            "recommendation": "Tréning nechaj. Skontroluj však príjem energie, pretože rýchlejší nárast nemusí byť iba svalová hmota.",
            "adjustment": "none",
        }

    if goal == "Sila":
        if strength == "Silnejší":
            return {
                "status": "Silový progres pokračuje",
                "tone": "success",
                "message": base,
                "recommendation": "Plán nemeníme. Pokračuj v malých prírastkoch váhy alebo opakovaní.",
                "adjustment": "none",
            }
        if strength == "Rovnaký" and recovery >= 3:
            return {
                "status": "Sila stagnuje, regenerácia je dobrá",
                "tone": "warning",
                "message": base,
                "recommendation": "Pridáme jednu pracovnú sériu k prvému hlavnému cviku v tréningu.",
                "adjustment": "add_compound_set",
            }
        return {
            "status": "Sila alebo regenerácia klesá",
            "tone": "warning",
            "message": base,
            "recommendation": "Znížime doplnkový objem a necháme hlavné cviky.",
            "adjustment": "reduce_volume",
        }

    # Kondícia
    if recovery >= 3 and strength != "Slabší":
        return {
            "status": "Môžeš mierne pridať kondíciu",
            "tone": "success",
            "message": base,
            "recommendation": "Pridáme krátky kondičný finisher po dvoch tréningoch.",
            "adjustment": "add_cardio",
        }
    return {
        "status": "Kondičný objem zatiaľ nepridávame",
        "tone": "warning",
        "message": base,
        "recommendation": "Najprv stabilizuj regeneráciu a dokončovanie naplánovaných tréningov.",
        "adjustment": "none",
    }


def apply_progress_adjustment(adjustment, profile):
    if not st.session_state.plan:
        return False

    if adjustment == "add_cardio":
        cardio = {
            "name": "Kondičný finisher",
            "muscle": "Kondícia",
            "secondary": "Srdcovo-cievna kondícia",
            "equipment": ["Vlastná váha"],
            "level": ["Začiatočník", "Mierne pokročilý", "Pokročilý"],
            "pattern": "cardio",
            "tips": "Pracuj v tempe, pri ktorom ešte držíš techniku. Nechoď každý týždeň úplne na doraz.",
            "setup": "10–15 minút: svižná chôdza, bicykel, orbitrek alebo intervaly 30 s práce / 60 s voľne.",
            "sets": 1,
            "reps": "10–15 min",
            "rest": "podľa potreby",
        }
        added = 0
        for day in st.session_state.plan:
            if added >= 2:
                break
            if not any(ex.get("pattern") == "cardio" for ex in day["exercises"]):
                day["exercises"].append(dict(cardio))
                added += 1
        return added > 0

    if adjustment == "add_priority_volume":
        priority = profile.get("priority", "Bez priority")
        target_groups = {
            "Prsia": {"Prsia"},
            "Ramená": {"Ramená"},
            "Chrbát": {"Chrbát"},
            "Ruky": {"Biceps", "Triceps"},
            "Nohy": {"Kvadricepsy", "Hamstringy"},
            "Zadok": {"Zadok"},
        }.get(priority, set())

        changed = 0
        for day in st.session_state.plan:
            for exercise in day["exercises"]:
                group = detailed_muscle_group(exercise["muscle"])
                if (target_groups and group in target_groups) or (not target_groups and changed < 2):
                    exercise["sets"] = min(5, int(exercise["sets"]) + 1)
                    changed += 1
                    break
        return changed > 0

    if adjustment == "add_compound_set":
        changed = 0
        for day in st.session_state.plan:
            if day["exercises"]:
                first = day["exercises"][0]
                first["sets"] = min(5, int(first["sets"]) + 1)
                changed += 1
        return changed > 0

    if adjustment == "reduce_volume":
        isolation_patterns = {
            "chest_isolation", "shoulder_isolation", "rear_delt",
            "biceps", "triceps", "quad_isolation",
            "hamstring_curl", "calves", "core",
        }
        changed = 0
        for day in st.session_state.plan:
            candidates = [
                exercise for exercise in reversed(day["exercises"])
                if exercise.get("pattern") in isolation_patterns
            ]
            if candidates:
                candidates[0]["sets"] = max(2, int(candidates[0]["sets"]) - 1)
                changed += 1
        return changed > 0

    return False


def set_screen(name):
    st.session_state.screen = name
    st.rerun()

init_database()

with st.sidebar:
    st.markdown("## 🔥 PlanForge")
    st.caption("Smart workout generator")
    st.markdown("---")
    if st.button("🏠 Domov", use_container_width=True):
        set_screen("Domov")
    if st.button("⚙️ Vytvoriť plán", use_container_width=True):
        set_screen("Generátor")
    if st.button("📋 Môj plán", use_container_width=True, disabled=not bool(st.session_state.plan)):
        set_screen("Plán")
    if st.button("📈 Týždenný progres", use_container_width=True, disabled=not bool(st.session_state.profile)):
        set_screen("Progres")
    st.markdown("---")
    st.markdown(
        "<div class='small-muted'>Verzia 1.1<br>Python + Streamlit + SQLite</div>",
        unsafe_allow_html=True,
    )

if st.session_state.screen == "Domov":
    hero_b64 = HERO_IMAGE.read_bytes()
    import base64
    encoded = base64.b64encode(hero_b64).decode()
    st.markdown(
        f"""
        <section class="hero" style="background-image:url('data:image/png;base64,{encoded}')">
          <div class="hero-content">
            <div class="eyebrow">Tréning podľa teba</div>
            <h1 class="hero-title">Žiadne<br><span class="accent">náhodné</span><br>cviky.</h1>
            <div class="hero-copy">
              Vytvor si tréning podľa cieľa, vybavenia, skúseností a cvikov,
              ktoré reálne chceš robiť. Každý cvik má techniku, nastavenie a vhodnú náhradu.
            </div>
            <div class="badges">
              <span class="badge">✓ podľa vybavenia</span>
              <span class="badge">✓ bez nechcených cvikov</span>
              <span class="badge">✓ rozumné náhrady</span>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="card">
              <div class="eyebrow">01</div>
              <h3>Vyber si cieľ</h3>
              <p class="small-muted">Svaly, sila, chudnutie alebo kondícia. Plán sa prispôsobí tomu, čo chceš dosiahnuť.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
              <div class="eyebrow">02</div>
              <h3>Zakáž cviky</h3>
              <p class="small-muted">Nechceš drepy, výpady alebo mŕtvy ťah? Appka ich nebude nasilu pchať do plánu.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="card">
              <div class="eyebrow">03</div>
              <h3>Vymieňaj rozumne</h3>
              <p class="small-muted">Každá náhrada zachová svalovú partiu aj pohybový vzor, nie náhodnú kokotinu.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    if st.button("Vytvoriť môj tréningový plán →", use_container_width=True):
        set_screen("Generátor")

elif st.session_state.screen == "Generátor":
    st.markdown("## Vytvor si tréning")
    st.caption("Vyplň profil. Pohlavie nič automaticky nezakazuje — ty si vyberieš, ktoré partie alebo konkrétne cviky nechceš v pláne vôbec mať.")

    with st.form("generator"):
        left, right = st.columns(2)
        with left:
            sex = st.selectbox("Pohlavie", ["Muž", "Žena", "Nechcem uviesť"])
            age = st.number_input("Vek", min_value=14, max_value=90, value=29, step=1)
            height = st.number_input("Výška (cm)", min_value=130, max_value=230, value=181, step=1)
            weight = st.number_input("Váha (kg)", min_value=35.0, max_value=250.0, value=80.0, step=0.5)
            goal = st.selectbox("Hlavný cieľ", ["Naberanie svalov", "Sila", "Chudnutie", "Kondícia"])
            level = st.selectbox("Úroveň", ["Začiatočník", "Mierne pokročilý", "Pokročilý"], index=1)

        with right:
            days = st.select_slider("Koľko dní týždenne chceš cvičiť?", options=[2, 3, 4, 5, 6], value=4)
            priority = st.selectbox("Prioritná partia", ["Bez priority", "Prsia", "Ramená", "Chrbát", "Ruky", "Zadok", "Nohy"])
            equipment = st.multiselect(
                "Aké máš vybavenie?",
                ["Vlastná váha", "Jednoručky", "Veľká činka", "Lavička", "Stojan", "Kladka", "Stroje", "Hrazda"],
                default=["Jednoručky", "Veľká činka", "Lavička", "Kladka", "Stroje", "Hrazda"],
            )
            all_names = [ex["name"] for ex in EXERCISES]
            excluded_muscles = st.multiselect(
                "Ktoré partie nechceš vôbec trénovať?",
                ["Prsia", "Ramená", "Chrbát", "Biceps", "Triceps", "Nohy", "Zadok", "Lýtka", "Core"],
                help="Napríklad žena môže zvoliť Prsia, ak ich nechce mať v pláne. Appka ich potom úplne vynechá."
            )
            excluded = st.multiselect("Ktoré konkrétne cviky nechceš robiť?", all_names)
            session_length = st.selectbox("Dĺžka tréningu", ["45 min", "60 min", "75 min", "90 min"], index=1)

        submitted = st.form_submit_button("Vygenerovať plán")

    if submitted:
        if not equipment:
            st.error("Vyber aspoň jedno vybavenie.")
        else:
            profile = {
                "sex": sex,
                "age": int(age),
                "height": int(height),
                "weight": float(weight),
                "goal": goal,
                "level": level,
                "days": days,
                "priority": priority,
                "equipment": equipment,
                "excluded_muscles": excluded_muscles,
                "excluded": excluded,
                "session_length": session_length,
            }
            pool = available_exercises(profile)
            if len(pool) < 8:
                st.error("Po vynechaní zvolených partií a cvikov ostalo príliš málo možností. Povoľ viac vybavenia alebo vynechaj menej partií.")
            else:
                st.session_state.profile = profile
                st.session_state.plan = generate_plan(profile)
                set_screen("Plán")

elif st.session_state.screen == "Plán":
    profile = st.session_state.profile
    st.markdown("## Tvoj tréningový plán")
    st.caption("Cviky sú zoskupené po partiách: všetky cviky na rovnakú partiu idú za sebou. V rámci partie ide najprv hlavný cvik a potom doplnkové cviky.")
    if profile.get("excluded_muscles"):
        st.info("Vynechané partie: " + ", ".join(profile["excluded_muscles"]))

    bmi = round(profile.get("weight", 0) / ((profile.get("height", 1) / 100) ** 2), 1)
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    metrics = [
        ("Profil", profile.get("sex", "—")),
        ("Vek", f"{profile.get('age', '—')} r."),
        ("Postava", f"{profile.get('height', '—')} cm / {profile.get('weight', '—')} kg"),
        ("BMI", bmi),
        ("Frekvencia", f"{profile.get('days', '—')}×"),
        ("Cieľ", profile.get("goal", "—")),
    ]
    for col, (label, value) in zip([m1, m2, m3, m4, m5, m6], metrics):
        with col:
            st.markdown(
                f"<div class='metric'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>",
                unsafe_allow_html=True,
            )

    st.write("")
    tabs = st.tabs([item["day"] for item in st.session_state.plan])

    for day_idx, (tab, day) in enumerate(zip(tabs, st.session_state.plan)):
        with tab:
            st.markdown(f"<div class='workout-card'><div class='eyebrow'>Tréning</div><h2>{day['day']}</h2>", unsafe_allow_html=True)

            previous_group = None
            for ex_idx, ex in enumerate(day["exercises"]):
                current_group = detailed_muscle_group(ex["muscle"])
                if current_group != previous_group:
                    st.markdown(
                        f"<div class='eyebrow' style='margin-top:18px'>{current_group}</div>",
                        unsafe_allow_html=True,
                    )
                    previous_group = current_group

                col1, col2 = st.columns([4, 1.15])
                with col1:
                    st.markdown(
                        f"""
                        <div class="exercise-card">
                          <div class="exercise-name">{ex_idx + 1}. {ex['name']}</div>
                          <div class="exercise-meta">
                            <strong class="accent">{ex['muscle']}</strong> · {ex['sets']} série · {ex['reps']} opakovaní · pauza {ex['rest']}
                          </div>
                          <div class="small-muted" style="margin-top:8px">Sekundárne: {ex['secondary']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    with st.expander("Technika a nastavenie"):
                        st.markdown(f"**Nastavenie:** {ex['setup']}")
                        st.markdown(f"**Technika:** {ex['tips']}")
                        st.markdown(f"**Vybavenie:** {', '.join(ex['equipment'])}")
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🔄 Vymeniť", key=f"swap_{day_idx}_{ex_idx}"):
                        swap_exercise(day_idx, ex_idx)

            st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Upraviť nastavenia"):
            set_screen("Generátor")
    with c2:
        if st.button("Vygenerovať nový variant"):
            st.session_state.plan = generate_plan(st.session_state.profile)
            st.rerun()


elif st.session_state.screen == "Progres":
    profile = st.session_state.profile
    records = load_progress()
    next_week = (records[-1]["week_no"] + 1) if records else 1
    default_weight = float(records[-1]["avg_weight"]) if records else float(profile.get("weight", 80.0))

    st.markdown("## Týždenný progres")
    st.caption(
        "Zapisuj priemernú rannú váhu za celý týždeň, nie náhodné váženie po jedle. "
        "Appka porovná tempo, odcvičené tréningy, silu a regeneráciu."
    )

    left, right = st.columns([1, 1.25])

    with left:
        with st.form("weekly_progress_form"):
            week_no = st.number_input("Týždeň", min_value=1, value=int(next_week), step=1)
            logged_on = st.date_input("Dátum zápisu", value=date.today())
            avg_weight = st.number_input(
                "Priemerná váha za týždeň (kg)",
                min_value=30.0,
                max_value=300.0,
                value=default_weight,
                step=0.1,
            )
            waist = st.number_input(
                "Obvod pása (cm, nepovinné)",
                min_value=0.0,
                max_value=250.0,
                value=0.0,
                step=0.5,
            )
            completed_sessions = st.number_input(
                "Koľko tréningov si odcvičil?",
                min_value=0,
                max_value=14,
                value=int(profile.get("days", 3)),
                step=1,
            )
            strength_status = st.selectbox(
                "Výkon oproti minulému týždňu",
                ["Silnejší", "Rovnaký", "Slabší"],
                index=1,
            )
            recovery = st.slider("Regenerácia", min_value=1, max_value=5, value=3)
            notes = st.text_area("Poznámka", placeholder="Spánok, choroba, cheat deň, bolesť, zmena režimu...")
            save_clicked = st.form_submit_button("Uložiť týždeň")

        if save_clicked:
            save_progress_record(
                week_no,
                logged_on,
                avg_weight,
                waist,
                completed_sessions,
                strength_status,
                recovery,
                notes,
            )
            st.success(f"Týždeň {int(week_no)} bol uložený.")
            st.rerun()

    with right:
        if not records:
            st.markdown(
                """
                <div class="card">
                  <div class="eyebrow">Začíname</div>
                  <h3>Zatiaľ nemáš uložený žiadny týždeň</h3>
                  <p class="small-muted">
                    Prvý zápis vytvorí východiskový bod. Reálny trend appka vyhodnotí od druhého týždňa.
                  </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            analysis = analyze_progress(records, profile)
            if analysis["tone"] == "success":
                st.success(f"**{analysis['status']}**\n\n{analysis['message']}")
            elif analysis["tone"] == "warning":
                st.warning(f"**{analysis['status']}**\n\n{analysis['message']}")
            else:
                st.info(f"**{analysis['status']}**\n\n{analysis['message']}")

            st.markdown(
                f"""
                <div class="card">
                  <div class="eyebrow">Odporúčanie</div>
                  <h3>{analysis['status']}</h3>
                  <p class="small-muted">{analysis['recommendation']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if analysis["adjustment"] != "none":
                if st.button("Použiť odporúčanú úpravu tréningu"):
                    changed = apply_progress_adjustment(analysis["adjustment"], profile)
                    if changed:
                        st.success("Tréningový plán bol upravený podľa progresu.")
                    else:
                        st.info("V aktuálnom pláne nebolo čo bezpečne upraviť.")

    records = load_progress()
    if records:
        st.write("")
        chart_data = pd.DataFrame(
            {
                "Týždeň": [f"Týždeň {row['week_no']}" for row in records],
                "Váha (kg)": [row["avg_weight"] for row in records],
            }
        ).set_index("Týždeň")
        st.markdown("### Vývoj váhy")
        st.line_chart(chart_data, height=320)

        table_data = pd.DataFrame(
            [
                {
                    "Týždeň": row["week_no"],
                    "Dátum": row["logged_on"],
                    "Priemerná váha": row["avg_weight"],
                    "Pás": row["waist"] if row["waist"] is not None else "—",
                    "Tréningy": f"{row['completed_sessions']}/{profile.get('days', '—')}",
                    "Výkon": row["strength_status"],
                    "Regenerácia": f"{row['recovery']}/5",
                    "Poznámka": row["notes"] or "—",
                }
                for row in records
            ]
        )
        st.dataframe(table_data, use_container_width=True, hide_index=True)

        with st.expander("Správa uložených údajov"):
            st.caption("Vymazanie odstráni všetky týždenné zápisy uložené v lokálnej databáze tejto appky.")
            if st.button("Vymazať celý progres", type="secondary"):
                clear_progress()
                st.rerun()


st.markdown(
    "<div class='footer'>PlanForge · tréningový plán a týždenné sledovanie progresu</div>",
    unsafe_allow_html=True,
)
