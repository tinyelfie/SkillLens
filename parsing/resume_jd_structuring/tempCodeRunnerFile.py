from extractor import extract_resume_structure, extract_jd_structure

# Replace with output from Step 1
with open("resume_text.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

with open("jd_text.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()


resume_structured = extract_resume_structure(resume_text)
jd_structured = extract_jd_structure(jd_text)

print("\n=== STRUCTURED RESUME ===")
print(resume_structured)

print("\n=== STRUCTURED JOB DESCRIPTION ===")
print(jd_structured)
