from transformers import pipeline

# Load the pretrained text-generation model.
generator = pipeline(
    "text-generation",
    model="distilgpt2"
)

# Give the model examples and ask it to continue the pattern.
prompt = """Explain each diagnostic trouble code in plain language.

P0301: Cylinder 1 misfire detected. One cylinder is not firing properly.
P0420: Catalyst efficiency below threshold. The catalytic converter may be failing.
P0171:"""

# Generate up to 30 new tokens.
result = generator(
    prompt,
    max_new_tokens=30
)

# Print the complete prompt and generated text.
print(result[0]["generated_text"])
