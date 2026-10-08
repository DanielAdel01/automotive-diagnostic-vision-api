from transformers import AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

# Load the pretrained language model.
model = AutoModelForCausalLM.from_pretrained(
    "distilgpt2"
)

# Define the LoRA adapter configuration.
config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)

# Attach the adapters to the model.
peft_model = get_peft_model(
    model,
    config
)

# Display how many parameters can be trained.
peft_model.print_trainable_parameters()

