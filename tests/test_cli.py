"""Tests for the Typer CLI application."""

from __future__ import annotations

from typer.testing import CliRunner

from audiogen.cli.main import app

runner = CliRunner()


class TestCLIHelp:
    def test_main_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "music" in result.output
        assert "voice" in result.output
        assert "sfx" in result.output
        assert "serve" in result.output

    def test_music_help(self):
        result = runner.invoke(app, ["music", "--help"])
        assert result.exit_code == 0
        assert "--duration" in result.output
        assert "--model" in result.output
        assert "--output" in result.output

    def test_voice_help(self):
        result = runner.invoke(app, ["voice", "--help"])
        assert result.exit_code == 0
        assert "--engine" in result.output
        assert "--reference" in result.output
        assert "--exaggeration" in result.output

    def test_sfx_help(self):
        result = runner.invoke(app, ["sfx", "--help"])
        assert result.exit_code == 0
        assert "--duration" in result.output

    def test_models_help(self):
        result = runner.invoke(app, ["models", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "checkpoints" in result.output

    def test_serve_help(self):
        result = runner.invoke(app, ["serve", "--help"])
        assert result.exit_code == 0
        assert "--host" in result.output
        assert "--port" in result.output


class TestCLIModels:
    def test_models_list_local(self):
        """Models list should work without GPU (just initializes engines)."""
        result = runner.invoke(app, ["models", "list"])
        assert result.exit_code == 0
        assert "musicgen" in result.output
        assert "chatterbox" in result.output
        assert "audiogen" in result.output
        assert "bark" in result.output

    def test_models_checkpoints_empty(self):
        result = runner.invoke(app, ["models", "checkpoints"])
        # Should succeed even with no checkpoints
        assert result.exit_code == 0
