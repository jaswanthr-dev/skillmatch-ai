"""
test_matcher.py

Simple unit tests for matcher.py.

Run these with:
    python -m unittest test_matcher.py
"""

import unittest
from matcher import (
    normalize_text,
    detect_skills,
    match_skills,
    calculate_match_percentage,
    generate_preparation_checklist,
    analyze_skill_match,
)


class TestNormalizeText(unittest.TestCase):
    def test_lowercases_text(self):
        self.assertEqual(normalize_text("Python"), "python")

    def test_handles_none(self):
        self.assertEqual(normalize_text(None), "")

    def test_strips_whitespace(self):
        self.assertEqual(normalize_text("  SQL  "), "sql")


class TestDetectSkills(unittest.TestCase):
    def test_detects_single_skill(self):
        result = detect_skills("I know Python well.")
        self.assertIn("python", result)

    def test_avoids_partial_word_match(self):
        result = detect_skills("I know javascript.")
        self.assertIn("javascript", result)
        self.assertNotIn("java", result)

    def test_detects_multiword_skill(self):
        result = detect_skills("Experience with machine learning models.")
        self.assertIn("machine learning", result)

    def test_removes_duplicates(self):
        result = detect_skills("python python PYTHON")
        self.assertEqual(result, {"python"})

    def test_no_skills_found_returns_empty_set(self):
        result = detect_skills("I enjoy hiking and painting.")
        self.assertEqual(result, set())

    def test_js_alias_detected_as_javascript(self):
        result = detect_skills("I know JS very well.")
        self.assertIn("javascript", result)
        self.assertNotIn("js", result)

    def test_mysql_alias_detected_as_sql(self):
        result = detect_skills("Experience with MySQL databases.")
        self.assertIn("sql", result)

    def test_html5_alias_detected_as_html(self):
        result = detect_skills("Built pages using HTML5.")
        self.assertIn("html", result)

    def test_css3_alias_detected_as_css(self):
        result = detect_skills("Styled with CSS3.")
        self.assertIn("css", result)

    def test_ml_alias_detected_as_machine_learning(self):
        result = detect_skills("Some ML experience preferred.")
        self.assertIn("machine learning", result)

    def test_js_and_javascript_together_count_once(self):
        result = detect_skills("I know js and javascript.")
        self.assertEqual(result, {"javascript"})


class TestMatchSkills(unittest.TestCase):
    def test_matched_and_missing(self):
        student = {"python", "sql"}
        required = {"python", "flask", "docker"}
        matched, missing = match_skills(student, required)
        self.assertEqual(matched, {"python"})
        self.assertEqual(missing, {"flask", "docker"})


class TestCalculateMatchPercentage(unittest.TestCase):
    def test_normal_case(self):
        matched = {"python"}
        required = {"python", "flask"}
        self.assertEqual(calculate_match_percentage(matched, required), 50.0)

    def test_full_match(self):
        matched = {"python", "flask"}
        required = {"python", "flask"}
        self.assertEqual(calculate_match_percentage(matched, required), 100.0)

    def test_zero_required_skills_returns_none(self):
        self.assertIsNone(calculate_match_percentage(set(), set()))


class TestGeneratePreparationChecklist(unittest.TestCase):
    def test_returns_tip_for_known_skill(self):
        checklist = generate_preparation_checklist({"docker"})
        self.assertEqual(len(checklist), 1)
        self.assertIn("Docker", checklist[0])

    def test_empty_missing_skills_returns_empty_checklist(self):
        self.assertEqual(generate_preparation_checklist(set()), [])

    def test_checklist_is_alphabetically_sorted(self):
        checklist = generate_preparation_checklist({"python", "aws", "git"})
        self.assertIn("AWS", checklist[0])
        self.assertIn("Python", checklist[-1])

    def test_unknown_skill_falls_back_to_generic_tip(self):
        custom_tips = {"python": "Practice Python."}
        checklist = generate_preparation_checklist({"rust"}, tips=custom_tips)
        self.assertEqual(
            checklist,
            ["Learn the basics of rust through a short project or tutorial."],
        )


class TestAnalyzeSkillMatch(unittest.TestCase):
    def test_full_pipeline(self):
        student_text = "I know Python, SQL, and Flask."
        job_text = "Looking for someone with Python and Docker experience."
        result = analyze_skill_match(student_text, job_text)

        self.assertEqual(result["matched_skills"], ["python"])
        self.assertEqual(result["missing_skills"], ["docker"])
        self.assertEqual(result["match_percentage"], 50.0)
        self.assertIsNone(result["message"])
        self.assertEqual(len(result["checklist"]), 1)

    def test_no_required_skills_detected(self):
        student_text = "I know Python."
        job_text = "We are a friendly team looking for a great attitude."
        result = analyze_skill_match(student_text, job_text)

        self.assertEqual(result["required_skills"], [])
        self.assertIsNone(result["match_percentage"])
        self.assertIsNotNone(result["message"])


if __name__ == "__main__":
    unittest.main()