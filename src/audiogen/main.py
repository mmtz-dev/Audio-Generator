from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from audiogen.api.dependencies import set_file_manager, set_model_manager
from audiogen.api.router import api_router
from audiogen.config import get_settings
from audiogen.core.file_manager import FileManager
from audiogen.core.model_manager import ModelManager
from audiogen.engines.audiogen import AudioGenEngine
from audiogen.engines.bark import BarkEngine
from audiogen.engines.chatterbox import ChatterboxEngine
from audiogen.engines.musicgen import MusicGenEngine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    settings = get_settings()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    # Create directories
    for d in (settings.models_dir, settings.outputs_dir, settings.trained_models_dir):
        Path(d).mkdir(parents=True, exist_ok=True)

    # Initialize singletons
    mgr = ModelManager(settings)
    mgr.register_engine(MusicGenEngine())
    mgr.register_engine(AudioGenEngine())
    mgr.register_engine(ChatterboxEngine())
    mgr.register_engine(BarkEngine())
    set_model_manager(mgr)

    file_mgr = FileManager(settings)
    set_file_manager(file_mgr)

    device = settings.get_device()
    logger.info("Audio Generator started — device=%s, outputs=%s", device, settings.outputs_dir)
    logger.info("Registered engines: %s", [e["name"] for e in mgr.list_engines()])

    if settings.trained_models_dir:
        checkpoints = mgr.scan_checkpoints()
        if checkpoints:
            logger.info("Found %d trained checkpoints", len(checkpoints))

    yield

    # Shutdown
    await mgr.unload_current()
    logger.info("Audio Generator shut down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Audio Generator",
        description="Generate music, voice, and sound effects using open-source ML models",
        version="0.1.0",
        lifespan=lifespan,
    )

    # API routes
    app.include_router(api_router)

    # Serve generated audio files
    settings = get_settings()
    outputs_dir = Path(settings.outputs_dir)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/outputs", StaticFiles(directory=str(outputs_dir)), name="outputs")

    # Mount Gradio UI
    try:
        import gradio as gr

        from audiogen.ui.app import create_ui

        gradio_app = create_ui()
        app = gr.mount_gradio_app(app, gradio_app, path="/ui")
        logger.info("Gradio UI mounted at /ui")
    except ImportError:
        logger.warning("Gradio not installed — web UI disabled")

    return app


app = create_app()


def run_server() -> None:
    """Entry point for the audiogen-server command."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "audiogen.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
