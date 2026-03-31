# ============================================================================
# Audio Generator Container
# Supports: MusicGen, AudioGen, Chatterbox TTS, Bark
# ============================================================================

# ---- Base stage: CUDA runtime + system deps ----
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1

# System dependencies for audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
        software-properties-common \
        gpg-agent \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-venv \
        python3.12-dev \
        # Audio libraries
        libsndfile1 \
        ffmpeg \
        sox \
        libsox-dev \
        espeak-ng \
        # General
        curl \
        ca-certificates \
        git \
    && ln -sf /usr/bin/python3.12 /usr/bin/python3 \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# ---- Dependencies stage: install Python packages ----
FROM base AS deps

WORKDIR /app

# Install PyTorch first (large, rarely changes)
RUN uv pip install --system --no-cache \
    torch torchaudio --index-url https://download.pytorch.org/whl/cu124

# Install project dependencies
COPY pyproject.toml README.md ./
RUN uv pip install --system --no-cache -e "."

# ---- Final stage: copy application code ----
FROM deps AS final

WORKDIR /app

# Copy application source
COPY src/ ./src/

# Re-install in editable mode with source present
RUN uv pip install --system --no-cache --no-deps -e .

# Default directories for mounted volumes
RUN mkdir -p /models /app/outputs /app/checkpoints

# Environment defaults
ENV AUDIOGEN_MODELS_DIR=/models \
    AUDIOGEN_OUTPUTS_DIR=/app/outputs \
    AUDIOGEN_TRAINED_MODELS_DIR=/app/checkpoints \
    HF_HOME=/models/huggingface \
    TORCH_HOME=/models/torch \
    GRADIO_SERVER_NAME=0.0.0.0

EXPOSE 8000

ENTRYPOINT ["audiogen"]
CMD ["serve"]
