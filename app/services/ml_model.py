import logging
import os
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from app.services.exe_to_asm import disassemble_exe
from app.services.asm_to_image import generate_image_from_asm_text

MODEL_PATH = os.getenv("MODEL_PATH", "resnet.pth")
CLASS_NAMES = ["Benign", "Malware"]
IMAGE_SIZE = 224

_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def _load_model():
    global _model
    if _model is not None:
        return _model

    checkpoint = torch.load(MODEL_PATH, map_location=_device)

    # Support both raw state_dict and wrapped checkpoint {"model_state_dict": ...}
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
        num_classes = checkpoint.get("num_classes", len(CLASS_NAMES))
    else:
        state_dict = checkpoint.get("state_dict", checkpoint) if isinstance(checkpoint, dict) else checkpoint
        num_classes = len(CLASS_NAMES)

    model = models.resnet50(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(state_dict)
    model.to(_device)
    model.eval()
    _model = model
    return _model


class MLModel:

    def disassemble(self, file_path):
        try:
            return disassemble_exe(file_path)
        except Exception as e:
            logging.exception("Disassembly failed: %s", e)
            return ""

    def convert_to_rgb(self, asm):
        try:
            img = generate_image_from_asm_text(asm, ngram=2, save_output=False)
            return np.asarray(img)
        except Exception as e:
            logging.exception("convert_to_rgb failed: %s", e)
            return np.zeros((800, 800, 3), dtype=np.uint8)

    def classify_image(self, image: np.ndarray) -> dict:
        model = _load_model()
        pil_img = Image.fromarray(image.astype(np.uint8), mode="RGB")
        tensor = _transform(pil_img).unsqueeze(0).to(_device)

        with torch.no_grad():
            logits = model(tensor)
            probs = torch.softmax(logits, dim=1)[0]

        class_idx = int(torch.argmax(probs).item())
        probability = float(probs[class_idx].item())
        label = CLASS_NAMES[class_idx] if class_idx < len(CLASS_NAMES) else str(class_idx)
        return {"label": label, "probability": round(probability, 4)}
