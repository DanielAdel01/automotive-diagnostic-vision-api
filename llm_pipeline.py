
from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")

result = generator(
    "Diagnostic Trouble Code P0301 means",
    max_new_tokens=30
)

print(result)
