from llm.llm_interface import call_llm
from rewriting.resume_optimiser.rewrite_prompt import REWRITE_PROMPT

def rewrite_resume(resume_context, jd_context):
    prompt = REWRITE_PROMPT.format(
        resume_context=resume_context,
        jd_context=jd_context
    )

    return call_llm(
        prompt,
        temperature=0.2,
        max_new_tokens=600
    )
