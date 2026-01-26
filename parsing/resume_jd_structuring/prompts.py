RESUME_EXTRACTION_PROMPT = """
IMPORTANT: Output MUST be strict JSON. No markdown. No comments. No text outside JSON.

You are an ATS-grade resume parser.

Extract the following information from the resume text.
Return ONLY valid JSON. Do not add explanations.

JSON SCHEMA:
{{
  "name": string | null,
  "summary": string | null,
  "skills": [string],
  "education": [string],
  "experience": [
    {{
      "role": string,
      "company": string,
      "duration": string,
      "description": string
    }}
  ],
  "projects": [string]
}}

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"
"""

JD_EXTRACTION_PROMPT = """
IMPORTANT: Output MUST be strict JSON. No markdown. No comments. No text outside JSON.

You are an ATS-grade job description parser.

Extract structured information from the job description.
Return ONLY valid JSON. Do not add explanations.

JSON SCHEMA:
{{
  "job_title": string,
  "required_skills": [string],
  "preferred_skills": [string],
  "responsibilities": [string],
  "requirements": [string],
  "experience_level": string | null
}}

JOB DESCRIPTION TEXT:
\"\"\"
{jd_text}
\"\"\"
"""

