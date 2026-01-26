from llm.llm_interface import call_llm

JUDGE_PROMPT = """
You are an impartial resume evaluator.

Given:
- Original resume evidence
- Rewritten resume
- Job description

Answer ONLY in JSON:

{
  "alignment_improved": true/false,
  "hallucination_detected": true/false,
  "confidence": 0.0-1.0
}
"""
def llm_judge(original_resume, rewritten_resume, jd_text):
    prompt = f"""
{JUDGE_PROMPT}

ORIGINAL RESUME:
{original_resume}

REWRITTEN RESUME:
{rewritten_resume}

JOB DESCRIPTION:
{jd_text}
"""
    return call_llm(
        prompt,
        temperature=0.0,
        max_new_tokens=300
    )

import re

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("No JSON found in LLM output")
    return json.loads(match.group())
