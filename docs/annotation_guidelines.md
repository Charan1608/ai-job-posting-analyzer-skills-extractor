# Annotation Guidelines

## Project

AI-Powered Job Posting Analyzer & Skills Extractor for Business Analytics Roles Using Generative AI

---

# Purpose

This document defines the annotation rules used to create the Gold Standard Dataset for evaluating AI-based skill extraction.

The goal is to ensure consistency across all manually labelled job postings.

---

# General Principles

Annotate only information that is explicitly mentioned in the job posting.

Do not infer missing information.

Use semicolon (;) to separate multiple values.

Do not use commas.

Leave blank if information is unavailable.

---

# Technical Skills

Include:

Programming languages

Databases

Cloud platforms

Libraries

Frameworks

BI tools

Data engineering tools

Analytics software

Examples

Python

SQL

Power BI

Tableau

Excel

Pandas

NumPy

PySpark

TensorFlow

Azure

AWS

Snowflake

Databricks

Apache Spark

Example Format

Python; SQL; Power BI; Excel

---

# Soft Skills

Examples

Communication

Leadership

Problem Solving

Critical Thinking

Teamwork

Presentation

Stakeholder Management

Time Management

Adaptability

Example Format

Communication; Leadership; Problem Solving

---

# Tools

Include software platforms such as

Git

Jira

Confluence

SAP

Salesforce

Snowflake

Databricks

Power BI Desktop

Azure DevOps

Example Format

Git; Jira; Snowflake

---

# Certifications

Examples

AWS Certified Cloud Practitioner

Microsoft PL-300

Azure Data Engineer Associate

Google Professional Data Engineer

PMP

Scrum Master

Example Format

Microsoft PL-300; AWS Certified Cloud Practitioner

---

# Experience

Allowed values

0-2

3-5

5-7

7-10

10+

Examples

3-5

5-7

---

# Education

Allowed values

Bachelor's

Master's

MBA

PhD

Example

Bachelor's

MBA

---

# Annotator

Use your full name.

Example

Charan N

---

# Review Status

Allowed values

Pending

Reviewed

---

# Comments

Optional notes about ambiguity.

Examples

Mentions SQL indirectly.

Power BI preferred but not mandatory.

---

# Rules

Always preserve original spelling.

Do not normalize skills during annotation.

Do not merge synonyms.

Normalization happens later in the pipeline.

---

# Example

Technical Skills

Python; SQL; Power BI; Excel

Soft Skills

Communication; Problem Solving

Tools

Git; Jira

Certification

Microsoft PL-300

Experience

3-5

Education

Bachelor's

Annotator

Charan N

Review Status

Reviewed

Comments

Clear technical requirements.