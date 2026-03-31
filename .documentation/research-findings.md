# Audio Generator — Research Findings

Project goal: Generate audio — including voice cloning, music, sound effects, foley, and environmental audio — using open-source, locally-runnable tools.

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

## Sound Effects & General Audio

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **Stable Audio Open 1.0** (Stability AI) | Up to 47s SFX/foley/ambient, fine-tunable on custom audio | Open |
| **AudioGen** (Meta AudioCraft) | Text-to-environmental sounds, part of AudioCraft suite | MIT |
| **AudioLDM 2** | Text-to-audio for speech, SFX, and music; style transfer & inpainting | Open |
| **Tango 2** | Text-to-audio with DPO alignment, strong on animal/nature/human sounds | Open |

---

## Foley & Video-Synced Audio

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **HunyuanVideo-Foley** (Tencent) | 48 kHz foley synced to video, SOTA fidelity & alignment | Open |
| **FoleyCrafter** (OpenMMLab) | Video-to-audio with onset-based temporal sync, text-controllable | Open |

---

## Unified Audio Toolkit

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **Amphion** (OpenMMLab) | Single framework for TTS, text-to-audio, singing voice conversion | MIT |

---

## All-in-One

- **TTS-WebUI** — Single Gradio/React UI bundling MusicGen, RVC, Demucs, Stable Audio, and many TTS engines in one local app.

---

## Key Trends

- Most serious tools require a GPU (NVIDIA CUDA preferred, but Mac MPS and AMD ROCm support is growing).
- **Kokoro TTS** is the go-to if you need CPU-only.
- **RVC + GPT-SoVITS** dominate the voice cloning community.
- **ACE-Step** and **DiffRhythm** are the cutting-edge music generation picks for local use.
- **Tango 2** and **Stable Audio Open** are the top picks for local sound effect generation.
- **HunyuanVideo-Foley** leads for video-synced foley.
- **AudioCraft** (Meta) covers both music (MusicGen) and sound effects (AudioGen) in one MIT-licensed suite.
