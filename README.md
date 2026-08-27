# Automotive Diagnostic & Vision API

A modular FastAPI backend unifying rule-based automotive fault diagnostics with real-time computer vision inference, built as a portfolio project bridging embedded automotive systems and applied AI.

## What it does

- **Diagnostics engine** - accepts vehicle sensor data (RPM, coolant temperature, battery voltage, DTC) and returns a threshold-based severity assessment and recommendation, driven by real reasoning logic rather than static responses.
- **Computer vision endpoint** - serves a trained ResNet34 traffic sign classifier (43 GTSRB classes, 99.7% validation accuracy) directly through the API, accepting an uploaded image and returning a predicted sign class with confidence.
- **Unified architecture** - both capabilities live behind a single, modular FastAPI app using APIRouter to separate concerns, with Pydantic models enforcing request validation and response shape throughout.

## Architecture

main.py
routers/
  diagnostics.py   # sensor validation, threshold-based fault analysis
  vision.py        # image preprocessing + model inference

The diagnostics endpoint's core logic is isolated into a standalone function (get_ai_recommendation) with a fixed input/output contract - sensor data in, severity + recommendation out. This is deliberate: the same function boundary that runs simple threshold rules today is designed to later host a trained model or LLM call without any change to the API layer, request schema, or response schema above it.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | /diagnostics | Submit sensor + DTC data |
| GET | /diagnostics/{dtc} | Look up DTC info |
| POST | /diagnostics/{dtc}/analysis | Threshold-based fault severity analysis |
| GET | /vision/classes | List all 43 supported traffic sign classes |
| POST | /vision/predict | Upload an image, get a predicted sign class + confidence |

## Notable engineering / debugging

- **Silent native crash in fastai's learn.predict()** - every call crashed the Python process at the OS level with no traceback. Isolated through systematic elimination down to fastai's internal DataLoader.one_batch() batching step on this specific Windows/PyTorch/fastai combination. Fixed by bypassing fastai's DataLoader entirely - building the input tensor manually with torchvision.transforms and running the raw model forward pass directly.
- **Preprocessing mismatch** - the manual pipeline initially assumed generic ImageNet defaults. Root-caused by inspecting the model's actual training pipeline and correcting to the model's real training transform: 128x128 with a resize-then-center-crop method.
- **Class-vocabulary ordering bug** - predictions were confidently wrong despite correct preprocessing. Traced to fastai building its internal class vocabulary in alphabetical order rather than numeric GTSRB order. Fixed by generating the class-name list directly from the model's actual vocabulary.

## Known limitations

- GTSRB does not include a 40 km/h speed limit class. A real 40 km/h sign is predicted as its nearest valid neighbor (60 km/h) at appropriately low confidence.
- The underlying classifier was trained on cropped, front-on photographs of German road signs, and performs less reliably on non-German sign designs, heavily backgrounded photos, and flat vector/clipart artwork.

## Tech stack

Python, FastAPI, Pydantic, PyTorch, fastai, torchvision

## Running locally

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload

Visit http://127.0.0.1:8000/docs for interactive API documentation.

> Note: the trained model file (model/export.pkl) is not included in this repo.
