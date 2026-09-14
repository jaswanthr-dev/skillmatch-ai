CREATE DATABASE IF NOT EXISTS skillmatch_db;
USE skillmatch_db;

CREATE TABLE IF NOT EXISTS analyses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_skills TEXT NOT NULL,
    internship_description TEXT NOT NULL,
    detected_student_skills JSON NOT NULL,
    detected_required_skills JSON NOT NULL,
    matched_skills JSON NOT NULL,
    missing_skills JSON NOT NULL,
    match_percentage DECIMAL(5,2) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);