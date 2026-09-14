"""
test_validation.py

Tests the home page's form validation.
Run with: python -m unittest test_validation.py -v
"""

import unittest
from app import app


class TestFormValidation(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_empty_both_fields_shows_error(self):
        response = self.client.post("/", data={"student_skills": "", "job_description": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please fill in both", response.data)

    def test_empty_student_skills_shows_error(self):
        response = self.client.post("/", data={"student_skills": "", "job_description": "Needs Python"})
        self.assertIn(b"Please fill in both", response.data)

    def test_empty_job_description_shows_error(self):
        response = self.client.post("/", data={"student_skills": "Python, SQL", "job_description": ""})
        self.assertIn(b"Please fill in both", response.data)

    def test_whitespace_only_counts_as_empty(self):
        response = self.client.post("/", data={"student_skills": "   ", "job_description": "   "})
        self.assertIn(b"Please fill in both", response.data)

    def test_get_request_shows_form_without_error(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Please fill in both", response.data)


if __name__ == "__main__":
    unittest.main()