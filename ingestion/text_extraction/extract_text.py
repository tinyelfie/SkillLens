import pdfplumber
from docx import Document
import re
from pathlib import Path


# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(file_path: str) -> str:
    text_chunks = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    return "\n".join(text_chunks)


# -----------------------------
# DOCX TEXT EXTRACTION
# -----------------------------
def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


# -----------------------------
# TEXT NORMALIZATION
# -----------------------------
def normalize_text(text: str) -> str:
    # Normalize bullet points
    text = re.sub(r"[•▪◦]", "-", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Restore paragraph structure
    text = re.sub(r"(\n\s*){2,}", "\n\n", text)

    return text.strip()


# -----------------------------
# MAIN INGESTION FUNCTION
# -----------------------------
def ingest_document(file_path: str) -> str:
    file_path = Path(file_path)

    if file_path.suffix.lower() == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

    clean_text = normalize_text(raw_text)
    return clean_text

# -----------------------------
# SIMPLE TEST + SAVE OUTPUTS
# -----------------------------
if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent

    files = {
        "resume": BASE_DIR / "resume.pdf",
        "jd": BASE_DIR / "job_description.pdf"
    }

    for key, file_path in files.items():
        print("\n" + "=" * 60)
        print(f"Extracted text from: {file_path.name}")
        print("=" * 60)

        text = ingest_document(file_path)
        print(text[:2000])  # preview first 2000 characters

        # -----------------------------
        # SAVE OUTPUT (PIPELINE FIX)
        # -----------------------------
        output_file = BASE_DIR / f"{key}_text.txt"
        output_file.write_text(text, encoding="utf-8")

        print(f"\n✅ Saved extracted text to: {output_file}")
