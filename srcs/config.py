import json
import sys
from typing import Any
import random
from mazegenerator import MazeGenerator
from pydantic import BaseModel, ConfigDict
from objects import Ghost, PacGum, Pacman
from ghosts import Blinky, Clyde, Inky, Pinky

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
            print(f"Error: File not found - {e}", file=sys.stderr)
            sys.exit(1)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error: Invalid JSON format - {e}", file=sys.stderr)
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
    valid_positions: list[tuple[int, int]] = []
    maze: list[list[int]] = []

    def load_level(self, level_index: int):
        self.maze = self.config.data.get(f"level_{level_index}")
        if not self.maze:
            print(f"Level not found: {level_index}", file=sys.stderr)
            sys.exit(1)


    def validate_positions(self) -> None:
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell != 15:
                    self.valid_positions.append((x, y))

    def init_positions(self):
        width = len(self.maze[0])
        height = len(self.maze)
        center = (width // 2, height // 2)
        pacgums_len = self.config.data.get("pacgum", 0)
        corners = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1)
        ]

        if center in self.valid_positions:
            self.state.pacman = Pacman(x=width // 2, y=height // 2)
        else:
            print("Invalid pacman position", file=sys.stderr)
            sys.exit(1)

        if all(corner in self.valid_positions for corner in corners):
            self.state.ghosts.append(Blinky(x=corners[0][0], y=corners[0][1], state="alive"))
            self.state.ghosts.append(Clyde(x=corners[1][0], y=corners[1][1], state="alive"))
            self.state.ghosts.append(Inky(x=corners[2][0], y=corners[2][1], state="alive"))
            self.state.ghosts.append(Pinky(x=corners[3][0], y=corners[3][1], state="alive"))
        else:
            print("Invalid ghost positions", file=sys.stderr)
            sys.exit(1)

        excluded_positions = set(corners)
        excluded_positions.add(center)
        available_positions = [pos for pos in self.valid_positions if pos not in excluded_positions]
        pacgum_count = min(self.config.data.get("pacgum", 0), len(available_positions))
        for i in range(pacgum_count):
            x, y = random.sample(available_positions, pacgum_count)
            self.state.pacgums.append(PacGum(x=x, y=y, eaten=False))

    def update(self):
        pass
