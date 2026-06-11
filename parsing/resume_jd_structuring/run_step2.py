import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from extractor import extract_resume_structure, extract_jd_structure

# Read raw text produced by Step 1
BASE_DIR = PROJECT_ROOT / "ingestion" / "text_extraction"

with open(BASE_DIR / "resume_text.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

with open(BASE_DIR / "jd_text.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

resume_structured = extract_resume_structure(resume_text)
jd_structured = extract_jd_structure(jd_text)

print("\n=== STRUCTURED RESUME ===")
print(json.dumps(resume_structured, indent=2))

print("\n=== STRUCTURED JOB DESCRIPTION ===")
print(json.dumps(jd_structured, indent=2))

# Save outputs for Steps 3–8
OUTPUT_DIR = PROJECT_ROOT / "embeddings" / "domain_embeddings"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

resume_out = OUTPUT_DIR / "resume_structured.json"
jd_out = OUTPUT_DIR / "jd_structured.json"

with open(resume_out, "w", encoding="utf-8") as f:
    json.dump(resume_structured, f, indent=2)

with open(jd_out, "w", encoding="utf-8") as f:
    json.dump(jd_structured, f, indent=2)

print(f"\n✅ Saved resume_structured.json → {resume_out}")
print(f"✅ Saved jd_structured.json     → {jd_out}")
