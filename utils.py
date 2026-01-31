import magic
from pydub import AudioSegment, silence

MAX_DURATION_MS = 30 * 1000
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg'}


def validate_audio_bytes(file_bytes: bytes, file_name: str):

    ext = file_name.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file extension")

    mime = magic.from_buffer(file_bytes, mime=True)
    if 'audio' not in mime:
        raise ValueError("Invalid file content")


def smart_trim_audio(input_path: str, output_path: str):

    audio = AudioSegment.from_file(input_path)

    audio = audio.set_channels(1).set_frame_rate(24000)

    chunks = silence.split_on_silence(
        audio,
        min_silence_len=700,
        silence_thresh=-40,
        keep_silence=200
    )

    processed = AudioSegment.silent(duration=0)

    for chunk in chunks:
        if len(processed) + len(chunk) > MAX_DURATION_MS:
            remaining = MAX_DURATION_MS - len(processed)
            processed += chunk[:remaining]
            break
        processed += chunk

    if len(processed) > MAX_DURATION_MS:
        processed = processed[:MAX_DURATION_MS]

    processed.export(output_path, format="wav")
