import os
from io import BytesIO
from elevenlabs.client import ElevenLabs

from ..utils.main_functions import load_config
from dotenv import load_dotenv

config = load_config("config.yaml")
load_dotenv()

VOICE = config["speech"]["voice"]
TTS_MODEL = config["speech"]["tts_model"]
ASR_MODEL = config["speech"]["asr_model"]

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise ValueError("ELEVENLABS_API_KEY is missing. Please set it in your .env file.")

# Init  ElevenLabs client
elevenlabs = ElevenLabs(api_key=API_KEY)

def tts_generate(text, voice_id = VOICE, model_id = TTS_MODEL):
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )

    audio_bytes = BytesIO()
    for chunk in audio:
        audio_bytes.write(chunk)
    audio_bytes.seek(0)

    print("TTS audio generated successfully.")
    return audio_bytes.getvalue()

def transcribe_local_file(file_path,
                          model_id=ASR_MODEL,
                          diarize=True,
                          tag_audio_events = True):
    
    with open(file_path, "rb") as f:
        transcription = elevenlabs.speech_to_text.convert(
            file=f,
            model_id=model_id,
            diarize=diarize,
            tag_audio_events=tag_audio_events,
        )

    print(" Transcription:", transcription.text.encode('utf-8', errors='replace').decode('utf-8'))
    return transcription.text



