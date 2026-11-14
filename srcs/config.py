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

    def load_level(self, level_index: int):
        maze = self.config.data.get(f"level_{level_index}")
        if not maze:
            print(f"Level not found: {level_index}", file=sys.stderr)
            sys.exit(1)
        

    def dfs(self, maze: list[list[int]]) -> None:
        height = len(maze)
        width = len(maze[0])
        start = (height // 2, width // 2)
        directions = [
            (0, -1, 1, 4), #up
            (1, 0, 2, 8), #right
            (0, 1, 4, 1), #down
            (-1, 0, 8, 2) #left
        ]

        stack = [start]
        visited = set()

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            self.valid_positions.append((x, y))
            for dx, dy, wall, opposite in directions:
                new_x, new_y = x + dx, y + dy
                if not (0 <= new_x < width and 0 <= new_y < height):
                    continue
                if maze[y][x] & wall:
                    continue
                if maze[new_y][new_x] & opposite:
                    continue
                if (new_x, new_y) not in visited:
                    stack.append((new_x, new_y))


    def update(self):
        pass
