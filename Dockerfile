FROM pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime

USER root
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    sox \
    libsndfile1 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Clone F5-TTS
RUN git clone https://github.com/SWivid/F5-TTS.git \
    && cd F5-TTS \
    && git submodule update --init --recursive \
    && pip install -e . --no-cache-dir

# Install serverless dependencies
RUN pip install runpod pydub python-magic

# Copy your production serverless files
COPY handler.py /workspace/F5-TTS/
COPY voice_manager.py /workspace/F5-TTS/
COPY tts_engine.py /workspace/F5-TTS/
COPY utils.py /workspace/F5-TTS/
COPY demo_speaker0.mp3 /workspace/F5-TTS/

WORKDIR /workspace/F5-TTS

ENV PYTHONUNBUFFERED=1

CMD ["python", "handler.py"]
