from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

router = APIRouter(prefix="/llm", tags=["llm"])


# Load the base model and tokenizer once when the API starts.
base_model = AutoModelForCausalLM.from_pretrained("distilgpt2")
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

# Load the trained V1 LoRA adapter on top of the base model.
llm_model = PeftModel.from_pretrained(
    base_model,
    "./dtc_lora_adapter"
)


class DTCQuery(BaseModel):
    dtc: str


@router.post("/explain")
def explain_dtc(query: DTCQuery):
    prompt = f"Diagnostic Trouble Code {query.dtc} means"

    inputs = tokenizer(prompt, return_tensors="pt")

    output = llm_model.generate(
        **inputs,
        max_new_tokens=20
    )

    text = tokenizer.decode(
        output[0],
        skip_special_tokens=True
    )

    return {
        "dtc": query.dtc,
        "explanation": text,
        "note": (
            "Experimental: fine-tuned on 30 examples, "
            "may not distinguish all DTC codes reliably. "
            "See Day 28 findings."
        )
    }
