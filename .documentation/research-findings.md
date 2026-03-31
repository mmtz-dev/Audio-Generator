# Audio Generator — Research Findings

Project goal: Generate audio including voice cloning and music generation using open-source, locally-runnable tools.

---

## Music Generation

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **ACE-Step 1.5** | Full songs up to 10 min, Mac/AMD/Intel support, <4 GB VRAM | MIT |
| **DiffRhythm** | Vocals + instruments in one pass, ~10 sec generation | Apache 2.0 |
| **MusicGen / AudioCraft** (Meta) | Text + melodic conditioning, well-documented | MIT |
| **YuE / HeartMuLa** | Open-source Suno alternative, runs fully offline | Open |

---

## Text-to-Speech (TTS)

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **Kokoro TTS** | 82M params, runs CPU-only, OpenAI-compatible API | Apache 2.0 |
| **Fish Speech V1.5** | Best multilingual benchmarks | Open |
| **CosyVoice2-0.5B** | ~150 ms streaming latency, conversational use | Open |
| **Chatterbox Turbo** | Clone voice in 5 sec, supports `[laugh]`/`[cough]` tags | MIT |
| **Bark** (Suno) | Laughter, sighs, non-speech sounds built-in | MIT |
| **Coqui XTTS-v2** | 6-sec clip cloning, 17 languages | Non-commercial |

---

## Voice Cloning & Conversion

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **RVC** | Real-time speech-to-speech, popular for AI vocal covers | MIT |
| **GPT-SoVITS** | Train a voice from just 1 minute of audio | MIT |
| **OpenVoice** | Cross-lingual voice style cloning | MIT |
| **Voicebox** | Polished local-first desktop app, 23 languages | Open |

---

## All-in-One

- **TTS-WebUI** — Single Gradio/React UI bundling MusicGen, RVC, Demucs, Stable Audio, and many TTS engines in one local app.

---

## Key Trends

- Most serious tools require a GPU (NVIDIA CUDA preferred, but Mac MPS and AMD ROCm support is growing).
- **Kokoro TTS** is the go-to if you need CPU-only.
- **RVC + GPT-SoVITS** dominate the voice cloning community.
- **ACE-Step** and **DiffRhythm** are the cutting-edge music generation picks for local use.
