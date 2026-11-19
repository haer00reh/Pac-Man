import json
import sys
from typing import Any
import random
from mazegenerator import MazeGenerator
from pydantic import BaseModel, ConfigDict
from objects import Ghost, PacGum, Pacman, SuperPacGum
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
def get_inky_target(self):
    projected = self.get_ahead_position(self.state.pacman, 2)

    blinky = self.state.ghosts[0]

    target_x = 2 * projected[0] - blinky.x
    target_y = 2 * projected[1] - blinky.y

    return target_x, target_y
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
    current_score: int = 0
    ghosts: list[Ghost] = []
    pacgums: list[PacGum] = []
    super_pacgums: list[SuperPacGum] = []
    projected = self.get_ahead_position(self.state.pacman, 2)

    blinky = self.state.ghosts[0]

    target_x = 2 * projected[0] - blinky.x
    target_y = 2 * projected[1] - blinky.y

    return target_x, target_y
    maps: list[MazeGenerator] = []


class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    state: GameState = GameState()
    config: Config = Config()
    valid_positions: list[tuple[int, int]] = []
    maze: list[list[int]] = []

    def load_level(self, level_index: int):
        dat = self.config.data.get("level")[level_index]
        self.maze = MazeGenerator(seed=self.config.seed, size=(dat["width"], dat["height"])).maze
        if not self.maze:
            print(f"Level not found: {level_index}", file=sys.stderr)
            sys.exit(1)


    def collect_valid_positions(self) -> None:
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell != 15:
                    self.valid_positions.append((x, y))

    def closest_euclidean_valid(self):
        width = len(self.maze[0])
        height = len(self.maze)
        center = (width // 2, height // 2)
        closest = min(self.valid_positions, key=lambda pos: (pos[0] - center[0])**2 + (pos[1] - center[1])**2)
        return closest


    def init_positions(self):
        width = len(self.maze[0])
        height = len(self.maze)
        center = (width // 2, height // 2)
        corners = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1)
        ]

        if center in self.valid_positions:
            self.state.pacman = Pacman(x=center[0], y=center[1], state="alive")
        else:
            closest = self.closest_euclidean_valid()
            self.state.pacman = Pacman(x=closest[0], y=closest[1], state="alive")

        if all(corner in self.valid_positions for corner in corners):
            self.state.ghosts.append(Blinky(x=corners[0][0], start_x=corners[0][0],
             y=corners[0][1], start_y=corners[0][1], state="alive",
              score=self.config.point_per_ghost, pacman=self.state.pacman))

            self.state.ghosts.append(Clyde(x=corners[1][0], start_x=corners[1][0],
             y=corners[1][1], start_y=corners[1][1], state="alive",
              score=self.config.point_per_ghost, pacman=self.state.pacman))

            self.state.ghosts.append(Inky(x=corners[2][0], start_x=corners[2][0],
             y=corners[2][1], start_y=corners[2][1], state="alive",
              score=self.config.point_per_ghost, pacman=self.state.pacman))

            self.state.ghosts.append(Pinky(x=corners[3][0], start_x=corners[3][0],
             y=corners[3][1], start_y=corners[3][1], state="alive",
              score=self.config.point_per_ghost, pacman=self.state.pacman))

            self.state.super_pacgums.append(SuperPacGum(x=corners[0][0], y=corners[0][1], eaten=False, score=self.config.point_per_sgum))
            self.state.super_pacgums.append(SuperPacGum(x=corners[1][0], y=corners[1][1], eaten=False, score=self.config.point_per_sgum))
            self.state.super_pacgums.append(SuperPacGum(x=corners[2][0], y=corners[2][1], eaten=False, score=self.config.point_per_sgum))
            self.state.super_pacgums.append(SuperPacGum(x=corners[3][0], y=corners[3][1], eaten=False, score=self.config.point_per_sgum))
        else:
            print("Invalid corner positions", file=sys.stderr)
            sys.exit(1)

        excluded_positions = set(corners)
        pacman_position = (self.state.pacman.x, self.state.pacman.y)
        excluded_positions.add(pacman_position)
        available_positions = [pos for pos in self.valid_positions if pos not in excluded_positions]
        pacgum_count = min(self.config.data.get("pacgum", 0), len(available_positions))
        for x, y in random.sample(available_positions, pacgum_count):
            self.state.pacgums.append(PacGum(x=x, y=y, eaten=False, score=self.config.point_per_gum))

    def can_move(self, x, y, direction):
        walls = {
            "north": (0, -1, 1, 4),
            "east": (1, 0, 2, 8),
            "south": (0, 1, 4, 1),
            "west": (-1, 0, 8, 2)
        }

        dx, dy, wall, opposite_wall = walls[direction]

        nx = x + dx
        ny = y + dy

        if not (0 <= ny < len(self.maze) and
                0 <= nx < len(self.maze[0])):
            return False

        if self.maze[y][x] & wall:
            return False

        if self.maze[ny][nx] & opposite_wall:
            return False

        return True


    def eat_ghost(self, ghost):
        ghost.state = "vulnerable"
        self.state.score += ghost.score
        ghost.respawn()

    def lose_life(self):
        self.state.lives -= 1

    def check_ghost_collisions(self):
        pacman = self.state.pacman

        if not pacman:
            return
        for ghost in self.state.ghosts:
            if pacman.x == ghost.x and pacman.y == ghost.y:
                if ghost.edible:
                    self.eat_ghost(ghost)
                else:
                    self.lose_life()
    
    def check_gums_collisions(self):
        pacman = self.state.pacman

        if not pacman:
            return
        for pacgum in self.state.pacgums:
            if pacman.x == pacgum.x and pacman.y == pacgum.y:
                pacgum.eaten = True
                self.state.score += pacgum.score
        for super_pacgum in self.state.super_pacgums:
            if pacman.x == super_pacgum.x and pacman.y == super_pacgum.y:
                super_pacgum.eaten = True
                self.state.score += super_pacgum.score

    def update(self):
        pass
