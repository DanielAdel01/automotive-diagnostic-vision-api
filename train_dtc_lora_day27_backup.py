```python
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model

from automotive_dataset import data


MODEL_NAME = "distilgpt2"
MAX_LENGTH = 96

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

dataset = Dataset.from_list(data)


def tokenize_fn(example):
    prompt_ids = tokenizer(
        example["prompt"],
        add_special_tokens=False,
    )["input_ids"]

    completion_ids = tokenizer(
        example["completion"],
        add_special_tokens=False,
    )["input_ids"] + [tokenizer.eos_token_id]

    input_ids = prompt_ids + completion_ids
    labels = [-100] * len(prompt_ids) + completion_ids

    input_ids = input_ids[:MAX_LENGTH]
    labels = labels[:MAX_LENGTH]

    attention_mask = [1] * len(input_ids)

    padding_length = MAX_LENGTH - len(input_ids)

    input_ids += [tokenizer.pad_token_id] * padding_length
    attention_mask += [0] * padding_length
    labels += [-100] * padding_length

    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
    }


tokenized = dataset.map(
    tokenize_fn,
    remove_columns=dataset.column_names,
)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["c_attn"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, config)
model.print_trainable_parameters()

training_args = TrainingArguments(
    output_dir="./lora_dtc_output_v2",
    num_train_epochs=40,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=1,
    learning_rate=3e-4,
    logging_steps=5,
    save_strategy="no",
    report_to="none",
    use_cpu=True,
    seed=42,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        padding=True,
        label_pad_token_id=-100,
        pad_to_multiple_of=None,
    ),
)

trainer.train()

model.save_pretrained("./dtc_lora_adapter_v2")
tokenizer.save_pretrained("./dtc_lora_adapter_v2")

print("LoRA adapter and tokenizer saved to ./dtc_lora_adapter_v2")
```
