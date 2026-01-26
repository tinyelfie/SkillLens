import json
from llm.llm_interface import call_llm
from parsing.resume_jd_structuring.prompts import (
    RESUME_EXTRACTION_PROMPT,
    JD_EXTRACTION_PROMPT,
)


def extract_resume_structure(resume_text: str) -> dict:
    prompt = RESUME_EXTRACTION_PROMPT.format(resume_text=resume_text)
    response = call_llm(prompt, temperature=0.0)

    try:
        return extract_json(response)
    except json.JSONDecodeError:
        raise ValueError("LLM failed to return valid JSON for resume")

def extract_jd_structure(jd_text: str) -> dict:
    prompt = JD_EXTRACTION_PROMPT.format(jd_text=jd_text)
    response = call_llm(prompt, temperature=0.0)

    try:
        return extract_json(response)
    except json.JSONDecodeError:
        raise ValueError("LLM failed to return valid JSON for JD")

import re

import json
import re

def extract_json(text: str) -> dict:
    """
    Robust JSON extraction from LLM output
    """
    # Find first { and last }
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in LLM output")

    json_str = text[start:end + 1]

    # Remove trailing commas (common LLM issue)
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*]", "]", json_str)

    return json.loads(json_str)
