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

    @staticmethod
    def reject_duplicate_params(
        pairs: list[tuple[str, Any]],
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        for key, value in pairs:
            if key in params:
                raise ValueError(f"Duplicate parameter: {key}")
            params[key] = value
        return params

    @staticmethod
    def check_values(value: Any, path: str = "config") -> None:
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if value < 0:
                raise ValueError(f"{path} cannot be negative")
        elif isinstance(value, dict):
            for key, item in value.items():
                Config.check_values(item, f"{path}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                Config.check_values(item, f"{path}[{index}]")

    def parse(self, content: str) -> dict[str, Any]:
        data = json.loads(content, object_pairs_hook=self.reject_duplicate_params)
        self.check_values(data)
        return data

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
