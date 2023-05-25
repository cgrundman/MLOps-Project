# Import generic wrappers
from transformers import AutoModel, AutoTokenizer
import torch
import os


# Define the model repo
model_name = "prajjwal1/bert-tiny"

# Download pytorch model
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Transform input tokens
inputs = tokenizer("Hello world!", return_tensors="pt")

# Model apply
outputs = model(**inputs)

os.mkdir('./model')

torch.save(model.state_dict(), './model/pretrained_model')

print("ok")
