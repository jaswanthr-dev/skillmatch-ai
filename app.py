"""
app.py

The main Flask application. This file defines every route (URL) our
site responds to, and connects them to matcher.py (the matching logic)
and history.py (the database operations).
"""

import os
from datetime import timezone
from zoneinfo import ZoneInfo
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from matcher import analyze_skill_match, generate_preparation_checklist
from history import (
    save_analysis,
    get_all_analyses,
    get_analysis_by_id,
    delete_analysis_by_id,
    clear_all_history,
)

app = Flask(__name__)

# The database stores timestamps in UTC (the server's own clock).
# We convert to this timezone only when DISPLAYING a time to a person -
# the stored value in MySQL never changes, only what we show on screen.
DISPLAY_TIMEZONE = ZoneInfo("Asia/Kolkata")


def to_display_time(naive_utc_datetime):
    """
    Converts a naive datetime (as returned by MySQL, with no timezone
    attached) into the correct local time for display.

    Why "naive_utc_datetime.replace(tzinfo=timezone.utc)" first: MySQL
    gives us a datetime with no timezone info attached at all - Python
    doesn't know it's UTC unless we tell it. This line labels it as
    UTC without changing the actual time value. Only THEN can we
    correctly convert it to another timezone with .astimezone().
    """
    utc_time = naive_utc_datetime.replace(tzinfo=timezone.utc)
    return utc_time.astimezone(DISPLAY_TIMEZONE)

# A secret key is required for Flask's flash() messages to work (they're
# stored in a signed cookie). We read it from the environment instead of
# hardcoding it, same reasoning as our database credentials: never write
# secrets directly into code. If it's missing, we fall back to a random
# one so the app doesn't crash - but flash messages won't survive an app
# restart in that case, which is fine for local development.
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))


@app.route("/", methods=["GET", "POST"])
def home():
    """
    GET: show the empty input form.
    POST: validate input, run the matching logic, save the result to
    the database, then redirect to that saved result's own page.

    Why we redirect instead of rendering the result directly (this is
    called the "Post/Redirect/Get" pattern): if we rendered results
    straight from a POST, refreshing the browser would resubmit the
    form and create duplicate entries. Redirecting to a GET page (the
    saved analysis's own URL) avoids that entirely.
    """
    if request.method == "POST":
        student_skills_text = request.form.get("student_skills", "").strip()
        job_description_text = request.form.get("job_description", "").strip()

        if not student_skills_text or not job_description_text:
            return render_template(
                "index.html",
                error="Please fill in both your skills and the internship description.",
                student_skills=student_skills_text,
                job_description=job_description_text,
            )

        result = analyze_skill_match(student_skills_text, job_description_text)
        new_id = save_analysis(student_skills_text, job_description_text, result)

        return redirect(url_for("history_detail", analysis_id=new_id))

    return render_template("index.html")


@app.route("/history")
def history():
    """
    Shows a list of every saved analysis, newest first, as links to
    each one's detail page.
    """
    analyses = get_all_analyses()

    # Convert each entry's stored UTC time to local time for display,
    # without touching what's actually saved in the database.
    for entry in analyses:
        entry["created_at"] = to_display_time(entry["created_at"])

    return render_template("history.html", analyses=analyses)


@app.route("/history/<int:analysis_id>")
def history_detail(analysis_id):
    """
    Shows one specific saved analysis in full detail.

    Why `abort(404)`: if someone visits a URL for an id that doesn't
    exist (e.g. it was already deleted, or they typed a random
    number), we show a proper "Not Found" page instead of crashing
    with a confusing error.
    """
    row = get_analysis_by_id(analysis_id)

    if row is None:
        abort(404)

    # Rebuild the same shape of dictionary that analyze_skill_match()
    # returns, so result_partial.html can display it identically
    # whether it's a fresh result or one loaded from history.
    match_percentage = float(row["match_percentage"]) if row["match_percentage"] is not None else None

    result = {
        "student_skills": row["detected_student_skills"],
        "required_skills": row["detected_required_skills"],
        "matched_skills": row["matched_skills"],
        "missing_skills": row["missing_skills"],
        "match_percentage": match_percentage,
        "message": None if match_percentage is not None else (
            "No recognizable required skills were found in this internship description."
        ),
    }
    # Checklist isn't stored directly - we regenerate it from
    # missing_skills using the same function matcher.py already has.
    result["checklist"] = generate_preparation_checklist(set(result["missing_skills"]))

    return render_template(
        "history_detail.html",
        result=result,
        analysis_id=analysis_id,
        created_at=to_display_time(row["created_at"]),
    )


@app.route("/history/<int:analysis_id>/delete", methods=["POST"])
def delete_history_entry(analysis_id):
    """
    Deletes one analysis. Only accepts POST (not GET), so a search
    engine crawler or an accidental link click can't delete data -
    deleting requires an actual form submission.
    """
    delete_analysis_by_id(analysis_id)
    flash("Analysis deleted.")
    return redirect(url_for("history"))


@app.route("/history/clear", methods=["POST"])
def clear_history():
    """
    Deletes EVERY saved analysis. The confirmation dialog itself lives
    in JavaScript (static/js/script.js) - by the time this route runs,
    the user has already confirmed they want to do this.
    """
    deleted_count = clear_all_history()

    if deleted_count == 0:
        flash("There was nothing to clear.")
    elif deleted_count == 1:
        flash("Deleted 1 analysis.")
    else:
        flash(f"Deleted {deleted_count} analyses.")

    return redirect(url_for("history"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)