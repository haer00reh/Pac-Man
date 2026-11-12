import json
import sys
from typing import Any

from mazegenerator import MazeGenerator
from pydantic import BaseModel, ConfigDict
from objects import Ghost, PacGum, Pacman


class Config(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file_path: str = ""
    data: dict[str, Any] = {}
    pacman: Pacman | None = None
    ghosts: list[Ghost] = []
    pacgums: list[PacGum] = []
    maps: list[MazeGenerator] = []

    def reject_duplicate_params(
        pairs: list[tuple[str, Any]],
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        for key, value in pairs:
            if key in params:
                raise ValueError(f"Duplicate parameter: {key}")
            params[key] = value
        return params

    def parse(self, content: str) -> dict[str, Any]:
        return json.loads(content, object_pairs_hook=self.reject_duplicate_params)

    def extract(self):
        try:
            with open(self.file_path, "r") as f:
                content = "".join(line.rsplit("#", 1)[0] for line in f)
            self.data = self.parse(content)
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            sys.exit(1)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error: Invalid JSON format - {e}")
            sys.exit(1)

    def init(self):
        self.maps = [
            MazeGenerator(
                size=(level["width"], level["height"]),
                seed=self.data.get("seed", 0),
            )
            for level in self.data.get("level", [])
        ]
