# AI-Powered Job Posting Analyzer & Skills Extractor

### Generative AI • NLP • ESCO Skill Normalization • Machine Learning • Business Analytics

An end-to-end **AI-powered Business Analytics project** that transforms unstructured job postings into structured job-role and skill intelligence.

The system combines **Generative AI-based skill extraction, structured JSON validation, skill normalization, ESCO taxonomy mapping, custom Business Analytics taxonomies, feature engineering, Machine Learning-based role classification, evaluation, explainable analytics, skill-gap analysis, and Power BI visualization**.

The project is designed to analyze job postings and answer practical questions such as:

- What skills are employers demanding?
- Which technical and analytical skills appear most frequently?
- How can different names for the same skill be standardized?
- Which skills are associated with different job roles?
- Which role best matches a job posting?
- What skills are important for Business Analytics careers?
- Where do skill gaps exist between job requirements and candidate capabilities?

---

## 📌 Project at a Glance

| Component | Implementation |
|---|---|
| Domain | Business Analytics / Recruitment Analytics |
| AI | Generative AI-based skill extraction |
| LLM Provider | Groq |
| NLP Task | Job-posting skill extraction |
| Validation | Structured JSON / schema validation |
| Skill Normalization | Exact, fuzzy, semantic and dictionary-based matching |
| Standard Taxonomy | ESCO |
| Custom Taxonomy | Business Analytics and technology dictionaries |
| Machine Learning | Job-role classification |
| Evaluation | Extraction, normalization and ML evaluation |
| Explainability | Feature importance and explainable analytics |
| Visualization | Python visualizations + Power BI |
| Application | Python application layer |
| Database | SQLite |
| Version Control | Git / GitHub |

---

# 🎯 Core Project Pipeline

```text
                    JOB POSTING
                         │
                         ▼
                DATA INGESTION
                         │
                         ▼
              DATA QUALITY & CLEANING
                         │
                         ▼
             EXPLORATORY DATA ANALYSIS
                         │
                         ▼
              GENERATIVE AI EXTRACTION
                         │
                         ▼
               JSON SCHEMA VALIDATION
                         │
                         ▼
                 SKILL CLEANING
                         │
                         ▼
              SKILL NORMALIZATION
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           EXACT      FUZZY      SEMANTIC
           MATCH      MATCH       MATCH
              │          │          │
              └──────────┼──────────┘
                         ▼
                CUSTOM TAXONOMIES
                         │
                         ▼
                  ESCO MAPPING
                         │
                         ▼
               NORMALIZED SKILLS
                         │
                         ▼
              FEATURE ENGINEERING
                         │
                         ▼
             ML ROLE CLASSIFICATION
                         │
                         ▼
          MODEL EVALUATION & COMPARISON
                         │
                         ▼
              ERROR / MISCLASSIFICATION
                       ANALYSIS
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           POWER BI   APPLICATION   CAREER
          DASHBOARD     LAYER      INSIGHTS

          ---

# 📂 Dataset & Data Pipeline

The project follows a structured data-processing pipeline that converts job-posting data into analysis-ready and machine-learning-ready datasets.

```text
Raw Job Posting Data
        ↓
Dataset Audit
        ↓
Dataset Profiling
        ↓
Data Quality Analysis
        ↓
Data Cleaning
        ↓
Role Discovery & Filtering
        ↓
Exploratory Data Analysis
        ↓
AI Skill Extraction
        ↓
Ground-Truth Evaluation
        ↓
Skill Normalization
        ↓
Feature Engineering
        ↓
Machine Learning Dataset
        ↓
Model Training & Evaluation
        ↓
Business Intelligence
---

# 🤖 Feature Engineering & Machine Learning

After skill extraction and normalization, the project converts structured job-posting information into Machine Learning-ready features.

The Machine Learning layer focuses primarily on **job-role classification** and supporting analytical interpretation.

---

## 🧩 Feature Engineering

Feature engineering components are maintained under:

```text
src/features/
---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Charan1608/ai-job-posting-analyzer-skills-extractor.git
cd ai-job-posting-analyzer-skills-extractor



