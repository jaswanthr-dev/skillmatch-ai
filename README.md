# SkillMatch AI

**A keyword-based internship skill matcher, built with Flask and MySQL.**

Paste your skills and an internship description, and get back a match score, matched and missing skills, and a personalized preparation checklist — all saved to a running history you can revisit anytime.

🔗 **Live demo:** [skillmatch-ai-six.vercel.app](https://skillmatch-ai-six.vercel.app)

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)

---

## What it does

1. You paste your skills and a job/internship description.
2. It scans both texts for known skill keywords — handling common synonyms like `js`/`javascript`, `sql`/`mysql`, and `ml`/`machine learning`.
3. You get back:
   - A **match score**, calculated as matched ÷ required skills
   - **Matched** and **missing** skill lists
   - A short **preparation checklist** for each missing skill
4. Every analysis is saved automatically — browse or delete your history anytime.

**Important:** this is keyword matching, not AI. It compares text against a fixed skill list — it doesn't understand context, experience level, or nuance. Treat it as a quick estimate, not a hiring judgment.

## Why keyword-based, on purpose

This was built as a learning project, so the matching logic is intentionally transparent: no external AI APIs, no ML models — just readable Python you can trace line by line in `matcher.py`. That trade-off is deliberate; the goal was understanding every part of the system, not maximizing accuracy.

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.13, Flask |
| Database | MySQL, via `mysql-connector-python` (a direct driver, not an ORM — every query is visible and hand-written) |
| Frontend | Jinja templates, vanilla HTML/CSS/JS — no frontend framework |
| Hosting | Vercel (app) + Aiven (MySQL) |
| Testing | `unittest` |

## Features

- Skill detection with synonym handling (`js` ↔ `javascript`, `html5` ↔ `html`, etc.)
- Match percentage, safely handling the zero-required-skills edge case
- Full history: view, revisit, and delete past analyses
- Light/dark theme, with a custom-styled confirmation modal for destructive actions
- Responsive layout with a collapsing mobile nav
- 29 automated tests covering the matching logic and form validation

| File/Folder | Purpose |
|---|---|
| `app.py` | Flask routes — home form, results, history, delete/clear |
| `matcher.py` | Skill detection, synonym handling, matching, checklist logic |
| `db.py` | MySQL connection helper |
| `history.py` | Save / read / delete saved analyses |
| `templates/` | Jinja templates for every page |
| `static/` | CSS and JS, served locally by Flask in development |
| `public/static/` | Same CSS/JS, served directly by Vercel in production |
| `sql/schema.sql` | Database + table definition |
| `test_*.py` | Automated tests (29 total) |

## Running It Locally

**1. Clone and set up a virtual environment**
```bash
git clone https://github.com/jaswanthr-dev/skillmatch-ai.git
cd skillmatch-ai
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

**2. Set up MySQL**
```bash
mysql -u root -p < sql/schema.sql
```

**3. Configure environment variables**
```bash
copy .env.example .env       # Windows
cp .env.example .env         # macOS/Linux
```
Fill in your real MySQL password and a random `SECRET_KEY` in `.env`.

**4. Run it**
```bash
python app.py
```
Open `http://127.0.0.1:5000`.

**5. Run the tests**
```bash
python -m unittest test_matcher.py test_validation.py -v
```

## Deployment

This app is deployed on **Vercel** (zero-config Flask support) with a free **Aiven** MySQL instance.

## Limitations

- Keyword matching only — no understanding of context, seniority, or depth of experience
- The skill list in `matcher.py` is fixed; anything not on it won't be detected
- No user accounts yet — history is shared across anyone using the same deployment, not private per person

## Possible Future Improvements

- User accounts, so history is private per person
- Move the skill list into the database, so it's editable without a code change
- Pagination for the history list
- Weight skills by frequency of mention, instead of a binary "detected or not"

---

Built as a learning project to practice Flask, MySQL, and full-stack deployment fundamentals.
