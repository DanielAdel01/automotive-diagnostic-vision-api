
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


MODEL_NAME = "distilgpt2"
ADAPTER_PATH = "./dtc_lora_adapter_v3"

tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH)
tokenizer.pad_token = tokenizer.eos_token

base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
fine_tuned = PeftModel.from_pretrained(
    AutoModelForCausalLM.from_pretrained(MODEL_NAME),
    ADAPTER_PATH,
)

base_model.eval()
fine_tuned.eval()

tests = [
    "Diagnostic Trouble Code P0301 means",
    "Diagnostic Trouble Code P0420 means",
    "Diagnostic Trouble Code P0171 means",
    "Diagnostic Trouble Code P0401 means",
]


def generate_answer(model, prompt):
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=60,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    return tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )


for prompt in tests:
    print("\n" + "=" * 65)
    print("PROMPT:", prompt)
    print("BASE MODEL:")
    print(generate_answer(base_model, prompt))
    print("FINE-TUNED MODEL:")
    print(generate_answer(fine_tuned, prompt))

