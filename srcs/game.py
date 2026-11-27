import random
import sys

from pydantic import BaseModel, ConfigDict, Field
from srcs.config import GameState, Config
from mazegenerator import MazeGenerator
from srcs.objects import Ghost, PacGum, Pacman, SuperPacGum
from srcs.ghosts import Blinky, Clyde, Inky, Pinky
from enum import Enum

FULL_WALL = 15
PACMAN_STEP = 0.4
GHOST_STEP = 1
FRIGHTENED_TIME = 8.0

DIRECTIONS: dict[str, tuple[int, int, int, int]] = {
    "north": (0, -1, 1, 4),
    "east": (1, 0, 2, 8),
    "south": (0, 1, 4, 1),
    "west": (-1, 0, 8, 2),
}


class Direction(Enum):
    NORTH = (0, -1, 1, 4)
    EAST = (1, 0, 2, 8)
    SOUTH = (0, 1, 4, 1)
    WEST = (-1, 0, 8, 2)
    NONE = None


class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    state: GameState = Field(default_factory=GameState)
    config: Config = Field(default_factory=Config)
    valid_positions: list[tuple[int, int]] = Field(default_factory=list)
    valid_set: set[tuple[int, int]] = Field(default_factory=set)
    maze: list[list[int]] = Field(default_factory=list)
    rng: random.Random = Field(default_factory=random.Random)

    level_index: int = 0
    status: str = "running"  # running    or    game_over   ot   won
    time_left: float = 0.0
    direction: Direction = Direction.NONE
    next_direction: Direction = Direction.NONE
    pacman_spawn: tuple[int, int] = (0, 0)
    pacman_acc: float = 0.0
    ghost_acc: float = 0.0
    size: tuple[int, int] = (0, 0)
    level_completed: bool = False

    @classmethod
    def _getconfig(cls, file_path: str | None):
        if file_path is None:
            raise ValueError("Config file not found")
        config = Config(file_path=file_path)
        config.extract()
        return config.highscore_file

    def setup(self, file_path: str | None) -> None:
        if file_path is None:
            raise ValueError("Config file not found")
        self.config.file_path = file_path
        self.config.extract()

        random.seed(self.config.seed)
        self.load_level(0)
        self.status = "running"

    def load_level(self, level_index: int) -> None:
        levels = self.config.data.get("level")
        if not isinstance(levels, list) or not 0 <= level_index < len(levels):
            print(f"Level not found: {level_index}", file=sys.stderr)
            sys.exit(1)
        try:
            dat = levels[level_index]
            self.size = (dat["width"], dat["height"])
        except (KeyError, TypeError):
            print(f"Invalid level definition: {level_index}", file=sys.stderr)
            sys.exit(1)

        if self.size[0] >= 27 or self.size[1] >= 27:
            print(f"Invalid width or height for lvl {level_index}, 27 max",
                  file=sys.stderr)
            sys.exit(1)

        self.maze = MazeGenerator(seed=self.config.seed, size=self.size).maze
        if not self.maze:
            print(f"Level not found: {level_index}", file=sys.stderr)
            sys.exit(1)

        self.level_index = level_index
        self.rng = random.Random(self.config.seed + level_index)
        self.time_left = float(self.config.time_limit)
        self.collect_valid_positions()
        self.init_positions()

    def collect_valid_positions(self) -> None:
        self.valid_positions = [
            (x, y)
            for y, row in enumerate(self.maze)
            for x, cell in enumerate(row)
            if cell != FULL_WALL
        ]
        self.valid_set = set(self.valid_positions)

    def closest_euclidean_valid(self) -> tuple[int, int]:
        width = len(self.maze[0])
        height = len(self.maze)
        center = (width // 2, height // 2)
        return min(
            self.valid_positions,
            key=lambda pos: ((pos[0] - center[0]) ** 2 + (pos[1] - center[1])
                             ** 2),
        )

    def init_positions(self) -> None:
        if not self.valid_positions:
            print("Maze has no valid positions", file=sys.stderr)
            sys.exit(1)

        self.state = GameState(lives=self.config.lives)
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.pacman_acc = 0.0
        self.ghost_acc = 0.0

        width = len(self.maze[0])
        height = len(self.maze)
        center = (width // 2, height // 2)
        corners = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        ]
        if center in self.valid_set:
            spawn = center
        else:
            spawn = self.closest_euclidean_valid()
        self.pacman_spawn = spawn
        self.state.pacman = Pacman(x=spawn[0], y=spawn[1], state="alive")

        if not all(corner in self.valid_set for corner in corners):
            print("Invalid corner positions", file=sys.stderr)
            sys.exit(1)

        for ghost_cls, (cx, cy) in zip((Blinky, Clyde, Inky, Pinky), corners):
            self.state.ghosts.append(ghost_cls(
                x=cx, start_x=cx, y=cy, start_y=cy, state="alive",
                score=self.config.point_per_ghost, pacman=self.state.pacman,
            ))
            self.state.super_pacgums.append(SuperPacGum(
                x=cx, y=cy, eaten=False, score=self.config.point_per_sgum,
            ))

        excluded = set(corners)
        excluded.add(spawn)
        available = [pos for pos in self.valid_positions
                     if pos not in excluded]
        count = min(self.config.data.get("pacgum", 0), len(available))
        for x, y in self.rng.sample(available, count):
            self.state.pacgums.append(
                PacGum(x=x, y=y, eaten=False, score=self.config.point_per_gum)
            )

    def set_direction(self, direction: Direction) -> None:
        """Call this from your input handler."""
        if direction in Direction:
            self.next_direction = direction

    def can_move(self, x: int, y: int, direction: Direction) -> bool:
        if direction not in Direction:
            return False
        if direction.value is None:
            return False
        dx, dy, wall, opposite_wall = direction.value
        nx, ny = x + dx, y + dy

        if not (0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0])):
            return False
        if self.maze[y][x] & wall:
            return False
        if self.maze[ny][nx] & opposite_wall:
            return False
        return True

    def update_pacman(self) -> None:
        pacman = self.state.pacman
        if pacman is None:
            return
        pacman.prev_x = pacman.x
        pacman.prev_y = pacman.y
        for direction in (self.next_direction, self.direction):
            if direction and self.can_move(pacman.x, pacman.y, direction):
                self.direction = direction
                dx, dy = direction.value[:2]
                pacman.x += dx
                pacman.y += dy
                pacman.direction = (dx, dy)
                return

    def update_visuals(self) -> None:
        t = self.pacman_acc / PACMAN_STEP
        if self.state.pacman is None:
            return
        self.state.pacman.visual_x = (self.state.pacman.prev_x + (
            self.state.pacman.x - self.state.pacman.prev_x) * t)
        self.state.pacman.visual_y = (self.state.pacman.prev_y + (
            self.state.pacman.y - self.state.pacman.prev_y) * t)

    def update_ghost_visuals(self) -> None:
        for ghost in self.state.ghosts:
            if ghost.visual_x is None or ghost.visual_y is None:
                continue
            t = self.ghost_acc / GHOST_STEP
            ghost.visual_x = ghost.prev_x + (ghost.x - ghost.prev_x) * t
            ghost.visual_y = ghost.prev_y + (ghost.y - ghost.prev_y) * t

    def update_ghosts(self) -> None:
        blinky = next((g for g in self.state.ghosts if isinstance(g, Blinky)),
                      None)
        for ghost in self.state.ghosts:
            if ghost.edible:
                ghost.wander(self.maze, self.rng)
            else:
                ghost.chase(self.maze, blinky)

    def eat_ghost(self, ghost: Ghost) -> None:
        self.state.score += ghost.score
        ghost.respawn()

    def reset_positions(self) -> None:
        pacman = self.state.pacman
        if pacman is not None:
            pacman.x, pacman.y = self.pacman_spawn
        if pacman is not None:
            pacman.direction = (0, 0)
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.state.frightened_timer = 0.0
        for ghost in self.state.ghosts:
            ghost.respawn()

    def lose_life(self) -> None:
        self.state.lives -= 1
        if self.state.lives <= 0:
            self.status = "game_over"
        else:
            self.reset_positions()

    def check_ghost_collisions(self) -> None:
        pacman = self.state.pacman
        if not pacman:
            return
        for ghost in self.state.ghosts:
            if (ghost.x, ghost.y) != (pacman.x, pacman.y):
                continue
            if ghost.edible:
                self.eat_ghost(ghost)
            else:
                self.lose_life()
                return

    def frighten_ghosts(self) -> None:
        self.state.frightened_timer = FRIGHTENED_TIME
        for ghost in self.state.ghosts:
            ghost.edible = True
            ghost.state = "vulnerable"

    def check_gums_collisions(self) -> None:
        pacman = self.state.pacman
        if not pacman:
            return
        pos = (pacman.x, pacman.y)
        for pacgum in self.state.pacgums:
            if not pacgum.eaten and (pacgum.x, pacgum.y) == pos:
                pacgum.eaten = True
                self.state.score += pacgum.score
        for super_pacgum in self.state.super_pacgums:
            if (not super_pacgum.eaten
                    and (super_pacgum.x, super_pacgum.y) == pos):
                super_pacgum.eaten = True
                self.state.score += super_pacgum.score
                self.frighten_ghosts()
        self.state.pacgums = [g for g in self.state.pacgums if not g.eaten]
        self.state.super_pacgums = [g for g in self.state.super_pacgums
                                    if not g.eaten]

    def update_frightened(self, delta_time: float) -> None:
        if self.state.frightened_timer <= 0:
            return
        self.state.frightened_timer -= delta_time
        if self.state.frightened_timer <= 0:
            self.state.frightened_timer = 0.0
            for ghost in self.state.ghosts:
                if ghost.edible:
                    ghost.edible = False
                    ghost.state = "alive"

    def check_game_over(self) -> bool:
        return self.state.lives <= 0 or self.time_left <= 0

    def check_level_completion(self) -> bool:
        return (all(g.eaten for g in self.state.pacgums)
                and all(g.eaten for g in self.state.super_pacgums))

    def advance_level(self) -> None:
        next_index = self.level_index + 1
        if next_index >= len(self.config.data.get("level", [])):
            self.status = "won"
        else:
            self.load_level(next_index)
        self.level_completed = True

    def update(self, delta_time: float) -> None:
        """delta_time in seconds."""
        if self.status != "running":
            return

        self.time_left -= delta_time
        self.update_frightened(delta_time)

        self.pacman_acc += delta_time
        while self.pacman_acc >= PACMAN_STEP and self.status == "running":
            self.pacman_acc -= PACMAN_STEP
            self.update_pacman()
            self.check_gums_collisions()
            self.check_ghost_collisions()
            print("loop1")

        self.ghost_acc += delta_time
        while self.ghost_acc >= GHOST_STEP and self.status == "running":
            self.ghost_acc -= GHOST_STEP
            self.update_ghosts()
            self.check_ghost_collisions()
            print("loop2")

        self.update_visuals()
        self.update_ghost_visuals()
        if self.status != "running":
            return
        if self.check_game_over():
            self.status = "game_over"
        elif self.check_level_completion():
            self.advance_level()
