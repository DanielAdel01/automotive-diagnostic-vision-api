import os
import re
import tempfile

from fastapi import APIRouter, UploadFile, File, Response

from routers.speech import model, tts_model
from routers.llm import tokenizer, llm_model


router = APIRouter(
    prefix="/assistant",
    tags=["assistant"]
)


@router.post("/ask")
async def voice_diagnostic_assistant(file: UploadFile = File(...)):
    # 1. Read the uploaded audio.
    audio_bytes = await file.read()

    # 2. Save the audio temporarily so Whisper can process it.
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ) as temp:
        temp.write(audio_bytes)
        temp_path = temp.name

    try:
        # 3. Transcribe the spoken question with Whisper.
        transcription = model.transcribe(temp_path)
    finally:
        # 4. Delete the temporary input audio.
        os.remove(temp_path)

    spoken_text = transcription["text"]

    # 5. Look for a DTC code such as P0301, P0420, or P0171.
    match = re.search(
        r"P0\d{3}",
        spoken_text.upper()
    )

    dtc_code = match.group(0) if match else None

    # 6. Stop if no DTC code was detected.
    if not dtc_code:
        return {
            "error": "No DTC code detected in speech",
            "heard": spoken_text
        }

    # 7. Build the same prompt used by the LLM endpoint.
    prompt = f"Diagnostic Trouble Code {dtc_code} means"

    # 8. Convert the prompt into tokens for the LLM.
    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    # 9. Generate the LLM explanation.
    output = llm_model.generate(
        **inputs,
        max_new_tokens=20
    )

    # 10. Convert the generated tokens back into text.
    explanation = tokenizer.decode(
        output[0],
        skip_special_tokens=True
    )

    # 11. Create a temporary WAV file for TTS.
    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    output_path = temp_file.name
    temp_file.close()

    try:
        # 12. Convert the LLM explanation into speech.
        tts_model.tts_to_file(
            text=explanation,
            file_path=output_path
        )

        # 13. Read the generated WAV file.
        with open(output_path, "rb") as audio_file:
            audio_response = audio_file.read()

        # 14. Return the WAV audio to the client.
        return Response(
            content=audio_response,
            media_type="audio/wav"
        )

    finally:
        # 15. Delete the temporary output file.
        if os.path.exists(output_path):
            os.remove(output_path)
