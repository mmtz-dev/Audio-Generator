from __future__ import annotations

from audiogen.core.file_manager import FileManager
from audiogen.core.model_manager import ModelManager

# Singletons initialized during app startup (see main.py)
_model_manager: ModelManager | None = None
_file_manager: FileManager | None = None


def set_model_manager(mgr: ModelManager) -> None:
    global _model_manager
    _model_manager = mgr


def set_file_manager(fm: FileManager) -> None:
    global _file_manager
    _file_manager = fm


def get_model_manager() -> ModelManager:
    if _model_manager is None:
        raise RuntimeError("ModelManager not initialized")
    return _model_manager


def get_file_manager() -> FileManager:
    if _file_manager is None:
        raise RuntimeError("FileManager not initialized")
    return _file_manager
