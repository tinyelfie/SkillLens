import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from extractor import extract_resume_structure, extract_jd_structure

# Replace with output from Step 1
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2] / "ingestion" / "text_extraction"

with open(BASE_DIR / "resume_text.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

with open(BASE_DIR / "jd_text.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()



resume_structured = extract_resume_structure(resume_text)
jd_structured = extract_jd_structure(jd_text)

print("\n=== STRUCTURED RESUME ===")
print(resume_structured)

print("\n=== STRUCTURED JOB DESCRIPTION ===")
print(jd_structured)
