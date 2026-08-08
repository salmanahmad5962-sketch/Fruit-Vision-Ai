---
language:
- en
license: apache-2.0
tags:
- vision
- image-classification
- generated_from_trainer
datasets:
- imagefolder
pipeline_tag: image-classification
base_model: microsoft/resnet-50
model-index:
- name: fruits-and-vegetables-detector-36
  results:
  - task:
      type: image-classification
      name: Image Classification
    dataset:
      name: imagefolder
      type: imagefolder
      config: default
      split: train
      args: default
    metrics:
    - type: accuracy
      value: 0.9721
      name: Accuracy
---

# fruits-and-vegetables-detector-36

This model is a fine-tuned version of [microsoft/resnet-50](https://huggingface.co/microsoft/resnet-50).

It achieves the following results on the evaluation set:

- Loss: 0.0014
- Accuracy: 0.9721

## Model description

This Model is a exploration test using the base model resnet-50 from microsoft.

## Intended uses & limitations

This Model was trained with a very small dataset
[kritikseth/fruit-and-vegetable-image-recognition](https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition) that contains only 36 labels

### How to use

Here is how to use this model to classify an image:

```python
import cv2
import torch
import torchvision.transforms as transforms
from transformers import AutoModelForImageClassification
from PIL import Image

# Load the saved model and tokenizer
model = AutoModelForImageClassification.from_pretrained("jazzmacedo/fruits-and-vegetables-detector-36")

# Get the list of labels from the model's configuration
labels = list(model.config.id2label.values())

# Define the preprocessing transformation
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

image_path = "path/to/your/image.jpg"
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(image)  # Convert NumPy array to PIL image
input_tensor = preprocess(pil_image).unsqueeze(0)

# Run the image through the model
outputs = model(input_tensor)

# Get the predicted label index
predicted_idx = torch.argmax(outputs.logits, dim=1).item()

# Get the predicted label text
predicted_label = labels[predicted_idx]

# Print the predicted label
print("Detected label:", predicted_label)
```

## Training and evaluation data

Dataset Source: https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:

- learning_rate: 0.001
- train_batch_size: 32
- eval_batch_size: 32
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 10
