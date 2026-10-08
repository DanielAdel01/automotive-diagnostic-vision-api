# Automotive Diagnostic & Vision API

A modular FastAPI backend combining rule-based automotive diagnostics, computer vision, speech recognition, text generation, and text-to-speech into one automotive AI portfolio project.

The project was built as a 30-day capstone focused on bridging automotive engineering with applied AI/ML, computer vision, speech processing, and API development.

## What it does

The API provides five major capabilities:

* **Diagnostics engine** - accepts vehicle sensor data such as RPM, coolant temperature, battery voltage, and DTC information, then returns a threshold-based severity assessment and recommendation.
* **Computer vision endpoint** - serves a trained ResNet34 traffic sign classifier covering 43 GTSRB classes with 99.7% validation accuracy.
* **Speech recognition** - uses OpenAI Whisper to convert uploaded automotive speech into text.
* **LLM-based DTC explanation** - uses a DistilGPT-2 model with a LoRA adapter trained on automotive DTC examples.
* **Voice diagnostic assistant** - combines speech recognition, DTC extraction, LLM explanation, and text-to-speech into one end-to-end pipeline.

## Capstone Voice Pipeline

The main capstone endpoint is:

```text
POST /assistant/ask

Audio input
    ↓
Whisper speech recognition
    ↓
Transcribed text
    ↓
DTC code extraction
    ↓
V1 LoRA-adapted LLM
    ↓
DTC explanation
    ↓
Coqui TTS
    ↓
WAV audio response
```

A live end-to-end test was performed using a real spoken automotive diagnostic recording.

The system successfully:

1. received the uploaded audio,
2. transcribed the spoken question,
3. detected DTC `P0301`,
4. generated an explanation with the LoRA-adapted LLM,
5. converted the explanation to speech,
6. returned a WAV response,
7. and produced an audible spoken response.

Example generated response:

> Diagnostic Trouble Code P0301 means the engine is not working properly.

The LLM response is intentionally documented as experimental because its limitations were identified and tested during the fine-tuning stages.

## Architecture

```text
main.py
routers/
  diagnostics.py   # sensor validation + threshold-based fault analysis
  vision.py        # image preprocessing + model inference
  speech.py        # Whisper transcription + Coqui TTS
  llm.py           # DistilGPT-2 + V1 LoRA DTC explanation
  assistant.py     # complete voice diagnostic pipeline

model/
  export.pkl # traffic sign classifier
```

The API uses FastAPI routers to separate each capability while allowing the final assistant endpoint to reuse the already-loaded speech and LLM models.

## Endpoints

| Method | Path                          | Description                                 |
| ------ | ----------------------------- | ------------------------------------------- |
| POST   | `/diagnostics`                | Submit sensor + DTC data                    |
| GET    | `/diagnostics/{dtc}`          | Look up DTC information                     |
| POST   | `/diagnostics/{dtc}/analysis` | Threshold-based fault severity analysis     |
| GET    | `/vision/classes`             | List all 43 supported traffic sign classes  |
| POST   | `/vision/predict`             | Upload an image and predict a traffic sign  |
| POST   | `/speech/transcribe`          | Transcribe uploaded audio with Whisper      |
| POST   | `/speech/speak`               | Convert text into WAV speech with Coqui TTS |
| POST   | `/llm/explain`                | Generate an experimental DTC explanation    |
| POST   | `/assistant/ask`              | Full voice-driven diagnostic pipeline       |

## AI / ML Components

### Computer Vision

* ResNet34
* GTSRB traffic sign dataset
* 43 classes
* 99.7% validation accuracy
* PyTorch / fastai / torchvision
* Custom inference preprocessing matching the training pipeline

### Speech Recognition

* OpenAI Whisper
* `tiny` model selected after benchmarking available Whisper sizes
* Used to transcribe spoken automotive diagnostic questions

### Text Generation

* DistilGPT-2
* LoRA fine-tuning using PEFT
* Automotive DTC dataset containing 30 training examples
* V1 adapter selected for API integration after comparing later experiments

### Text-to-Speech

* Coqui TTS
* Tacotron2-DDC
* Generates WAV responses from the LLM output

## Notable Engineering / Debugging

### Silent native crash in fastai's `learn.predict()`

Every call crashed the Python process at the OS level with no traceback.

The problem was isolated through systematic elimination down to fastai's internal `DataLoader.one_batch()` batching step on the specific Windows/PyTorch/fastai combination.

The final solution bypassed fastai's DataLoader entirely by building the input tensor manually with torchvision transforms and running the raw model forward pass directly.

### Preprocessing mismatch

The initial manual inference pipeline assumed generic ImageNet defaults.

The actual training pipeline was inspected and the preprocessing was corrected to match the trained model:

* resize
* center crop
* 128×128 input
* ImageNet normalization

### Class-vocabulary ordering bug

Predictions were confidently wrong despite correct preprocessing.

The issue was traced to fastai building its internal class vocabulary in alphabetical order rather than the required numeric GTSRB ordering.

The class-name mapping was corrected using the model's actual vocabulary.

### LoRA fine-tuning limitation

The DTC dataset contained only 30 examples.

Multiple LoRA experiments were performed with different adapter settings and training configurations.

Later experiments did not reliably distinguish between different DTC codes, so the first V1 adapter was retained for API integration and the limitation was documented instead of hiding the poor generalization.

This is an experimental component rather than a production-grade diagnostic reasoning model.

## Known Limitations

* The LLM is experimental and may produce the same generic explanation for different DTC codes.
* The LoRA training dataset contains only 30 examples, so generalization is limited.
* The voice assistant uses a simple regular expression to identify DTC codes in transcribed speech.
* Whisper transcription quality depends on audio quality, pronunciation, and background noise.
* GTSRB does not include a 40 km/h speed-limit class. A real 40 km/h sign is therefore predicted as the nearest valid class.
* The traffic sign classifier was trained on cropped, front-on photographs of German road signs and performs less reliably on non-German sign designs, heavily backgrounded photos, and flat vector artwork.

## Tech Stack

* Python
* FastAPI
* Pydantic
* PyTorch
* fastai
* torchvision
* Transformers
* PEFT / LoRA
* Whisper
* Coqui TTS
* Uvicorn
* OpenCV / PIL-based image processing

## Running Locally

Create and activate the Python environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
python -m uvicorn main:app --reload
```

The interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Example Voice Assistant Test

From the project directory:

```bash
curl -X POST \
  -F "file=@automotive_test.mp3" \
  http://127.0.0.1:8000/assistant/ask \
  --output assistant_response.wav
```

The returned `assistant_response.wav` contains the spoken response generated by the complete pipeline.

## Project Outcome

This project progressed from separate automotive AI experiments into a single integrated FastAPI system.

The final capstone demonstrates:

```text
Automotive data
     +
Computer vision
     +
Speech recognition
     +
LLM inference
     +
Text-to-speech
     ↓
Integrated automotive AI API
```

The project intentionally documents both successful engineering work and model limitations discovered during development.

> Note: the trained traffic-sign model file (`model/export.pkl`) and other large model artifacts are not included in this repository.

