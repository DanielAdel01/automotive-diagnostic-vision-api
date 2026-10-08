import os
import tempfile
import whisper

from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from TTS.api import TTS


router = APIRouter(
    prefix="/speech",
    tags=["speech"]
)

tts_model = TTS(
    model_name="tts_models/en/ljspeech/tacotron2-DDC"
)


# tiny — chosen in Day 21 based on measured evidence
model = whisper.load_model("tiny")


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        temp.write(audio_bytes)
        temp_path = temp.name

    try:
        result = model.transcribe(temp_path)
    finally:
        os.remove(temp_path)

    return {
        "language": result["language"],
        "text": result["text"]
    }

@router.post("/speak")
def speak(text: str):
    """
    Convert text to speech and return a WAV audio response.
    """

    # Create a unique temporary WAV file.
    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )
    output_path = temp_file.name
    temp_file.close()

    try:
        # Generate speech and save it to the temporary file.
        tts_model.tts_to_file(
            text=text,
            file_path=output_path
        )

        # Read the generated WAV file as binary data.
        with open(output_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        # Return the audio data as a WAV response.
        return Response(
            content=audio_bytes,
            media_type="audio/wav"
        )

    finally:
        # Remove the temporary file after processing.
        if os.path.exists(output_path):
            os.remove(output_path)
