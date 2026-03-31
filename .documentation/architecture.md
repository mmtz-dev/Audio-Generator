# Audio Generator -- Architecture

## 1. High-Level Architecture

Shows the three user-facing interfaces, the FastAPI application layer, core
services, and the engine implementations that perform actual audio generation.

```mermaid
flowchart TD
    subgraph Interfaces["Interfaces"]
        WebUI["Web UI\n(Gradio at /ui)"]
        API["REST API\n(FastAPI at /api/v1)"]
        CLI["CLI\n(Typer)"]
    end

    subgraph FastAPIApp["FastAPI Application -- main.py"]
        direction TB
        GradioMount["Gradio Mount"]
        Router["API Router"]
        Static["Static Files\n(/outputs)"]
    end

    subgraph Routes["API Route Modules"]
        MusicRoute["music.py"]
        VoiceRoute["voice.py"]
        SFXRoute["sfx.py"]
        ModelsRoute["models.py"]
    end

    subgraph Core["Core Layer"]
        MM["ModelManager\nload/unload engines\nVRAM tracking\ncheckpoint scanning"]
        AE["AudioEngine\n(abstract base)"]
        FM["FileManager\noutput paths & URLs"]
        AU["audio_utils\ntensor-to-wav\nformat conversion\nnormalization"]
    end

    subgraph Engines["Engine Implementations (all extend AudioEngine)"]
        MusicGen["MusicGenEngine\nMeta AudioCraft MusicGen\nMusic -- 32 kHz"]
        AudioGen["AudioGenEngine\nMeta AudioCraft AudioGen\nSFX -- 16 kHz"]
        Chatterbox["ChatterboxEngine\nResemble AI Chatterbox\nVoice + emotion -- 24 kHz"]
        Bark["BarkEngine\nSuno Bark\nVoice + non-verbal -- 24 kHz"]
    end

    WebUI --> GradioMount
    API --> Router
    CLI -->|direct call| MM

    GradioMount --> Router
    Router --> MusicRoute
    Router --> VoiceRoute
    Router --> SFXRoute
    Router --> ModelsRoute

    MusicRoute --> MM
    VoiceRoute --> MM
    SFXRoute --> MM
    ModelsRoute --> MM

    MusicRoute --> FM
    VoiceRoute --> FM
    SFXRoute --> FM

    MM --> AE
    AE --> MusicGen
    AE --> AudioGen
    AE --> Chatterbox
    AE --> Bark

    MusicGen --> AU
    AudioGen --> AU
    Chatterbox --> AU
    Bark --> AU

    FM --> Static
```

## 2. Request Flow

Traces a single generation request (e.g. music) from the moment a user submits
it through the interface, into the API route, through the core layer, into the
engine, and back out as a downloadable audio file.

```mermaid
sequenceDiagram
    actor User
    participant UI as Interface<br/>(Web UI / REST API / CLI)
    participant Route as API Route<br/>(music / voice / sfx)
    participant MM as ModelManager
    participant Engine as AudioEngine<br/>(MusicGen / AudioGen /<br/>Chatterbox / Bark)
    participant AU as audio_utils
    participant FM as FileManager
    participant FS as Filesystem<br/>(/outputs)

    User->>UI: Submit generation request
    UI->>Route: POST /api/v1/{type}/generate
    Route->>MM: get_engine(engine_name)

    alt Engine not loaded
        MM->>MM: Check VRAM budget
        MM->>MM: Unload current engine if needed
        MM->>Engine: load(device, checkpoint?)
        Engine-->>MM: Ready
    end

    MM-->>Route: engine reference

    Route->>Engine: generate(params)
    Engine->>Engine: Run model inference
    Engine->>AU: raw tensor
    AU->>AU: tensor_to_wav / normalize / convert format
    AU-->>Engine: processed audio bytes

    Engine-->>Route: audio result

    Route->>FM: save(audio_bytes, metadata)
    FM->>FS: Write WAV file
    FM-->>Route: file_path + download URL

    Route-->>UI: JSON response (URL, duration, metadata)
    UI-->>User: Audio player / download link
```

## 3. Docker Container Diagram

Shows the single-container deployment, GPU passthrough, and the three volumes
used for model weights, generated outputs, and trained checkpoints from
Audio-Trainer.

```mermaid
flowchart LR
    subgraph Host["Host Machine"]
        GPU["NVIDIA GPU"]
        HostOutputs["./outputs"]
        TrainedDir["TRAINED_MODELS_DIR\n(Audio-Trainer checkpoints)"]
    end

    subgraph Docker["Docker Container -- audiogen"]
        direction TB
        subgraph App["Application (port 8000)"]
            Uvicorn["Uvicorn Server"]
            FastAPI["FastAPI App"]
            Gradio["Gradio UI"]
        end

        subgraph Mounts["Mount Points"]
            Models["/models\n(model-cache volume)\nHF_HOME + TORCH_HOME"]
            Outputs["/app/outputs\n(bind mount)"]
            Checkpoints["/app/checkpoints\n(read-only bind mount)"]
        end

        Uvicorn --> FastAPI
        FastAPI --> Gradio
        FastAPI --> Models
        FastAPI --> Outputs
        FastAPI --> Checkpoints
    end

    subgraph Volumes["Docker Volumes"]
        ModelCache["model-cache\n(named volume)\nPersists model weights\nacross rebuilds"]
    end

    GPU -.->|nvidia driver\nGPU passthrough| Docker
    ModelCache ---|volume mount| Models
    HostOutputs ---|bind mount| Outputs
    TrainedDir ---|read-only bind| Checkpoints
```
