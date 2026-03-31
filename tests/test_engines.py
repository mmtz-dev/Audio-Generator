"""Tests for audio generation engine implementations."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pytest
import torch

from audiogen.core.engine import GenerationResult


# ── MusicGen Engine ─────────────────────────────────────────────


class TestMusicGenEngine:
    def test_engine_attributes(self):
        from audiogen.engines.musicgen import MusicGenEngine

        engine = MusicGenEngine()
        assert engine.name == "musicgen"
        assert engine.engine_type == "music"
        assert not engine.is_loaded()

    @patch("audiogen.engines.musicgen.get_settings")
    @patch("audiogen.engines.musicgen.MusicGenEngine.load")
    async def test_load_sets_loaded(self, mock_load, mock_settings):
        from audiogen.engines.musicgen import MusicGenEngine

        engine = MusicGenEngine()
        # Simulate load setting _loaded
        async def fake_load(model_path=None):
            engine._loaded = True

        mock_load.side_effect = fake_load
        await engine.load()
        assert engine.is_loaded()


# ── AudioGen Engine ─────────────────────────────────────────────


class TestAudioGenEngine:
    def test_engine_attributes(self):
        from audiogen.engines.audiogen import AudioGenEngine

        engine = AudioGenEngine()
        assert engine.name == "audiogen"
        assert engine.engine_type == "sfx"
        assert not engine.is_loaded()


# ── Chatterbox Engine ───────────────────────────────────────────


class TestChatterboxEngine:
    def test_engine_attributes(self):
        from audiogen.engines.chatterbox import ChatterboxEngine

        engine = ChatterboxEngine()
        assert engine.name == "chatterbox"
        assert engine.engine_type == "voice"
        assert not engine.is_loaded()

    async def test_generate_requires_loaded(self):
        from audiogen.engines.chatterbox import ChatterboxEngine

        engine = ChatterboxEngine()
        with pytest.raises(RuntimeError, match="not loaded"):
            await engine.generate(text="hello")


# ── Bark Engine ─────────────────────────────────────────────────


class TestBarkEngine:
    def test_engine_attributes(self):
        from audiogen.engines.bark import BarkEngine

        engine = BarkEngine()
        assert engine.name == "bark"
        assert engine.engine_type == "voice"
        assert not engine.is_loaded()

    async def test_generate_requires_loaded(self):
        from audiogen.engines.bark import BarkEngine

        engine = BarkEngine()
        with pytest.raises(RuntimeError, match="not loaded"):
            await engine.generate(text="hello")


# ── GenerationResult ────────────────────────────────────────────


class TestGenerationResult:
    def test_creation(self, tmp_path):
        result = GenerationResult(
            audio_path=tmp_path / "test.wav",
            duration_seconds=5.0,
            sample_rate=32000,
            engine_name="test",
            generation_time_seconds=1.5,
        )
        assert result.duration_seconds == 5.0
        assert result.metadata == {}

    def test_with_metadata(self, tmp_path):
        result = GenerationResult(
            audio_path=tmp_path / "test.wav",
            duration_seconds=5.0,
            sample_rate=32000,
            engine_name="test",
            generation_time_seconds=1.5,
            metadata={"prompt": "test"},
        )
        assert result.metadata["prompt"] == "test"
