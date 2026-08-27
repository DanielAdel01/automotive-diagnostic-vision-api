from fastapi import APIRouter, UploadFile, File
from fastai.vision.all import load_learner
from PIL import Image
import pathlib
import io
import torch
import torchvision.transforms as T

# Windows fix: fastai models trained on Linux/Colab sometimes store paths
# in a way that breaks on Windows. This line prevents a common load error.
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

router = APIRouter(
    prefix="/vision",
    tags=["vision"]
)

MODEL_PATH = "model/export.pkl"
learn = load_learner(MODEL_PATH)
learn.model.eval()

# Manual preprocessing pipeline — bypasses fastai's DataLoader.one_batch(),
# which crashes on this machine. Matches the model's actual training
# pipeline: Resize (crop method, 128x128) + ImageNet normalization stats,
# confirmed by inspecting learn.dls.after_item and learn.dls.after_batch.
transform = T.Compose([
    T.Resize(146),
    T.CenterCrop(128),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Official GTSRB class names.
# The index corresponds to the original GTSRB numeric class ID.
GTSRB_CLASS_NAMES = [
    "Speed limit (20km/h)",
    "Speed limit (30km/h)",
    "Speed limit (50km/h)",
    "Speed limit (60km/h)",
    "Speed limit (70km/h)",
    "Speed limit (80km/h)",
    "End of speed limit (80km/h)",
    "Speed limit (100km/h)",
    "Speed limit (120km/h)",
    "No passing",
    "No passing for vehicles over 3.5 metric tons",
    "Right-of-way at the next intersection",
    "Priority road",
    "Yield",
    "Stop",
    "No vehicles",
    "Vehicles over 3.5 metric tons prohibited",
    "No entry",
    "General caution",
    "Dangerous curve to the left",
    "Dangerous curve to the right",
    "Double curve",
    "Bumpy road",
    "Slippery road",
    "Road narrows on the right",
    "Road work",
    "Traffic signals",
    "Pedestrians",
    "Children crossing",
    "Bicycles crossing",
    "Beware of ice/snow",
    "Wild animals crossing",
    "End of all speed and passing limits",
    "Turn right ahead",
    "Turn left ahead",
    "Ahead only",
    "Go straight or right",
    "Go straight or left",
    "Keep right",
    "Keep left",
    "Roundabout mandatory",
    "End of no passing",
    "End of no passing by vehicles over 3.5 metric tons"
]

# Fastai sorted the folder names alphabetically.
# Example:
# 0, 1, 10, 11, ..., 19, 2, 20, ..., 9
#
# Rebuild the class list in the exact order used by the trained model.
CLASS_NAMES = [
    GTSRB_CLASS_NAMES[int(class_id)]
    for class_id in learn.dls.vocab
]

@router.get("/classes")
def get_classes():
    return {"count": len(CLASS_NAMES), "classes": CLASS_NAMES}

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = learn.model(tensor)

    probs = torch.softmax(out, dim=1)
    pred_idx = int(torch.argmax(probs))

    return {
        "predicted_class": CLASS_NAMES[pred_idx],
        "confidence": round(float(probs[0][pred_idx]), 4)
    }
