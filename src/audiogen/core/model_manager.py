from __future__ import annotations

import gc
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import torch

from audiogen.config import Settings

if TYPE_CHECKING:
    from audiogen.core.engine import AudioEngine

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages engine lifecycle: loading, unloading, and swapping models on GPU."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engines: dict[str, AudioEngine] = {}
        self._current_engine: str | None = None

    def register_engine(self, engine: AudioEngine) -> None:
        """Register an engine so it can be loaded on demand."""
        self._engines[engine.name] = engine
        logger.info("Registered engine: %s (%s)", engine.name, engine.engine_type)

    def get_engine(self, name: str) -> AudioEngine:
        """Get a registered engine by name."""
        if name not in self._engines:
            available = ", ".join(self._engines.keys())
            raise KeyError(f"Engine '{name}' not found. Available: {available}")
        return self._engines[name]

    async def load_engine(self, name: str) -> AudioEngine:
        """Load an engine, unloading the current one if different."""
        engine = self.get_engine(name)
        if engine.is_loaded():
            return engine

        # Unload current engine if a different one is loaded
        if self._current_engine and self._current_engine != name:
            await self.unload_current()

        logger.info("Loading engine: %s", name)
        await engine.load()
        self._current_engine = name
        return engine

    async def unload_current(self) -> None:
        """Unload the currently loaded engine and free GPU memory."""
        if not self._current_engine:
            return

        engine = self._engines.get(self._current_engine)
        if engine and engine.is_loaded():
            logger.info("Unloading engine: %s", self._current_engine)
            await engine.unload()

        self._current_engine = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

    async def unload_engine(self, name: str) -> None:
        """Unload a specific engine by name."""
        engine = self.get_engine(name)
        if engine.is_loaded():
            logger.info("Unloading engine: %s", name)
            await engine.unload()
            if self._current_engine == name:
                self._current_engine = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()

    def list_engines(self) -> list[dict]:
        """Return info about all registered engines."""
        result = []
        for name, engine in self._engines.items():
            result.append({
                "name": name,
                "type": engine.engine_type,
                "loaded": engine.is_loaded(),
                "required_vram_gb": engine.required_vram_gb,
            })
        return result

    def get_gpu_info(self) -> dict:
        """Return GPU memory usage info."""
        if not torch.cuda.is_available():
            return {"available": False}
        return {
            "available": True,
            "device_name": torch.cuda.get_device_name(0),
            "memory_allocated_mb": round(torch.cuda.memory_allocated(0) / 1024 / 1024, 1),
            "memory_reserved_mb": round(torch.cuda.memory_reserved(0) / 1024 / 1024, 1),
            "memory_total_mb": round(torch.cuda.get_device_properties(0).total_mem / 1024 / 1024, 1),
        }

    def scan_checkpoints(self) -> list[dict]:
        """Scan the trained models directory for available checkpoints."""
        checkpoints_dir = Path(self._settings.trained_models_dir)
        if not checkpoints_dir.exists():
            return []

        extensions = {".pt", ".pth", ".ckpt", ".safetensors", ".bin"}
        results = []
        for f in sorted(checkpoints_dir.rglob("*")):
            if f.suffix in extensions:
                results.append({
                    "name": f.stem,
                    "path": str(f),
                    "format": f.suffix,
                    "size_mb": round(f.stat().st_size / 1024 / 1024, 1),
                })
        return results
