from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"  # or your model

_tokenizer = None
_model = None


def _load_model():
    global _tokenizer, _model

    if _model is None:
        print("🔵 Loading LLM (one time only)...")

        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

        _model.eval()

    return _tokenizer, _model


def call_llm(prompt: str, temperature: float = 0.0, max_new_tokens: int = 512):
    tokenizer, model = _load_model()

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else None
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
