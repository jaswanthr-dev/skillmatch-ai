# SkillMatch AI — Internship Skill Matcher

A beginner-built web application where a student pastes their skills and
an internship description, and gets back matched skills, missing
skills, a match percentage, and a short preparation checklist.

This is keyword-based matching, not AI - it looks for known skill terms
in both texts and compares them.

## Installation
python -m venv venv
venv\Scripts\activate   (Windows) or source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt

## MySQL Setup
mysql -u root -p < sql/schema.sql

## Environment Variables
Copy .env.example to .env, fill in DB_PASSWORD and SECRET_KEY.

## Run
python app.py
Open http://127.0.0.1:5000

## Test
python -m unittest test_matcher.py test_validation.py -v

## Deploying to GitHub + Vercel
git init && git add . && git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

Create a free MySQL database on aiven.io, then import your repo at
vercel.com/new. Add DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY
as environment variables in Vercel's project settings, then Deploy.

Run schema.sql once against your Aiven database:
mysql -h <aiven-host> -P <aiven-port> -u <aiven-user> -p <db-name> < sql/schema.sql