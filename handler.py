import runpod
import logging
from voice_manager import upload_voice
from tts_engine import synthesize

logging.basicConfig(level=logging.INFO)

MAX_TEXT_LENGTH = 2000
MAX_BASE64_SIZE = 15_000_000  # ~15MB safety


def response(status: int, message: str = None, data=None):
    return {
        "status": status,
        "message": message,
        "data": data
    }


def handler(job):
    try:
        job_input = job.get("input", {})
        action = job_input.get("action")

        if not action:
            return response(400, "Missing action field")

        if action == "upload_voice":
            return handle_upload(job_input)

        elif action == "synthesize":
            return handle_synthesize(job_input)

        else:
            return response(400, "Invalid action")

    except Exception as e:
        logging.exception("Unhandled server error")
        return response(500, "Internal server error")


def handle_upload(job_input):
    file_base64 = job_input.get("file")
    file_name = job_input.get("file_name")

    if not file_base64 or not file_name:
        return response(400, "file and file_name required")

    if len(file_base64) > MAX_BASE64_SIZE:
        return response(400, "File too large")

    try:
        voice_id = upload_voice(file_base64, file_name)
        return response(201, "Voice uploaded", {"voice_id": voice_id})
    except ValueError as e:
        return response(400, str(e))
    except Exception:
        logging.exception("Upload failed")
        return response(500, "Upload failed")


def handle_synthesize(job_input):
    voice_id = job_input.get("voice_id")
