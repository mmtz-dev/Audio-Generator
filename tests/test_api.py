"""Tests for the FastAPI REST API endpoints."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from audiogen.core.engine import GenerationResult


@pytest.fixture
def mock_result(tmp_path):
    """Create a mock generation result with a real temp file."""
    audio_path = tmp_path / "test.wav"
    audio_path.write_bytes(b"\x00" * 100)
    return GenerationResult(
        audio_path=audio_path,
        duration_seconds=5.0,
        sample_rate=32000,
        engine_name="musicgen",
        generation_time_seconds=1.5,
    )


@pytest.fixture
def client(tmp_path, mock_result):
    """Create a test client with mocked dependencies."""
    from audiogen.api.dependencies import set_file_manager, set_model_manager
    from audiogen.config import Settings
    from audiogen.core.file_manager import FileManager
    from audiogen.core.model_manager import ModelManager

    settings = Settings(
        models_dir=str(tmp_path / "models"),
        outputs_dir=str(tmp_path / "outputs"),
        trained_models_dir=str(tmp_path / "checkpoints"),
    )

    # Create output dir
    (tmp_path / "outputs").mkdir()
    (tmp_path / "models").mkdir()
    (tmp_path / "checkpoints").mkdir()

    # Mock model manager
    mgr = MagicMock(spec=ModelManager)
    mock_engine = AsyncMock()
    mock_engine.generate = AsyncMock(return_value=mock_result)
    mgr.load_engine = AsyncMock(return_value=mock_engine)
    mgr.list_engines.return_value = [
        {"name": "musicgen", "type": "music", "loaded": False, "required_vram_gb": 2.0},
        {"name": "audiogen", "type": "sfx", "loaded": False, "required_vram_gb": 4.0},
        {"name": "chatterbox", "type": "voice", "loaded": False, "required_vram_gb": 2.0},
        {"name": "bark", "type": "voice", "loaded": False, "required_vram_gb": 6.0},
    ]
    mgr.get_gpu_info.return_value = {"available": False}
    mgr.scan_checkpoints.return_value = []
    set_model_manager(mgr)

    file_mgr = FileManager(settings)
    set_file_manager(file_mgr)

    # Import app after setting dependencies
    from fastapi.testclient import TestClient

    from audiogen.main import create_app

    app = create_app()
    return TestClient(app)


class TestHealthEndpoint:
    def test_health(self, client):
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"


class TestModelsEndpoint:
    def test_list_models(self, client):
        resp = client.get("/api/v1/models")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["engines"]) == 4
        names = [e["name"] for e in data["engines"]]
        assert "musicgen" in names
        assert "chatterbox" in names

    def test_list_checkpoints(self, client):
        resp = client.get("/api/v1/checkpoints")
        assert resp.status_code == 200
        assert resp.json() == []


class TestMusicEndpoint:
    def test_generate_music(self, client):
        resp = client.post(
            "/api/v1/music/generate",
            data={"prompt": "jazz piano", "duration_seconds": 5},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "audio_url" in data
        assert data["engine_used"] == "musicgen"


class TestVoiceEndpoint:
    def test_generate_voice_chatterbox(self, client, mock_result):
        mock_result.engine_name = "chatterbox"
        resp = client.post(
            "/api/v1/voice/generate",
            data={"text": "Hello world", "engine": "chatterbox"},
        )
        assert resp.status_code == 200

    def test_generate_voice_bark(self, client, mock_result):
        mock_result.engine_name = "bark"
        resp = client.post(
            "/api/v1/voice/generate",
            data={"text": "Hello world", "engine": "bark"},
        )
        assert resp.status_code == 200


class TestSFXEndpoint:
    def test_generate_sfx(self, client):
        resp = client.post(
            "/api/v1/sfx/generate",
            data={"prompt": "thunderstorm", "duration_seconds": 5},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "audio_url" in data
