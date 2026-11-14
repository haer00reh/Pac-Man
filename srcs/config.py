import json
import sys
from typing import Any

from mazegenerator import MazeGenerator
from pydantic import BaseModel, ConfigDict
from objects import Ghost, PacGum, Pacman


class Config(BaseModel):

    file_path: str = ""
    data: dict[str, Any] = {}
    time_limit: int = 0
    seed: int = 42
    point_per_gum: int = 0
    point_per_sgum: int = 0
    point_per_ghost: int = 0

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
        self.time_limit = self.data.get("level_max_time", 90)
        self.seed = self.data.get("seed", 42)
        self.point_per_gum = self.data.get("points_per_pacgum", 1)
        self.point_per_sgum = self.data.get("points_per_super_pacgum", 3)
        self.point_per_ghost = self.data.get("points_per_ghost", 6)





class GameState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pacman: Pacman | None = None
    ghosts: list[Ghost] = []
    pacgums: list[PacGum] = []
    maps: list[MazeGenerator] = []


class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    state: GameState = GameState()
    config: Config = Config()


    def load_level(self, level_index):
        pass

    def update(self):
        pass
