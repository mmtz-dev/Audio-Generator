from __future__ import annotations

import logging
from pathlib import Path

import gradio as gr

logger = logging.getLogger(__name__)


def _get_checkpoint_choices() -> list[str]:
    """Scan checkpoints directory for available voice models."""
    from audiogen.api.dependencies import get_model_manager

    try:
        mgr = get_model_manager()
        checkpoints = mgr.scan_checkpoints()
        return [c["name"] for c in checkpoints]
    except RuntimeError:
        return []


def _get_engine_status() -> str:
    """Get formatted engine status for the Models tab."""
    from audiogen.api.dependencies import get_model_manager

    try:
        mgr = get_model_manager()
        engines = mgr.list_engines()
        gpu = mgr.get_gpu_info()

        lines = ["| Engine | Type | Loaded | VRAM Required |"]
        lines.append("|--------|------|--------|---------------|")
        for e in engines:
            status = "Yes" if e["loaded"] else "No"
            lines.append(f"| {e['name']} | {e['type']} | {status} | {e['required_vram_gb']} GB |")

        if gpu.get("available"):
            lines.append("")
            lines.append(f"**GPU:** {gpu['device_name']}")
            lines.append(
                f"**VRAM:** {gpu['memory_allocated_mb']:.0f} MB used / "
                f"{gpu['memory_total_mb']:.0f} MB total"
            )
        else:
            lines.append("\n**GPU:** Not available (running on CPU)")

        return "\n".join(lines)
    except RuntimeError:
        return "Engine manager not initialized"


# ── Generation handlers ─────────────────────────────────────────


async def generate_music(
    prompt: str,
    duration: float,
    model_size: str,
    temperature: float,
    top_k: int,
    top_p: float,
    cfg_coef: float,
    melody_audio: str | None,
):
    from audiogen.api.dependencies import get_model_manager

    mgr = get_model_manager()
    engine = await mgr.load_engine("musicgen")

    gen_kwargs = {
        "prompt": prompt,
        "duration_seconds": duration,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "cfg_coef": cfg_coef,
    }

    if melody_audio:
        import torchaudio

        waveform, sr = torchaudio.load(melody_audio)
        gen_kwargs["melody_audio"] = waveform
        gen_kwargs["melody_sample_rate"] = sr

    result = await engine.generate(**gen_kwargs)
    return str(result.audio_path), f"Generated in {result.generation_time_seconds}s"


async def generate_voice(
    text: str,
    engine_name: str,
    reference_audio: str | None,
    exaggeration: float,
    cfg_weight: float,
    temperature: float,
    speaker_preset: str,
    text_temp: float,
    waveform_temp: float,
):
    from audiogen.api.dependencies import get_model_manager

    mgr = get_model_manager()
    audio_engine = await mgr.load_engine(engine_name)

    if engine_name == "chatterbox":
        gen_kwargs = {
            "text": text,
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight,
            "temperature": temperature,
        }
        if reference_audio:
            gen_kwargs["reference_audio"] = reference_audio
        result = await audio_engine.generate(**gen_kwargs)
    else:
        result = await audio_engine.generate(
            text=text,
            speaker_preset=speaker_preset or None,
            text_temp=text_temp,
            waveform_temp=waveform_temp,
        )

    return str(result.audio_path), f"Generated in {result.generation_time_seconds}s"


async def generate_sfx(
    prompt: str,
    duration: float,
    temperature: float,
    top_k: int,
    top_p: float,
    cfg_coef: float,
):
    from audiogen.api.dependencies import get_model_manager

    mgr = get_model_manager()
    engine = await mgr.load_engine("audiogen")

    result = await engine.generate(
        prompt=prompt,
        duration_seconds=duration,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        cfg_coef=cfg_coef,
    )
    return str(result.audio_path), f"Generated in {result.generation_time_seconds}s"


async def load_engine(engine_name: str):
    from audiogen.api.dependencies import get_model_manager

    mgr = get_model_manager()
    await mgr.load_engine(engine_name)
    return _get_engine_status()


async def unload_engine(engine_name: str):
    from audiogen.api.dependencies import get_model_manager

    mgr = get_model_manager()
    await mgr.unload_engine(engine_name)
    return _get_engine_status()


# ── Gradio UI ───────────────────────────────────────────────────


def create_ui() -> gr.Blocks:
    """Create the Gradio tabbed interface."""
    with gr.Blocks(title="Audio Generator", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# Audio Generator\nGenerate music, voice, and sound effects.")

        with gr.Tabs():
            # ── Music Tab ───────────────────────────────────
            with gr.Tab("Music"):
                with gr.Row():
                    with gr.Column():
                        music_prompt = gr.Textbox(
                            label="Prompt",
                            placeholder="epic orchestral battle theme with drums",
                            lines=3,
                        )
                        music_duration = gr.Slider(1, 60, value=10, step=1, label="Duration (s)")
                        music_model = gr.Dropdown(
                            ["small", "medium", "large", "melody"],
                            value="small",
                            label="Model Size",
                        )
                        with gr.Accordion("Advanced Settings", open=False):
                            music_temp = gr.Slider(0, 2, value=1.0, step=0.1, label="Temperature")
                            music_topk = gr.Slider(0, 1000, value=250, step=10, label="Top-K")
                            music_topp = gr.Slider(0, 1, value=0.0, step=0.05, label="Top-P")
                            music_cfg = gr.Slider(0, 10, value=3.0, step=0.5, label="CFG Scale")
                        music_melody = gr.Audio(label="Melody Conditioning (optional)", type="filepath")
                        music_btn = gr.Button("Generate Music", variant="primary")
                    with gr.Column():
                        music_output = gr.Audio(label="Generated Music")
                        music_status = gr.Textbox(label="Status", interactive=False)

                music_btn.click(
                    fn=generate_music,
                    inputs=[
                        music_prompt, music_duration, music_model,
                        music_temp, music_topk, music_topp, music_cfg, music_melody,
                    ],
                    outputs=[music_output, music_status],
                )

            # ── Voice Tab ───────────────────────────────────
            with gr.Tab("Voice"):
                with gr.Row():
                    with gr.Column():
                        voice_text = gr.Textbox(
                            label="Text",
                            placeholder="Hello! Welcome to the show. [laughs]",
                            lines=3,
                        )
                        voice_engine = gr.Dropdown(
                            ["chatterbox", "bark"],
                            value="chatterbox",
                            label="Engine",
                        )
                        voice_ref = gr.Audio(
                            label="Reference Audio (voice cloning, Chatterbox only)",
                            type="filepath",
                        )

                        with gr.Accordion("Chatterbox Settings", open=True):
                            voice_exag = gr.Slider(
                                0, 2, value=0.5, step=0.05,
                                label="Exaggeration (emotion intensity)",
                            )
                            voice_cfg = gr.Slider(0, 2, value=0.5, step=0.1, label="CFG Weight")
                            voice_temp = gr.Slider(0, 2, value=0.8, step=0.1, label="Temperature")

                        with gr.Accordion("Bark Settings", open=False):
                            voice_preset = gr.Textbox(
                                label="Speaker Preset",
                                placeholder="v2/en_speaker_1",
                            )
                            voice_text_temp = gr.Slider(0, 2, value=0.7, step=0.1, label="Text Temp")
                            voice_wave_temp = gr.Slider(0, 2, value=0.7, step=0.1, label="Waveform Temp")

                        voice_btn = gr.Button("Generate Voice", variant="primary")
                    with gr.Column():
                        voice_output = gr.Audio(label="Generated Speech")
                        voice_status = gr.Textbox(label="Status", interactive=False)

                voice_btn.click(
                    fn=generate_voice,
                    inputs=[
                        voice_text, voice_engine, voice_ref,
                        voice_exag, voice_cfg, voice_temp,
                        voice_preset, voice_text_temp, voice_wave_temp,
                    ],
                    outputs=[voice_output, voice_status],
                )

            # ── SFX Tab ─────────────────────────────────────
            with gr.Tab("Sound Effects"):
                with gr.Row():
                    with gr.Column():
                        sfx_prompt = gr.Textbox(
                            label="Prompt",
                            placeholder="thunderstorm with heavy rain and distant thunder",
                            lines=3,
                        )
                        sfx_duration = gr.Slider(1, 60, value=10, step=1, label="Duration (s)")
                        with gr.Accordion("Advanced Settings", open=False):
                            sfx_temp = gr.Slider(0, 2, value=1.0, step=0.1, label="Temperature")
                            sfx_topk = gr.Slider(0, 1000, value=250, step=10, label="Top-K")
                            sfx_topp = gr.Slider(0, 1, value=0.0, step=0.05, label="Top-P")
                            sfx_cfg = gr.Slider(0, 10, value=3.0, step=0.5, label="CFG Scale")
                        sfx_btn = gr.Button("Generate Sound Effect", variant="primary")
                    with gr.Column():
                        sfx_output = gr.Audio(label="Generated Sound Effect")
                        sfx_status = gr.Textbox(label="Status", interactive=False)

                sfx_btn.click(
                    fn=generate_sfx,
                    inputs=[sfx_prompt, sfx_duration, sfx_temp, sfx_topk, sfx_topp, sfx_cfg],
                    outputs=[sfx_output, sfx_status],
                )

            # ── Models Tab ──────────────────────────────────
            with gr.Tab("Models"):
                model_status_md = gr.Markdown(_get_engine_status())

                with gr.Row():
                    model_select = gr.Dropdown(
                        ["musicgen", "audiogen", "chatterbox", "bark"],
                        label="Engine",
                    )
                    load_btn = gr.Button("Load")
                    unload_btn = gr.Button("Unload")

                load_btn.click(fn=load_engine, inputs=[model_select], outputs=[model_status_md])
                unload_btn.click(fn=unload_engine, inputs=[model_select], outputs=[model_status_md])

    return demo
