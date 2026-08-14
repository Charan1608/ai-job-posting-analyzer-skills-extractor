-- =========================================================
-- AI-Powered Job Posting Analyzer Database Schema
-- =========================================================

CREATE TABLE IF NOT EXISTS analysis_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    predicted_role TEXT,

    confidence REAL,

    education TEXT,

    experience TEXT,

    technical_skills TEXT,

    normalized_skills TEXT,

    tools TEXT,

    soft_skills TEXT,

    certifications TEXT,

    skill_gap TEXT
);