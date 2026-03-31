from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

from audiogen.config import Settings


class FileManager:
    """Manages output files and temporary storage."""

    def __init__(self, settings: Settings) -> None:
        self._outputs_dir = Path(settings.outputs_dir)
        self._outputs_dir.mkdir(parents=True, exist_ok=True)

    def generate_output_path(
        self,
        prefix: str,
        extension: str = "wav",
    ) -> Path:
        """Generate a unique output file path organized by date."""
        date_dir = self._outputs_dir / datetime.now().strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)

        short_id = uuid.uuid4().hex[:8]
        filename = f"{prefix}_{short_id}.{extension}"
        return date_dir / filename

    def get_output_url(self, path: Path) -> str:
        """Convert an output file path to a relative URL for the API."""
        try:
            relative = path.relative_to(self._outputs_dir)
        except ValueError:
            return f"/outputs/{path.name}"
        return f"/outputs/{relative}"

    @property
    def outputs_dir(self) -> Path:
        return self._outputs_dir
