# Audio Generator

Generate music, voice, and sound effects using open-source ML models.

## Engines

| Engine | Type | Model | License |
|--------|------|-------|---------|
| MusicGen | Music | AudioCraft (Meta) | MIT |
| AudioGen | Sound Effects | AudioCraft (Meta) | MIT |
| Chatterbox | Voice/TTS | Resemble AI | MIT |
| Bark | Voice/TTS | Suno AI | MIT |

## Quick Start

```bash
# Start the server (API + Web UI)
docker compose up --build

# Web UI: http://localhost:8000/ui
# API docs: http://localhost:8000/docs
```

## CLI Usage

```bash
# Music generation
audiogen music "epic orchestral battle theme" --duration 15 --output battle.wav

# Voice synthesis with emotion
audiogen voice "Hello! Welcome to the show." --engine chatterbox --exaggeration 0.8

# Voice cloning
audiogen voice "Clone this voice" --reference speaker.wav

# Sound effects
audiogen sfx "thunderstorm with heavy rain" --duration 10

# Model management
audiogen models list
audiogen models checkpoints
```

## Development

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Audio-Trainer Integration

Set `TRAINED_MODELS_DIR` to point at your Audio-Trainer checkpoints:

```bash
TRAINED_MODELS_DIR=/path/to/Audio-Trainer/checkpoints docker compose up
```
