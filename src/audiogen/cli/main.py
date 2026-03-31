from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(
    name="audiogen",
    help="Generate music, voice, and sound effects from the command line.",
    no_args_is_help=True,
)


def _run_async(coro):
    """Run an async function synchronously."""
    return asyncio.get_event_loop().run_until_complete(coro)


def _init_local():
    """Initialize the engine stack for local (non-API) mode."""
    from audiogen.api.dependencies import set_file_manager, set_model_manager
    from audiogen.config import get_settings
    from audiogen.core.file_manager import FileManager
    from audiogen.core.model_manager import ModelManager
    from audiogen.engines.audiogen import AudioGenEngine
    from audiogen.engines.bark import BarkEngine
    from audiogen.engines.chatterbox import ChatterboxEngine
    from audiogen.engines.musicgen import MusicGenEngine

    settings = get_settings()
    for d in (settings.models_dir, settings.outputs_dir, settings.trained_models_dir):
        Path(d).mkdir(parents=True, exist_ok=True)

    mgr = ModelManager(settings)
    mgr.register_engine(MusicGenEngine())
    mgr.register_engine(AudioGenEngine())
    mgr.register_engine(ChatterboxEngine())
    mgr.register_engine(BarkEngine())
    set_model_manager(mgr)
    set_file_manager(FileManager(settings))
    return mgr


def _remote_generate(api_url: str, endpoint: str, data: dict, files: dict | None = None):
    """Call the remote API for generation."""
    import httpx

    url = f"{api_url}/api/v1/{endpoint}"
    with httpx.Client(timeout=300) as client:
        resp = client.post(url, data=data, files=files)
        resp.raise_for_status()
        return resp.json()


# ── Music ───────────────────────────────────────────────────────


@app.command()
def music(
    prompt: str = typer.Argument(..., help="Text description of the music"),
    duration: float = typer.Option(10.0, "--duration", "-d", help="Duration in seconds"),
    model_size: str = typer.Option("small", "--model", "-m", help="small/medium/large/melody"),
    temperature: float = typer.Option(1.0, "--temperature", "-t"),
    top_k: int = typer.Option(250, "--top-k"),
    top_p: float = typer.Option(0.0, "--top-p"),
    cfg_coef: float = typer.Option(3.0, "--cfg"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    output_format: str = typer.Option("wav", "--format", "-f"),
    api_url: Optional[str] = typer.Option(None, "--api-url", help="Remote API URL"),
):
    """Generate music from a text prompt."""
    if api_url:
        result = _remote_generate(api_url, "music/generate", {
            "prompt": prompt,
            "duration_seconds": duration,
            "model_size": model_size,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "cfg_coef": cfg_coef,
            "output_format": output_format,
        })
        typer.echo(json.dumps(result, indent=2))
        return

    mgr = _init_local()

    async def run():
        engine = await mgr.load_engine("musicgen")
        return await engine.generate(
            prompt=prompt,
            duration_seconds=duration,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            cfg_coef=cfg_coef,
            output_format=output_format,
        )

    result = _run_async(run())

    if output:
        import shutil
        shutil.copy2(result.audio_path, output)
        typer.echo(f"Saved to {output}")
    else:
        typer.echo(f"Generated: {result.audio_path}")
    typer.echo(f"Duration: {result.duration_seconds}s | Time: {result.generation_time_seconds}s")


# ── Voice ───────────────────────────────────────────────────────


@app.command()
def voice(
    text: str = typer.Argument(..., help="Text to synthesize"),
    engine: str = typer.Option("chatterbox", "--engine", "-e", help="chatterbox or bark"),
    reference: Optional[str] = typer.Option(None, "--reference", "-r", help="Reference audio for voice cloning"),
    exaggeration: float = typer.Option(0.5, "--exaggeration", help="Emotion intensity (Chatterbox)"),
    cfg_weight: float = typer.Option(0.5, "--cfg-weight"),
    temperature: float = typer.Option(0.8, "--temperature", "-t"),
    speaker_preset: Optional[str] = typer.Option(None, "--preset", "-p", help="Bark speaker preset"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    output_format: str = typer.Option("wav", "--format", "-f"),
    api_url: Optional[str] = typer.Option(None, "--api-url"),
):
    """Generate speech from text."""
    if api_url:
        data = {
            "text": text,
            "engine": engine,
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight,
            "temperature": temperature,
            "output_format": output_format,
        }
        if speaker_preset:
            data["speaker_preset"] = speaker_preset
        files = None
        if reference:
            files = {"reference_audio": open(reference, "rb")}
        result = _remote_generate(api_url, "voice/generate", data, files)
        typer.echo(json.dumps(result, indent=2))
        return

    mgr = _init_local()

    async def run():
        audio_engine = await mgr.load_engine(engine)
        if engine == "chatterbox":
            return await audio_engine.generate(
                text=text,
                reference_audio=reference,
                exaggeration=exaggeration,
                cfg_weight=cfg_weight,
                temperature=temperature,
                output_format=output_format,
            )
        else:
            return await audio_engine.generate(
                text=text,
                speaker_preset=speaker_preset,
                output_format=output_format,
            )

    result = _run_async(run())

    if output:
        import shutil
        shutil.copy2(result.audio_path, output)
        typer.echo(f"Saved to {output}")
    else:
        typer.echo(f"Generated: {result.audio_path}")
    typer.echo(f"Duration: {result.duration_seconds}s | Time: {result.generation_time_seconds}s")


# ── Sound Effects ───────────────────────────────────────────────


@app.command()
def sfx(
    prompt: str = typer.Argument(..., help="Text description of the sound effect"),
    duration: float = typer.Option(10.0, "--duration", "-d"),
    temperature: float = typer.Option(1.0, "--temperature", "-t"),
    top_k: int = typer.Option(250, "--top-k"),
    top_p: float = typer.Option(0.0, "--top-p"),
    cfg_coef: float = typer.Option(3.0, "--cfg"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    output_format: str = typer.Option("wav", "--format", "-f"),
    api_url: Optional[str] = typer.Option(None, "--api-url"),
):
    """Generate sound effects from a text prompt."""
    if api_url:
        result = _remote_generate(api_url, "sfx/generate", {
            "prompt": prompt,
            "duration_seconds": duration,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "cfg_coef": cfg_coef,
            "output_format": output_format,
        })
        typer.echo(json.dumps(result, indent=2))
        return

    mgr = _init_local()

    async def run():
        engine = await mgr.load_engine("audiogen")
        return await engine.generate(
            prompt=prompt,
            duration_seconds=duration,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            cfg_coef=cfg_coef,
            output_format=output_format,
        )

    result = _run_async(run())

    if output:
        import shutil
        shutil.copy2(result.audio_path, output)
        typer.echo(f"Saved to {output}")
    else:
        typer.echo(f"Generated: {result.audio_path}")
    typer.echo(f"Duration: {result.duration_seconds}s | Time: {result.generation_time_seconds}s")


# ── Models ──────────────────────────────────────────────────────


models_app = typer.Typer(help="Manage audio generation engines.")
app.add_typer(models_app, name="models")


@models_app.command("list")
def models_list(
    api_url: Optional[str] = typer.Option(None, "--api-url"),
):
    """List available engines and their status."""
    if api_url:
        import httpx

        with httpx.Client(timeout=30) as client:
            resp = client.get(f"{api_url}/api/v1/models")
            resp.raise_for_status()
            data = resp.json()
        for e in data["engines"]:
            status = "LOADED" if e["loaded"] else "unloaded"
            typer.echo(f"  {e['name']:15s} {e['type']:8s} {status:10s} {e['required_vram_gb']} GB")
        return

    mgr = _init_local()
    for e in mgr.list_engines():
        status = "LOADED" if e["loaded"] else "unloaded"
        typer.echo(f"  {e['name']:15s} {e['type']:8s} {status:10s} {e['required_vram_gb']} GB")


@models_app.command("checkpoints")
def models_checkpoints():
    """List trained model checkpoints from Audio-Trainer."""
    mgr = _init_local()
    checkpoints = mgr.scan_checkpoints()
    if not checkpoints:
        typer.echo("No checkpoints found.")
        return
    for c in checkpoints:
        typer.echo(f"  {c['name']:30s} {c['format']:12s} {c['size_mb']:8.1f} MB")


# ── Server ──────────────────────────────────────────────────────


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host"),
    port: int = typer.Option(8000, "--port"),
    reload: bool = typer.Option(False, "--reload"),
):
    """Start the API server with web UI."""
    import uvicorn

    uvicorn.run("audiogen.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    app()
