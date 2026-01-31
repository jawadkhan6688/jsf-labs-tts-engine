import os
import uuid
import base64
import torch
from f5_tts.api import F5TTS

VOICE_DIR = "data/voices"
OUTPUT_DIR = "data/outputs"

DEFAULT_REF_FILE = "demo_speaker0.mp3"

os.makedirs(OUTPUT_DIR, exist_ok=True)

device = "cuda:0" if torch.cuda.is_available() else "cpu"

model = F5TTS(
    model="F5TTS_v1_Base",
    device=device,
    ode_method="euler",
    use_ema=True,
)


def synthesize(voice_id: str, text: str, speed: float) -> str:

    # --------------------------
    # Choose reference file
    # --------------------------
    if voice_id:
        ref_path = os.path.join(VOICE_DIR, f"{voice_id}.wav")

        if not os.path.exists(ref_path):
            raise FileNotFoundError("Voice not found")
    else:
        # Use default file
        ref_path = DEFAULT_REF_FILE

        if not os.path.exists(ref_path):
            raise FileNotFoundError("Default reference file missing")

    # Clamp speed
    speed = max(0.8, min(1.3, float(speed)))

    output_path = os.path.join(
        OUTPUT_DIR,
        f"output_{uuid.uuid4()}.wav"
    )

    # Transcribe reference
    ref_text = model.transcribe(ref_path)

    try:
        model.infer(
            ref_file=ref_path,
            ref_text=ref_text,
            gen_text=text,
            speed=speed,
            nfe_step=28,
            cfg_strength=2.2,
            file_wave=output_path
        )
    except Exception:
        if os.path.exists(output_path):
            os.remove(output_path)
        raise

    with open(output_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode()

    os.remove(output_path)

    return audio_base64
