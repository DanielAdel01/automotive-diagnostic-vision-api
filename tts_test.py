from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

tts.tts_to_file(
    text="Diagnostic Trouble Code P0301 detected. Engine speed is approximately 6200 revolutions per minute.",
    file_path="output.wav"
)

print("Speech generated successfully: output.wav")

