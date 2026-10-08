
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

prompt = "Diagnostic Trouble Code P0301 means"

inputs = tokenizer(prompt, return_tensors="pt")

output = model.generate(**inputs, max_new_tokens=30)

result = tokenizer.decode(output[0], skip_special_tokens=True)

print(result)
