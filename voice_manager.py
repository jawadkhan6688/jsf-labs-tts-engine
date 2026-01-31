import os
import uuid
import base64
from utils import validate_audio_bytes, smart_trim_audio

VOICE_DIR = "data/voices"
os.makedirs(VOICE_DIR, exist_ok=True)


def upload_voice(file_base64: str, file_name: str) -> str:
    file_bytes = base64.b64decode(file_base64)

    validate_audio_bytes(file_bytes, file_name)

    voice_id = str(uuid.uuid4())

    temp_path = os.path.join(VOICE_DIR, f"{voice_id}_temp")
    final_path = os.path.join(VOICE_DIR, f"{voice_id}.wav")

    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    smart_trim_audio(temp_path, final_path)

    os.remove(temp_path)

    return voice_id
