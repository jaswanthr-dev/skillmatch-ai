import os
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from matcher import analyze_skill_match, generate_preparation_checklist
from history import (
    save_analysis, get_all_analyses, get_analysis_by_id,
    delete_analysis_by_id, clear_all_history,
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        student_skills_text = request.form.get("student_skills", "").strip()
        job_description_text = request.form.get("job_description", "").strip()

        if not student_skills_text or not job_description_text:
            return render_template("index.html",
                error="Please fill in both your skills and the internship description.",
                student_skills=student_skills_text, job_description=job_description_text)

        result = analyze_skill_match(student_skills_text, job_description_text)
        new_id = save_analysis(student_skills_text, job_description_text, result)
        return redirect(url_for("history_detail", analysis_id=new_id))

    return render_template("index.html")


@app.route("/history")
def history():
    analyses = get_all_analyses()
    return render_template("history.html", analyses=analyses)


@app.route("/history/<int:analysis_id>")
def history_detail(analysis_id):
    row = get_analysis_by_id(analysis_id)
    if row is None:
        abort(404)

    match_percentage = float(row["match_percentage"]) if row["match_percentage"] is not None else None
    result = {
        "student_skills": row["detected_student_skills"],
        "required_skills": row["detected_required_skills"],
        "matched_skills": row["matched_skills"],
        "missing_skills": row["missing_skills"],
        "match_percentage": match_percentage,
        "message": None if match_percentage is not None else
            "No recognizable required skills were found in this internship description.",
    }
    result["checklist"] = generate_preparation_checklist(set(result["missing_skills"]))

    return render_template("history_detail.html", result=result,
        analysis_id=analysis_id, created_at=row["created_at"])


@app.route("/history/<int:analysis_id>/delete", methods=["POST"])
def delete_history_entry(analysis_id):
    delete_analysis_by_id(analysis_id)
    flash("Analysis deleted.")
    return redirect(url_for("history"))


@app.route("/history/clear", methods=["POST"])
def clear_history():
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