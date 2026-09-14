import json
from db import get_connection


def save_analysis(student_skills_text, job_description_text, result):
    connection = get_connection()
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO analyses (
            student_skills, internship_description, detected_student_skills,
            detected_required_skills, matched_skills, missing_skills, match_percentage
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        student_skills_text, job_description_text,
        json.dumps(result["student_skills"]), json.dumps(result["required_skills"]),
        json.dumps(result["matched_skills"]), json.dumps(result["missing_skills"]),
        result["match_percentage"],
    )
    cursor.execute(insert_query, values)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def get_all_analyses():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, match_percentage, created_at FROM analyses ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def get_analysis_by_id(analysis_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM analyses WHERE id = %s", (analysis_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row is None:
        return None
    row["detected_student_skills"] = json.loads(row["detected_student_skills"])
    row["detected_required_skills"] = json.loads(row["detected_required_skills"])
    row["matched_skills"] = json.loads(row["matched_skills"])
    row["missing_skills"] = json.loads(row["missing_skills"])
    return row


def delete_analysis_by_id(analysis_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = %s", (analysis_id,))
    connection.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    connection.close()
    return deleted


def clear_all_history():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM analyses")
    connection.commit()
    deleted_count = cursor.rowcount
    cursor.close()
    connection.close()
    return deleted_count